"""
load.py
-------
Loads transformed DataFrames into the warehouse.
Supports SQLite (dev/test) and Snowflake (production).
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from etl.utils import logger, timer
import config


def _get_engine():
    """Return a SQLAlchemy engine based on config."""
    if config.USE_SNOWFLAKE:
        sf = config.SNOWFLAKE_CONFIG
        url = (
            f"snowflake://{sf['user']}:{sf['password']}@{sf['account']}/"
            f"{sf['database']}/{sf['schema']}?warehouse={sf['warehouse']}"
        )
        logger.info("Connecting to Snowflake...")
    else:
        url = f"sqlite:///{config.SQLITE_DB_PATH}"
        logger.info(f"Connecting to SQLite: {config.SQLITE_DB_PATH}")

    return create_engine(url)


@timer
def load(tables: dict[str, pd.DataFrame]) -> None:
    """
    Load all dimension and fact tables into the warehouse.
    Uses replace strategy so re-runs are idempotent.
    """
    logger.info("── LOAD ─────────────────────────────────────")
    engine = _get_engine()

    load_order = ["dim_date", "dim_product", "dim_customer", "dim_region", "fact_sales"]

    with engine.begin() as conn:
        for table_name in load_order:
            df = tables.get(table_name)
            if df is None:
                logger.warning(f"Table '{table_name}' not found in transform output — skipping.")
                continue

            # Batch insert
            total = len(df)
            df.to_sql(table_name, con=conn, if_exists="replace", index=False,
                      chunksize=config.BATCH_SIZE, method="multi")
            logger.info(f"  ✓ Loaded {total:,} rows → {table_name}")

    logger.info("All tables loaded successfully.")


@timer
def export_for_dashboard(tables: dict[str, pd.DataFrame]) -> None:
    """Export key tables as CSVs for Tableau / Power BI."""
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    export_tables = ["fact_sales", "dim_date", "dim_product", "dim_customer", "dim_region"]

    for name in export_tables:
        df = tables.get(name)
        if df is not None:
            path = f"{config.EXPORT_DIR}/{name}.csv"
            df.to_csv(path, index=False)
            logger.info(f"  ✓ Exported {name} → {path}")
