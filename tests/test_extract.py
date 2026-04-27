"""Unit tests for extract.py"""

import pytest
import pandas as pd
import os
import tempfile
from etl.extract import _read_csv, validate_row_counts


def write_temp_csv(data: dict, tmp_dir: str, filename: str) -> str:
    path = os.path.join(tmp_dir, filename)
    pd.DataFrame(data).to_csv(path, index=False)
    return path


def test_read_csv_valid(tmp_path):
    path = write_temp_csv(
        {"order_id": ["O1"], "order_date": ["2023-01-01"], "customer_id": ["C1"],
         "product_id": ["P1"], "quantity": [1], "unit_price": [10.0], "revenue": [10.0]},
        str(tmp_path), "orders.csv"
    )
    df = _read_csv(path, {"order_id", "order_date", "customer_id", "product_id", "quantity", "unit_price", "revenue"})
    assert len(df) == 1


def test_read_csv_missing_columns(tmp_path):
    path = write_temp_csv({"order_id": ["O1"]}, str(tmp_path), "bad.csv")
    with pytest.raises(ValueError, match="Missing required columns"):
        _read_csv(path, {"order_id", "revenue"})


def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        _read_csv("/nonexistent/path.csv", {"order_id"})


def test_validate_row_counts_passes():
    data = {"orders": pd.DataFrame({"a": [1, 2]})}
    validate_row_counts(data, min_rows=1)  # Should not raise


def test_validate_row_counts_fails():
    data = {"orders": pd.DataFrame()}
    with pytest.raises(ValueError, match="0 rows"):
        validate_row_counts(data, min_rows=1)
