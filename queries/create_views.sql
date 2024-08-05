-- Создание представления sales_summary
CREATE VIEW sales_summary AS
SELECT
    s.date,
    p.product_name,
    r.region_name,
    SUM(s.amount) AS total_amount
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN regions r ON s.region_id = r.region_id
GROUP BY s.date, p.product_name, r.region_name;
