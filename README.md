# 🛒 E-Commerce Sales Data Warehouse

A production-style data warehousing project that ingests raw e-commerce CSV data, transforms it through a Python ETL pipeline, loads it into a **star-schema SQL warehouse**, and surfaces insights through an executive **Tableau / Power BI** dashboard.

---

## 📐 Architecture

```
Raw CSV Files
     │
     ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────────────┐
│  Extract    │────▶│  Transform   │────▶│   Load (Snowflake/  │
│  (Python)   │     │  (Python +   │     │    SQLite for dev)  │
│             │     │   pandas)    │     │   Star Schema DW    │
└─────────────┘     └──────────────┘     └─────────────────────┘
                                                  │
                                                  ▼
                                       ┌─────────────────────┐
                                       │  Tableau / Power BI │
                                       │  Executive Dashboard│
                                       └─────────────────────┘
```

## 🗂️ Star Schema

```
                    ┌──────────────┐
                    │  dim_date    │
                    └──────┬───────┘
                           │
┌──────────────┐    ┌──────▼───────┐    ┌──────────────┐
│  dim_product │────│  fact_sales  │────│  dim_customer│
└──────────────┘    └──────┬───────┘    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │  dim_region  │
                    └──────────────┘
```

---

## 🚀 Features

- ✅ **ETL Pipeline** — Extract from CSV, clean & validate with pandas, load into star schema
- ✅ **Star Schema Design** — fact_sales + 4 dimension tables
- ✅ **Data Quality Checks** — null checks, type validation, duplicate detection
- ✅ **Sample Data Generator** — 10,000 realistic order rows via Faker
- ✅ **SQL Analytics Queries** — pre-built queries for revenue, top products, regional trends
- ✅ **Dashboard-ready** — CSV exports + Tableau/Power BI connection guide
- ✅ **Unit Tests** — pytest coverage on ETL transforms
- ✅ **CI/CD** — GitHub Actions pipeline

---

## 📁 Project Structure

```
ecommerce-data-warehouse/
├── data/
│   ├── raw/                    # Raw input CSV files (gitignored for large files)
│   ├── processed/              # Cleaned & transformed outputs
│   └── sample/                 # Sample data for dev/testing
│       ├── orders.csv
│       ├── products.csv
│       └── customers.csv
├── etl/
│   ├── __init__.py
│   ├── extract.py              # CSV ingestion & validation
│   ├── transform.py            # Cleaning, type casting, enrichment
│   ├── load.py                 # DB loader (SQLite dev / Snowflake prod)
│   ├── pipeline.py             # Orchestrates E → T → L
│   └── utils.py                # Logging, config helpers
├── warehouse/
│   ├── schema/
│   │   ├── create_tables.sql   # DDL for all dim + fact tables
│   │   └── drop_tables.sql
│   └── procedures/
│       ├── analytics_queries.sql  # Pre-built business queries
│       └── data_quality.sql       # QA checks
├── dashboard/
│   ├── exports/                # CSV exports for Tableau/Power BI
│   └── README.md               # Dashboard setup guide
├── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   └── dashboard_guide.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── config.py
├── requirements.txt
├── generate_sample_data.py
├── run_pipeline.py
└── .gitignore
```

---

## ⚙️ Setup & Run

### 1. Clone & install

```bash
git clone https://github.com/YOUR USERNAME/ecommerce-data-warehouse.git
cd ecommerce-data-warehouse

python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate sample data

```bash
python generate_sample_data.py
```

### 3. Run the full ETL pipeline

```bash
python run_pipeline.py
```

### 4. Run tests

```bash
pytest tests/ -v
```

### 5. Query the warehouse

```bash
sqlite3 warehouse.db < warehouse/procedures/analytics_queries.sql
```

---

## 📊 Sample Analytics Queries

| Query | Description |
|---|---|
| Monthly Revenue Trend | Total revenue & orders per month |
| Top 10 Products | Best sellers by revenue and quantity |
| Regional Sales Breakdown | Revenue by region/country |
| Customer Lifetime Value | Top customers by total spend |
| Category Performance | Revenue % by product category |

---

## 🔌 Snowflake Connection (Production)

Set environment variables:

```bash
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_user
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_DATABASE=ECOMMERCE_DW
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_SCHEMA=PUBLIC
```

Then in `config.py`, set `USE_SNOWFLAKE=True`.

---

## 🗃️ Data Dictionary

See [`docs/data_dictionary.md`](docs/data_dictionary.md) for full column definitions.

---

## 👩‍💻 Built By

**Harsha Sree Gudapati**  

