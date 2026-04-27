-- ============================================================
-- Data Quality Checks — run after each ETL load
-- All queries should return 0 rows if data is clean.
-- ============================================================

-- Check 1: Null order keys in fact table
SELECT 'NULL order_id' AS check_name, COUNT(*) AS violations
FROM fact_sales WHERE order_id IS NULL;

-- Check 2: Orphaned fact rows (no matching dimension)
SELECT 'Orphaned customer_id' AS check_name, COUNT(*) AS violations
FROM fact_sales f
LEFT JOIN dim_customer c ON f.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

SELECT 'Orphaned product_id' AS check_name, COUNT(*) AS violations
FROM fact_sales f
LEFT JOIN dim_product p ON f.product_id = p.product_id
WHERE p.product_id IS NULL;

-- Check 3: Negative revenue
SELECT 'Negative revenue' AS check_name, COUNT(*) AS violations
FROM fact_sales WHERE revenue < 0;

-- Check 4: Invalid discount range
SELECT 'Invalid discount (>1 or <0)' AS check_name, COUNT(*) AS violations
FROM fact_sales WHERE discount < 0 OR discount > 1;

-- Check 5: Future dates
SELECT 'Future order dates' AS check_name, COUNT(*) AS violations
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.full_date > DATE('now');

-- Check 6: Duplicate orders
SELECT 'Duplicate order_id' AS check_name, COUNT(*) AS violations
FROM (
    SELECT order_id FROM fact_sales GROUP BY order_id HAVING COUNT(*) > 1
);
