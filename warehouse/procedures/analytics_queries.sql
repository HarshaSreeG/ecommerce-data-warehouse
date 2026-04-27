-- ============================================================
-- E-Commerce DW — Pre-Built Analytics Queries
-- ============================================================

-- ── 1. Monthly Revenue Trend ─────────────────────────────────
SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(f.order_id)       AS total_orders,
    SUM(f.quantity)         AS units_sold,
    ROUND(SUM(f.revenue), 2)       AS total_revenue,
    ROUND(AVG(f.revenue), 2)       AS avg_order_value,
    ROUND(SUM(f.gross_profit), 2)  AS total_gross_profit
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.order_status = 'completed'
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;


-- ── 2. Top 10 Products by Revenue ────────────────────────────
SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(f.order_id)               AS order_count,
    SUM(f.quantity)                 AS units_sold,
    ROUND(SUM(f.revenue), 2)        AS total_revenue,
    ROUND(AVG(f.discount) * 100, 1) AS avg_discount_pct
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
WHERE f.order_status = 'completed'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;


-- ── 3. Revenue by Category ───────────────────────────────────
SELECT
    p.category,
    COUNT(DISTINCT f.order_id)      AS orders,
    ROUND(SUM(f.revenue), 2)        AS revenue,
    ROUND(
        SUM(f.revenue) * 100.0 / SUM(SUM(f.revenue)) OVER (), 2
    )                               AS revenue_pct
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
WHERE f.order_status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;


-- ── 4. Regional Sales Breakdown ──────────────────────────────
SELECT
    r.country,
    r.region,
    COUNT(DISTINCT f.customer_id)   AS unique_customers,
    COUNT(f.order_id)               AS orders,
    ROUND(SUM(f.revenue), 2)        AS revenue,
    ROUND(AVG(f.revenue), 2)        AS avg_order_value
FROM fact_sales f
JOIN dim_region r ON f.region_key = r.region_key
WHERE f.order_status = 'completed'
GROUP BY r.country, r.region
ORDER BY revenue DESC;


-- ── 5. Customer Lifetime Value (Top 20) ──────────────────────
SELECT
    c.customer_id,
    c.full_name,
    c.customer_segment,
    c.country,
    COUNT(f.order_id)           AS total_orders,
    ROUND(SUM(f.revenue), 2)    AS lifetime_value,
    ROUND(AVG(f.revenue), 2)    AS avg_order_value,
    MIN(f.date_key)             AS first_order_date_key,
    MAX(f.date_key)             AS last_order_date_key
FROM fact_sales f
JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE f.order_status = 'completed'
GROUP BY c.customer_id, c.full_name, c.customer_segment, c.country
ORDER BY lifetime_value DESC
LIMIT 20;


-- ── 6. Order Status Distribution ─────────────────────────────
SELECT
    order_status,
    COUNT(*)                        AS count,
    ROUND(SUM(revenue), 2)          AS revenue,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2
    )                               AS pct_of_orders
FROM fact_sales
GROUP BY order_status
ORDER BY count DESC;


-- ── 7. Payment Method Breakdown ──────────────────────────────
SELECT
    payment_method,
    COUNT(*)                    AS transactions,
    ROUND(SUM(revenue), 2)      AS total_revenue,
    ROUND(AVG(revenue), 2)      AS avg_revenue
FROM fact_sales
WHERE order_status = 'completed'
GROUP BY payment_method
ORDER BY total_revenue DESC;


-- ── 8. Quarter-over-Quarter Growth ───────────────────────────
SELECT
    year,
    quarter,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(
        (SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY year, quarter))
        * 100.0 / LAG(SUM(revenue)) OVER (ORDER BY year, quarter),
        2
    ) AS qoq_growth_pct
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE f.order_status = 'completed'
GROUP BY year, quarter
ORDER BY year, quarter;
