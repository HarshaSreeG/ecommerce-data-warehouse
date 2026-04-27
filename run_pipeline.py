"""
run_pipeline.py
---------------
Entry point. Run: python run_pipeline.py
"""

import argparse
import os
from etl.pipeline import run_pipeline
import config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the E-Commerce ETL pipeline.")
    parser.add_argument("--orders",    default=f"{config.SAMPLE_DATA_DIR}/orders.csv")
    parser.add_argument("--products",  default=f"{config.SAMPLE_DATA_DIR}/products.csv")
    parser.add_argument("--customers", default=f"{config.SAMPLE_DATA_DIR}/customers.csv")
    parser.add_argument("--no-export", action="store_true", help="Skip CSV export for dashboard")
    args = parser.parse_args()

    os.makedirs("logs", exist_ok=True)

    run_pipeline(
        orders_path=args.orders,
        products_path=args.products,
        customers_path=args.customers,
        export_csv=not args.no_export,
    )
