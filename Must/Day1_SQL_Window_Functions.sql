================================================================================
  DAY 1 — SQL WINDOW FUNCTIONS PRACTICE (POSTGRESQL)
  Interview: 26 May 2026 | Data Engineering + AI
================================================================================

-- Run these in PostgreSQL. Compatible with other SQL dialects with minor tweaks.
-- The queries use a sample e-commerce schema

-- =============================================================================
-- SAMPLE DATA SETUP (Run this to create test tables)
-- =============================================================================

CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    customer_name VARCHAR(100),
    order_date DATE,
    order_amount DECIMAL(10,2),
    product_category VARCHAR(50)
);

INSERT INTO orders VALUES
(1, 101, 'Alice',   '2026-01-15', 250.00, 'Electronics'),
(2, 102, 'Bob',     '2026-01-16', 120.00, 'Books'),
(3, 101, 'Alice',   '2026-02-10', 480.00, 'Electronics'),
(4, 103, 'Charlie', '2026-02-15', 75.00,  'Food'),
(5, 102, 'Bob',     '2026-03-01', 200.00, 'Electronics'),
(6, 101, 'Alice',   '2026-03-15', 90.00,  'Books'),
(7, 103, 'Charlie', '2026-03-20', 320.00, 'Electronics'),
(8, 104, 'Diana',   '2026-04-01', 150.00, 'Food'),
(9, 102, 'Bob',     '2026-04-10', 310.00, 'Electronics'),
(10, 101, 'Alice',  '2026-04-15', 600.00, 'Electronics');

-- =============================================================================
-- PROBLEM 1: Latest Order Per Customer (ROW_NUMBER)
-- =============================================================================
-- Find the most recent order for each customer.
-- Expected: Each customer's latest order row only.

-- Solution:
WITH ranked_orders AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM orders
)
SELECT order_id, customer_id, customer_name, order_date, order_amount
FROM ranked_orders
WHERE rn = 1;

-- =============================================================================
-- PROBLEM 2: Rank Customers by Total Spend (RANK vs DENSE_RANK)
-- =============================================================================
-- Rank customers by total order amount.
-- If two customers have the same total, they should get the same rank.
-- RANK skips numbers after ties. DENSE_RANK does not.

-- Correct approach:
SELECT 
    customer_id,
    customer_name,
    SUM(order_amount) AS total_spent,
    RANK() OVER (ORDER BY SUM(order_amount) DESC) AS rank_rank,
    DENSE_RANK() OVER (ORDER BY SUM(order_amount) DESC) AS dense_rank_rank
FROM orders
GROUP BY customer_id, customer_name;

-- =============================================================================
-- PROBLEM 3: Running Total Per Customer
-- =============================================================================
-- Show each order plus the running total of spend per customer.

-- Solution:
SELECT 
    order_id,
    customer_id,
    customer_name,
    order_date,
    order_amount,
    SUM(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS UNBOUNDED PRECEDING
    ) AS running_total
FROM orders
ORDER BY customer_id, order_date;

-- =============================================================================
-- PROBLEM 4: Previous Order Amount (LAG)
-- =============================================================================
-- Show each order and the previous order amount for that customer.
-- Useful for detecting changes in spend behavior.

-- Solution:
SELECT 
    order_id,
    customer_id,
    customer_name,
    order_date,
    order_amount,
    LAG(order_amount, 1) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS prev_order_amount,
    CASE 
        WHEN order_amount > LAG(order_amount, 1) OVER (
            PARTITION BY customer_id ORDER BY order_date
        ) THEN 'INCREASED'
        WHEN order_amount < LAG(order_amount, 1) OVER (
            PARTITION BY customer_id ORDER BY order_date
        ) THEN 'DECREASED'
        ELSE 'FIRST_ORDER'
    END AS spend_change
FROM orders
ORDER BY customer_id, order_date;

-- =============================================================================
-- PROBLEM 5: Next Order Date (LEAD)
-- =============================================================================
-- Find the days between consecutive orders for each customer.

-- Solution:
SELECT
    order_id,
    customer_id,
    customer_name,
    order_date,
    LEAD(order_date, 1) OVER (
        PARTITION BY customer_id
        ORDER BY order_date
    ) AS next_order_date,
    -- PostgreSQL: subtract dates directly => difference in days
    (LEAD(order_date, 1) OVER (PARTITION BY customer_id ORDER BY order_date) - order_date)
        AS days_until_next_order
FROM orders
ORDER BY customer_id, order_date;

select order_id,customer_id,customer_name,order_date,order_amount,
lead(order_date,1) over(partition by customer_id order by order_date) as next_order_date,
case when 
	(lead(order_date,1) over(partition by customer_id order by order_date) - order_date) <= 7 Then 'Next order placed within 7 days'
when 
	(lead(order_date,1) over(partition by customer_id order by order_date) - order_date) > 7 
	and (lead(order_date,1) over(partition by customer_id order by order_date) - order_date) <= 14 Then 'Next order placed between 8-14 days'
when
	(lead(order_date,1) over(partition by customer_id order by order_date) - order_date) > 14
	and (lead(order_date,1) over(partition by customer_id order by order_date) - order_date) < 30 Then 'Next order placed between 15-30 days'
when lead(order_date,1) over(partition by customer_id order by order_date) is null then 'No future orders'
else 'Beyond 30 days' end as order_interval
from orders 
order by customer_id,order_date

-- =============================================================================
-- PROBLEM 6: First and Last Order Per Customer (FIRST_VALUE / LAST_VALUE)
-- =============================================================================
-- Show each order along with the customer's first order date and amount.

