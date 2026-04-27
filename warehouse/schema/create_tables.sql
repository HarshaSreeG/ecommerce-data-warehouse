-- ============================================================
-- E-Commerce Data Warehouse — Star Schema DDL
-- ============================================================

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_key        INTEGER PRIMARY KEY,
    full_date       TEXT NOT NULL,
    year            INTEGER,
    quarter         INTEGER,
    month           INTEGER,
    month_name      TEXT,
    week            INTEGER,
    day_of_month    INTEGER,
    day_of_week     INTEGER,
    day_name        TEXT,
    is_weekend      BOOLEAN
);

-- Dimension: Product
CREATE TABLE IF NOT EXISTS dim_product (
    product_id      TEXT PRIMARY KEY,
    product_name    TEXT NOT NULL,
    category        TEXT,
    sub_category    TEXT,
    unit_price      REAL,
    cost_price      REAL,
    margin_pct      REAL,
    supplier        TEXT,
    in_stock        BOOLEAN
);

-- Dimension: Customer
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id         TEXT PRIMARY KEY,
    full_name           TEXT,
    email               TEXT,
    country             TEXT,
    region              TEXT,
    customer_segment    TEXT,
    signup_date         TEXT
);

-- Dimension: Region
CREATE TABLE IF NOT EXISTS dim_region (
    region_key  INTEGER PRIMARY KEY,
    region      TEXT NOT NULL,
    country     TEXT NOT NULL
);

-- Fact: Sales
CREATE TABLE IF NOT EXISTS fact_sales (
    order_id        TEXT PRIMARY KEY,
    date_key        INTEGER REFERENCES dim_date(date_key),
    customer_id     TEXT    REFERENCES dim_customer(customer_id),
    product_id      TEXT    REFERENCES dim_product(product_id),
    region_key      INTEGER REFERENCES dim_region(region_key),
    quantity        INTEGER,
    unit_price      REAL,
    discount        REAL,
    revenue         REAL,
    shipping_cost   REAL,
    gross_profit    REAL,
    order_status    TEXT,
    payment_method  TEXT
);

-- Indexes for common join patterns
CREATE INDEX IF NOT EXISTS idx_fact_date       ON fact_sales(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_product    ON fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_customer   ON fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_region     ON fact_sales(region_key);
CREATE INDEX IF NOT EXISTS idx_fact_status     ON fact_sales(order_status);
