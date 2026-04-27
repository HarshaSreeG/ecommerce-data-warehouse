# Data Dictionary

## fact_sales

| Column | Type | Description |
|---|---|---|
| order_id | TEXT (PK) | Unique order identifier |
| date_key | INTEGER (FK) | Foreign key → dim_date |
| customer_id | TEXT (FK) | Foreign key → dim_customer |
| product_id | TEXT (FK) | Foreign key → dim_product |
| region_key | INTEGER (FK) | Foreign key → dim_region |
| quantity | INTEGER | Units ordered |
| unit_price | REAL | Price per unit at time of order |
| discount | REAL | Discount rate (0.0–1.0) |
| revenue | REAL | Actual revenue after discount |
| shipping_cost | REAL | Shipping fee charged |
| gross_profit | REAL | revenue − shipping_cost |
| order_status | TEXT | completed / returned / pending / cancelled |
| payment_method | TEXT | Credit Card / PayPal / Debit Card / Bank Transfer |

---

## dim_date

| Column | Type | Description |
|---|---|---|
| date_key | INTEGER (PK) | YYYYMMDD integer key |
| full_date | TEXT | ISO date string (YYYY-MM-DD) |
| year | INTEGER | Calendar year |
| quarter | INTEGER | 1–4 |
| month | INTEGER | 1–12 |
| month_name | TEXT | January … December |
| week | INTEGER | ISO week number |
| day_of_month | INTEGER | 1–31 |
| day_of_week | INTEGER | 0=Monday … 6=Sunday |
| day_name | TEXT | Monday … Sunday |
| is_weekend | BOOLEAN | True for Saturday/Sunday |

---

## dim_product

| Column | Type | Description |
|---|---|---|
| product_id | TEXT (PK) | Unique product identifier |
| product_name | TEXT | Display name |
| category | TEXT | Top-level category |
| sub_category | TEXT | Sub-category |
| unit_price | REAL | Current list price |
| cost_price | REAL | Cost of goods |
| margin_pct | REAL | (unit_price − cost_price) / unit_price × 100 |
| supplier | TEXT | Supplier name |
| in_stock | BOOLEAN | Current stock status |

---

## dim_customer

| Column | Type | Description |
|---|---|---|
| customer_id | TEXT (PK) | Unique customer identifier |
| full_name | TEXT | First + last name |
| email | TEXT | Contact email (lowercase) |
| country | TEXT | Country of residence |
| region | TEXT | Sales region |
| customer_segment | TEXT | Bronze / Silver / Gold / Platinum |
| signup_date | TEXT | Account creation date |

---

## dim_region

| Column | Type | Description |
|---|---|---|
| region_key | INTEGER (PK) | Surrogate key |
| region | TEXT | Region name (North / South / East / West / Central) |
| country | TEXT | Country name |
