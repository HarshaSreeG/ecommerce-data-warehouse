"""
pipeline.py
-----------
Orchestrates the full ETL: Extract → Transform → Load → Export.
"""

from etl.extract import extract, validate_row_counts
from etl.transform import transform
from etl.load import load, export_for_dashboard
from etl.utils import logger, timer
import config


@timer
def run_pipeline(
    orders_path: str    = f"{config.SAMPLE_DATA_DIR}/orders.csv",
    products_path: str  = f"{config.SAMPLE_DATA_DIR}/products.csv",
    customers_path: str = f"{config.SAMPLE_DATA_DIR}/customers.csv",
    export_csv: bool    = True,
) -> dict:
    """
    Full ETL pipeline.

    Args:
        orders_path:    Path to orders CSV.
        products_path:  Path to products CSV.
        customers_path: Path to customers CSV.
        export_csv:     Whether to export CSVs for dashboard.

    Returns:
        dict of table_name → DataFrame (the transformed warehouse tables).
    """
    logger.info("════════════════════════════════════════════")
    logger.info("  E-Commerce Data Warehouse ETL Pipeline   ")
    logger.info("════════════════════════════════════════════")

    # 1. Extract
    raw = extract(orders_path, products_path, customers_path)
    validate_row_counts(raw)

    # 2. Transform
    tables = transform(raw)

    # 3. Load
    load(tables)

    # 4. Export for BI tools
    if export_csv:
        export_for_dashboard(tables)

    logger.info("════════════════════════════════════════════")
    logger.info("  Pipeline completed successfully!          ")
    logger.info("════════════════════════════════════════════")

    return tables
