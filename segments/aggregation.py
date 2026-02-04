"""
Aggregation Segment
Covers aggregate functions and grouping in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the aggregation segment."""
    layout = get_layout_manager()
    
    st.header("📊 Aggregations & Window Functions")
    
    layout.render_expandable_section(
        "📝 Aggregate Functions",
        lambda: _render_aggregate_functions(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Window Functions",
        lambda: _render_window_functions()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_aggregate_functions() -> None:
    """Render aggregate functions section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Aggregate Functions** combine multiple rows into summary results:
    
    - **COUNT()**: Counts rows (or non-NULL values in column)
    - **SUM()**: Adds up numeric values
    - **AVG()**: Calculates average value
    - **MIN() / MAX()**: Finds minimum or maximum value
    - **STRING_AGG()**: Concatenates string values
    - **ARRAY_AGG()**: Combines values into array
    - **GROUP BY**: Groups data for aggregation
    - **FILTER clause**: Conditional aggregation (count IF)
    - **DISTINCT in aggregate**: Count/sum unique values only
    """)
    
    layout.render_code_block("""
-- COUNT - count rows
SELECT COUNT(*) as total_users FROM users;
SELECT COUNT(DISTINCT email) as unique_emails FROM users;

-- SUM - sum values
SELECT SUM(amount) as total_revenue FROM orders;
SELECT SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) as paid_revenue FROM orders;

-- AVG - average value
SELECT AVG(price) as avg_price FROM products;
SELECT AVG(CAST(rating AS DECIMAL)) as avg_rating FROM reviews;

-- MIN/MAX - minimum/maximum value
SELECT MIN(created_at) as oldest_user, MAX(created_at) as newest_user FROM users;
SELECT MIN(price) as cheapest, MAX(price) as most_expensive FROM products;

-- STRING_AGG - aggregate strings (comma-separated)
SELECT 
    user_id,
    STRING_AGG(tag, ', ') as tags
FROM post_tags
GROUP BY user_id;

-- ARRAY_AGG - aggregate into array
SELECT 
    user_id,
    ARRAY_AGG(tag) as tag_array
FROM post_tags
GROUP BY user_id;

-- GROUP BY - group rows by category
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price
FROM products
GROUP BY category;

-- GROUP BY multiple columns
SELECT 
    country,
    state,
    COUNT(*) as user_count
FROM users
GROUP BY country, state;

-- HAVING - filter groups
SELECT 
    category,
    COUNT(*) as product_count
FROM products
GROUP BY category
HAVING COUNT(*) > 5;
    """, title="SQL Examples")
    
    layout.render_tip("Use GROUP BY with aggregate functions to summarize data by categories")


def _render_window_functions() -> None:
    """Render window functions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- ROW_NUMBER - sequential row number
SELECT 
    username,
    post_count,
    ROW_NUMBER() OVER (ORDER BY post_count DESC) as rank
FROM users;

-- RANK - rank with ties
SELECT 
    username,
    score,
    RANK() OVER (ORDER BY score DESC) as rank
FROM leaderboard;

-- DENSE_RANK - rank without gaps
SELECT 
    username,
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) as rank
FROM leaderboard;

-- LAG/LEAD - access previous/next row
SELECT 
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) as prev_revenue,
    LEAD(revenue) OVER (ORDER BY date) as next_revenue
FROM daily_sales;

-- Running total with SUM window function
SELECT 
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- PARTITION BY - window functions per group
SELECT 
    username,
    post_date,
    ROW_NUMBER() OVER (PARTITION BY username ORDER BY post_date DESC) as post_num_for_user
FROM posts;

-- FIRST_VALUE/LAST_VALUE - first/last value in window
SELECT 
    department,
    salary,
    FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) as max_salary_in_dept,
    LAST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as min_salary_in_dept
FROM employees;

-- NTILE - divide into quantiles
SELECT 
    username,
    post_count,
    NTILE(4) OVER (ORDER BY post_count) as quartile
FROM users;

-- PERCENT_RANK
SELECT 
    username,
    score,
    PERCENT_RANK() OVER (ORDER BY score) as percentile
FROM leaderboard;
    """, title="SQL Examples")
    
    layout.render_tip("Window functions are powerful for calculating rankings, running totals, and row comparisons")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Monthly Sales Report with Rankings")
    st.markdown("""
    **Scenario:** Show sales performance across regions with rankings
    
    ```sql
    SELECT 
        EXTRACT(MONTH FROM order_date) as month,
        region,
        SUM(total) as monthly_sales,
        COUNT(DISTINCT customer_id) as customers,
        AVG(total) as avg_order_value,
        
        -- Ranking this region's sales against all others
        RANK() OVER (PARTITION BY EXTRACT(MONTH FROM order_date) ORDER BY SUM(total) DESC) as region_rank,
        
        -- Month-over-month comparison
        LAG(SUM(total)) OVER (PARTITION BY region ORDER BY EXTRACT(MONTH FROM order_date)) as prev_month_sales,
        
        -- Running annual total
        SUM(SUM(total)) OVER (PARTITION BY region ORDER BY EXTRACT(MONTH FROM order_date)) as ytd_sales
        
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date) = 2025
    GROUP BY month, region;
    
    -- Result: Top performers highlighted, trends visible at a glance!
    ```
    
    **Why this matters:** Window functions let you calculate rankings and trends without complex application code. Compare regions, months, and rolling totals in one query.
    """)
    
    tips = [
        "Use COUNT(DISTINCT column) for counting unique values",
        "Remember to include non-aggregated columns in GROUP BY",
        "Use HAVING to filter groups, WHERE to filter rows",
        "Window functions run after GROUP BY - understand their scope",
        "Use PARTITION BY to apply window functions to subsets",
        "Order window functions with ORDER BY for consistent results",
        "Use STRING_AGG to aggregate text into comma-separated lists",
        "ARRAY_AGG aggregates values into arrays for flexibility",
        "Test aggregate queries with sample data first",
        "Monitor performance of aggregates on large tables with EXPLAIN ANALYZE"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
