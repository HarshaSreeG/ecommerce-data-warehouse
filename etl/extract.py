"""
extract.py
----------
Reads raw CSV files and runs basic validation checks.
Returns DataFrames ready for the transform step.
"""

import os
import pandas as pd
from etl.utils import logger, timer

REQUIRED_ORDER_COLS   = {"order_id", "order_date", "customer_id", "product_id", "quantity", "unit_price", "revenue"}
REQUIRED_PRODUCT_COLS = {"product_id", "product_name", "category", "unit_price"}
REQUIRED_CUSTOMER_COLS = {"customer_id", "first_name", "last_name", "email", "country", "region"}


def _read_csv(path: str, required_cols: set) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_csv(path)
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {path}: {missing}")

    logger.info(f"Loaded {len(df):,} rows from {path}")
    return df


@timer
def extract(orders_path: str, products_path: str, customers_path: str) -> dict[str, pd.DataFrame]:
    """
    Extract all three source CSVs.

    Returns:
        dict with keys 'orders', 'products', 'customers'
    """
    logger.info("── EXTRACT ──────────────────────────────────")
    return {
        "orders":    _read_csv(orders_path,    REQUIRED_ORDER_COLS),
        "products":  _read_csv(products_path,  REQUIRED_PRODUCT_COLS),
        "customers": _read_csv(customers_path, REQUIRED_CUSTOMER_COLS),
    }


def validate_row_counts(data: dict[str, pd.DataFrame], min_rows: int = 1) -> None:
    """Raise if any DataFrame is empty."""
    for name, df in data.items():
        if len(df) < min_rows:
            raise ValueError(f"'{name}' has {len(df)} rows — expected at least {min_rows}.")
    logger.info("Row count validation passed.")
