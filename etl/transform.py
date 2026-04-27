"""
transform.py
------------
Cleans raw DataFrames and builds the star-schema dimension and fact tables.

Dimensions produced:  dim_date, dim_product, dim_customer, dim_region
Fact table produced:  fact_sales
"""

import pandas as pd
import numpy as np
from etl.utils import logger, timer


# ── Helpers ──────────────────────────────────────────────────────────────────

def _drop_duplicates(df: pd.DataFrame, key: str, label: str) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=[key])
    dropped = before - len(df)
    if dropped:
        logger.warning(f"Dropped {dropped} duplicate {key} rows in {label}.")
    return df


def _fill_nulls(df: pd.DataFrame, defaults: dict) -> pd.DataFrame:
    return df.fillna(defaults)


# ── Dimension Builders ────────────────────────────────────────────────────────

@timer
def build_dim_date(orders: pd.DataFrame) -> pd.DataFrame:
    """Expand every unique order date into a full date dimension row."""
    dates = pd.to_datetime(orders["order_date"]).drop_duplicates().sort_values()
    df = pd.DataFrame({"full_date": dates})
    df["date_key"]      = df["full_date"].dt.strftime("%Y%m%d").astype(int)
    df["year"]          = df["full_date"].dt.year
    df["quarter"]       = df["full_date"].dt.quarter
    df["month"]         = df["full_date"].dt.month
    df["month_name"]    = df["full_date"].dt.strftime("%B")
    df["week"]          = df["full_date"].dt.isocalendar().week.astype(int)
    df["day_of_month"]  = df["full_date"].dt.day
    df["day_of_week"]   = df["full_date"].dt.dayofweek          # 0=Mon
    df["day_name"]      = df["full_date"].dt.strftime("%A")
    df["is_weekend"]    = df["day_of_week"].isin([5, 6])
    df["full_date"]     = df["full_date"].dt.strftime("%Y-%m-%d")
    logger.info(f"dim_date: {len(df):,} rows")
    return df


@timer
def build_dim_product(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()
    df = _drop_duplicates(df, "product_id", "dim_product")
    df = _fill_nulls(df, {"sub_category": "Unknown", "supplier": "Unknown"})
    df["unit_price"]  = pd.to_numeric(df["unit_price"],  errors="coerce").fillna(0.0).round(2)
    df["cost_price"]  = pd.to_numeric(df.get("cost_price", 0), errors="coerce").fillna(0.0).round(2)
    df["margin_pct"]  = np.where(
        df["unit_price"] > 0,
        ((df["unit_price"] - df["cost_price"]) / df["unit_price"] * 100).round(2),
        0.0,
    )
    df["in_stock"] = df.get("in_stock", True).astype(bool)
    logger.info(f"dim_product: {len(df):,} rows")
    return df[["product_id", "product_name", "category", "sub_category",
               "unit_price", "cost_price", "margin_pct", "supplier", "in_stock"]]


@timer
def build_dim_customer(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.copy()
    df = _drop_duplicates(df, "customer_id", "dim_customer")
    df["full_name"]        = df["first_name"].str.strip() + " " + df["last_name"].str.strip()
    df["email"]            = df["email"].str.lower().str.strip()
    df["customer_segment"] = df.get("customer_segment", "Bronze").fillna("Bronze")
    df["signup_date"]      = pd.to_datetime(df.get("signup_date", pd.NaT)).dt.strftime("%Y-%m-%d")
    logger.info(f"dim_customer: {len(df):,} rows")
    return df[["customer_id", "full_name", "email", "country", "region",
               "customer_segment", "signup_date"]]


@timer
def build_dim_region(customers: pd.DataFrame) -> pd.DataFrame:
    df = (
        customers[["region", "country"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    df["region_key"] = df.index + 1
    logger.info(f"dim_region: {len(df):,} rows")
    return df[["region_key", "region", "country"]]


# ── Fact Table ────────────────────────────────────────────────────────────────

@timer
def build_fact_sales(
    orders: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_customer: pd.DataFrame,
    dim_region: pd.DataFrame,
) -> pd.DataFrame:
    df = orders.copy()

    # Type coercions
    df["order_date"]    = pd.to_datetime(df["order_date"])
    df["quantity"]      = pd.to_numeric(df["quantity"],      errors="coerce").fillna(0).astype(int)
    df["unit_price"]    = pd.to_numeric(df["unit_price"],    errors="coerce").fillna(0.0).round(2)
    df["discount"]      = pd.to_numeric(df.get("discount", 0), errors="coerce").fillna(0.0).round(4)
    df["revenue"]       = pd.to_numeric(df["revenue"],       errors="coerce").fillna(0.0).round(2)
    df["shipping_cost"] = pd.to_numeric(df.get("shipping_cost", 0), errors="coerce").fillna(0.0).round(2)

    # Drop rows with null keys
    before = len(df)
    df = df.dropna(subset=["order_id", "customer_id", "product_id"])
    if len(df) < before:
        logger.warning(f"Dropped {before - len(df)} rows with null keys.")

    # Join date_key
    date_lookup = dim_date.set_index("full_date")["date_key"]
    df["date_key"] = df["order_date"].dt.strftime("%Y-%m-%d").map(date_lookup)

    # Join region_key via customer
    cust_region = (
        dim_customer[["customer_id"]]
        .merge(
            dim_region.merge(
                dim_customer[["customer_id", "region", "country"]],
                on=["region", "country"], how="inner"
            )[["customer_id", "region_key"]],
            on="customer_id", how="left"
        )
    )
    df = df.merge(cust_region[["customer_id", "region_key"]], on="customer_id", how="left")

    # Derived metrics
    df["gross_profit"] = (df["revenue"] - df["shipping_cost"]).round(2)

    # Filter only completed orders for revenue reporting (keep all for status analysis)
    logger.info(f"fact_sales: {len(df):,} rows")
    return df[[
        "order_id", "date_key", "customer_id", "product_id", "region_key",
        "quantity", "unit_price", "discount", "revenue",
        "shipping_cost", "gross_profit", "order_status", "payment_method",
    ]]


# ── Master Transform ──────────────────────────────────────────────────────────

@timer
def transform(raw: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Run all transforms. Returns dict of table_name → DataFrame."""
    logger.info("── TRANSFORM ────────────────────────────────")
    dim_date     = build_dim_date(raw["orders"])
    dim_product  = build_dim_product(raw["products"])
    dim_customer = build_dim_customer(raw["customers"])
    dim_region   = build_dim_region(raw["customers"])
    fact_sales   = build_fact_sales(raw["orders"], dim_date, dim_customer, dim_region)

    return {
        "dim_date":     dim_date,
        "dim_product":  dim_product,
        "dim_customer": dim_customer,
        "dim_region":   dim_region,
        "fact_sales":   fact_sales,
    }
