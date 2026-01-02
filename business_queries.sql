-- Query 1: Customer Purchase History
SELECT c.customer_id, c.first_name, c.last_name,
COUNT(o.order_id) AS total_orders,
SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING COUNT(o.order_id) >= 2 AND SUM(o.total_amount) > 5000;

-- Query 2: Product Sales Analysis
SELECT p.category, SUM(oi.subtotal) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
HAVING SUM(oi.subtotal) > 10000;

-- Query 3: Monthly Sales Trend
SELECT MONTHNAME(order_date) AS month_name,
COUNT(order_id) AS total_orders,
SUM(total_amount) AS monthly_revenue,
SUM(SUM(total_amount)) OVER (ORDER BY MONTH(order_date)) AS cumulative_revenue
FROM orders
WHERE YEAR(order_date) = 2024
GROUP BY MONTH(order_date), MONTHNAME(order_date)
ORDER BY MONTH(order_date);