-- Solution:
SELECT 
    order_id,
    customer_id,
    customer_name,
    order_date,
    order_amount,
    FIRST_VALUE(order_date) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_order_date,
    FIRST_VALUE(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_order_amount
FROM orders
ORDER BY customer_id, order_date;

-- =============================================================================
-- PROBLEM 7: NTILE — Bucket Customers Into Quartiles
-- =============================================================================
-- Divide customers into 4 groups based on total spend.

-- Solution:
WITH customer_totals AS (
    SELECT 
        customer_id,
        customer_name,
        SUM(order_amount) AS total_spent
    FROM orders
    GROUP BY customer_id, customer_name
)
SELECT *,
       NTILE(4) OVER (ORDER BY total_spent DESC) AS spend_quartile
FROM customer_totals;
-- NTILE is basically  a way to assign quartiles (or any number of buckets) based on ordering.
-- It doesnt really matter what the value of total_spent is, just the relative order.
-- In this case, Bob and Pavan have the same total_spent of 630.00, but Bob is listed before Pavan in the result set, so Bob gets assigned to quartile 1 and Pavan gets assigned to quartile 2. 
-- If you want tied values to be in the same quartile, you would need to use a different approach, such as using RANK or DENSE_RANK to assign ranks first and then bucket based on those ranks.

101	"Alice"	1420.00	1
102	"Bob"	630.00	1
105	"Pavan"	630.00	2
103	"Charlie"	395.00	3
104	"Diana"	150.00	4

-- Because NTILE divides the ordered set into equal buckets. If there are ties in total_spent, it will still assign them to buckets based on their order in the result set. 


-- =============================================================================
-- PROBLEM 8: Advanced — Top 2 Products Per Customer by Spend
-- =============================================================================
-- For each customer, find their top 2 product categories by spend.

-- Solution:
WITH category_spend AS (
    SELECT 
        customer_id,
        customer_name,
        product_category,
        SUM(order_amount) AS category_spend
    FROM orders
    GROUP BY customer_id, customer_name, product_category
),
ranked_categories AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id 
               ORDER BY category_spend DESC
           ) AS rn
    FROM category_spend
)
SELECT customer_id, customer_name, product_category, category_spend
FROM ranked_categories
WHERE rn <= 2
ORDER BY customer_id, rn;

-- =============================================================================
-- PROBLEM 9: MEDIAN Spend Per Customer (PERCENTILE_CONT)
-- =============================================================================
-- Find the median order amount per customer.

-- Solution:
SELECT 
    customer_id,
    customer_name,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_amount) AS median_order_amount
FROM orders
GROUP BY customer_id, customer_name;

-- =============================================================================
-- PROBLEM 10: Moving Average (3-order window)
-- =============================================================================
-- 3-order moving average of order amount per customer.

-- Solution:
SELECT 
    order_id,
    customer_id,
    customer_name,
    order_date,
    order_amount,
    AVG(order_amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3
FROM orders
ORDER BY customer_id, order_date;

-- =============================================================================
-- RECURSIVE CTE: Employee Hierarchy
-- =============================================================================

CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    manager_id INT NULL
);

INSERT INTO employees VALUES
(1, 'CEO', NULL),
(2, 'VP Engineering', 1),
(3, 'VP Marketing', 1),
(4, 'Data Engineering Lead', 2),
(5, 'Senior Data Engineer', 4),
(6, 'Junior Data Engineer', 4),
(7, 'Marketing Manager', 3);

-- Find all direct and indirect reports under 'VP Engineering' (emp_id=2)
WITH RECURSIVE org_hierarchy AS (
    -- Anchor: start with VP Engineering
    SELECT emp_id, emp_name, manager_id, 0 AS level
    FROM employees
    WHERE emp_id = 2
    
    UNION ALL
    
    -- Recursive: find employees whose manager is in the previous level
    SELECT e.emp_id, e.emp_name, e.manager_id, oh.level + 1
    FROM employees e
    INNER JOIN org_hierarchy oh ON e.manager_id = oh.emp_id
)
SELECT emp_id, emp_name, level
FROM org_hierarchy
ORDER BY level, emp_name;

-- =============================================================================
-- CTE vs SUBQUERY vs TEMP TABLE
-- =============================================================================
-- Same result 3 ways — know the tradeoffs for interviews.

-- CTE (readable, good for single query)
WITH high_spenders AS (
    SELECT customer_id, SUM(order_amount) AS total
    FROM orders
    GROUP BY customer_id
    HAVING SUM(order_amount) > 500
)
SELECT o.*
FROM orders o
JOIN high_spenders hs ON o.customer_id = hs.customer_id;

-- Subquery (compact, harder to read when complex)
SELECT o.*
FROM orders o
JOIN (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING SUM(order_amount) > 500
) hs ON o.customer_id = hs.customer_id;

-- Temp Table (reuse across multiple queries, good for large data)
-- CREATE TEMP TABLE high_spenders AS
-- SELECT customer_id, SUM(order_amount) AS total
-- FROM orders
-- GROUP BY customer_id
-- HAVING SUM(order_amount) > 500;

-- =============================================================================
-- ANTI JOIN: Customers Who Never Ordered
-- =============================================================================

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100)
);

INSERT INTO customers VALUES
(101, 'Alice'),
(102, 'Bob'),
(103, 'Charlie'),
(104, 'Diana'),
(105, 'Eve'),    -- No orders
(106, 'Frank');  -- No orders

-- Find customers with NO orders (prefer this over NOT IN due to NULL handling)
SELECT c.*
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL;

-- NOT IN version (BEWARE: fails if subquery returns NULL)
SELECT *
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
-- If orders.customer_id has NULL, this returns empty result set!

-- Better: NOT EXISTS (handles NULL correctly)
SELECT *
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);