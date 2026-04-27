# Dashboard Setup Guide

After running the ETL pipeline, CSV files are exported to `dashboard/exports/`. Use them to connect Tableau or Power BI.

---

## Tableau

1. Open Tableau Desktop → **Connect → Text File**
2. Load `fact_sales.csv` as the primary data source
3. Add joins:
   - fact_sales `date_key` → dim_date `date_key`
   - fact_sales `product_id` → dim_product `product_id`
   - fact_sales `customer_id` → dim_customer `customer_id`
   - fact_sales `region_key` → dim_region `region_key`
4. Recommended sheets:
   - **Revenue Trend** — Line chart: `month_name` × `SUM(revenue)`
   - **Top Products** — Bar chart: `product_name` × `SUM(revenue)`
   - **Regional Map** — Filled map: `country` colored by `SUM(revenue)`
   - **Customer Segments** — Pie/treemap: `customer_segment` × `COUNT(order_id)`

---

## Power BI

1. **Get Data → Text/CSV** → load all five CSVs
2. In **Model view**, create relationships:
   - fact_sales[date_key] → dim_date[date_key]
   - fact_sales[product_id] → dim_product[product_id]
   - fact_sales[customer_id] → dim_customer[customer_id]
   - fact_sales[region_key] → dim_region[region_key]
3. Create DAX measures:
   ```
   Total Revenue = SUM(fact_sales[revenue])
   Avg Order Value = AVERAGE(fact_sales[revenue])
   Completed Orders = CALCULATE(COUNTROWS(fact_sales), fact_sales[order_status] = "completed")
   Gross Profit Margin % = DIVIDE(SUM(fact_sales[gross_profit]), SUM(fact_sales[revenue])) * 100
   ```
4. Recommended visuals:
   - **KPI cards**: Total Revenue, Total Orders, Avg Order Value, Gross Profit %
   - **Line chart**: Monthly revenue trend
   - **Bar chart**: Top 10 products by revenue
   - **Map**: Revenue by country
   - **Donut chart**: Order status split
   - **Matrix**: Category × Month revenue heatmap

---

## Snowflake Direct Connect

For live connections from Tableau/Power BI to Snowflake:

- Tableau: **Connect → Snowflake** → enter credentials from `config.py`
- Power BI: **Get Data → Snowflake** → enter server + warehouse details
