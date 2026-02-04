"""
Select Segment
Covers querying data with SELECT statements in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the select segment."""
    layout = get_layout_manager()
    
    st.header("🔍 SELECT Queries")
    
    layout.render_expandable_section(
        "📝 Basic SELECT",
        lambda: _render_basic_select(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Filtering & Sorting",
        lambda: _render_filtering_sorting()
    )
    
    layout.render_expandable_section(
        "📝 Advanced SELECT",
        lambda: _render_advanced_select()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_basic_select() -> None:
    """Render basic select section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **SELECT** statements are used to retrieve data from tables. Here are the basic patterns you'll use:
    
    - **SELECT all columns** (*): Retrieves every column from a table
    - **SELECT specific columns**: Retrieves only the columns you need (more efficient)
    - **Column aliases (AS)**: Rename columns for better readability in results
    - **Expressions**: Use functions like UPPER(), LENGTH() to transform data
    - **LIMIT**: Control how many rows you retrieve
    - **OFFSET**: Skip rows for pagination (LIMIT with OFFSET)
    - **DISTINCT**: Get unique values, removing duplicates
    - **COUNT()**: Count the number of rows matching your criteria
    """)
    
    layout.render_code_block("""
-- Select all columns
SELECT * FROM users;

-- Select specific columns
SELECT id, username, email FROM users;

-- Select with alias
SELECT 
    id as user_id,
    username as user_name,
    email as user_email
FROM users;

-- Select with expression
SELECT 
    id,
    username,
    UPPER(username) as username_upper,
    LENGTH(email) as email_length
FROM users;

-- Select with LIMIT
SELECT * FROM users LIMIT 10;

-- Select with OFFSET (pagination)
SELECT * FROM users LIMIT 10 OFFSET 20;  -- Skip first 20, get next 10

-- Select distinct values
SELECT DISTINCT email FROM users;

-- Count rows
SELECT COUNT(*) as total_users FROM users;

-- Select with column renaming
SELECT username AS name, email AS contact FROM users;
    """, title="SQL Examples")
    
    layout.render_tip("Specify columns instead of SELECT * for better performance and clarity")
    
    st.markdown("### 🏢 Real-World Example: E-Commerce Product Listing")
    st.markdown("""
    **Scenario:** Display products on your online store with pagination
    
    ```sql
    -- Users see 20 products per page, browsing different pages
    SELECT id, name, price, category, stock_level
    FROM products
    WHERE is_active = TRUE
      AND stock_level > 0
    ORDER BY popularity DESC
    LIMIT 20 OFFSET 0;  -- Page 1
    
    LIMIT 20 OFFSET 20;  -- Page 2
    LIMIT 20 OFFSET 40;  -- Page 3
    ```
    
    **Why this matters:** Pagination prevents loading thousands of products at once, improving page load speed and user experience.
    """)


def _render_filtering_sorting() -> None:
    """Render filtering and sorting section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Filtering & Sorting** helps you narrow down results and organize them:
    
    - **WHERE**: Filter rows based on conditions
    - **AND/OR**: Combine multiple conditions (AND = all must be true, OR = at least one true)
    - **IN**: Check if a value exists in a list
    - **BETWEEN**: Find values within a range
    - **LIKE / ILIKE**: Pattern matching (% = any characters, _ = single character)
    - **IS NULL / IS NOT NULL**: Check for missing values
    - **ORDER BY**: Sort results (ASC = ascending, DESC = descending)
    - **NULL handling in ORDER BY**: Control how NULL values are sorted
    """)
    
    layout.render_code_block("""
-- WHERE clause - filter by conditions
SELECT * FROM users WHERE is_active = TRUE;

-- Multiple conditions with AND
SELECT * FROM orders 
WHERE status = 'completed' 
  AND total > 100
  AND created_at > '2024-01-01';

-- Multiple conditions with OR
SELECT * FROM products 
WHERE category = 'electronics'
   OR category = 'appliances';

-- IN operator
SELECT * FROM users WHERE id IN (1, 2, 3, 4, 5);

-- BETWEEN operator
SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- LIKE pattern matching
SELECT * FROM users WHERE username LIKE 'john%';
SELECT * FROM users WHERE email ILIKE '%gmail.com';  -- Case insensitive

-- NOT NULL check
SELECT * FROM users WHERE phone IS NOT NULL;

-- ORDER BY - sort results
SELECT * FROM users ORDER BY created_at DESC;

-- ORDER BY multiple columns
SELECT * FROM users ORDER BY last_name, first_name;

-- ORDER BY with NULL handling
SELECT * FROM users 
ORDER BY phone IS NOT NULL DESC, phone;  -- Non-null values first

-- LIMIT with ORDER BY (top N)
SELECT * FROM products 
ORDER BY price DESC 
LIMIT 10;  -- Top 10 most expensive
    """, title="SQL Examples")
    
    st.markdown("### 🏢 Real-World Example: Finding Inactive Users to Delete")
    st.markdown("""
    **Scenario:** You need to clean up inactive accounts from the database
    
    ```sql
    -- Find inactive users (no login for 12 months) for cleanup
    SELECT id, username, email, last_login
    FROM users
    WHERE last_login < CURRENT_DATE - INTERVAL '1 year'
       OR (last_login IS NULL AND created_at < CURRENT_DATE - INTERVAL '2 years')
    ORDER BY last_login DESC
    LIMIT 1000;
    ```
    
    **Why this matters:** GDPR compliance requires removing old inactive accounts; filtering first ensures you delete the right users.
    """)


def _render_advanced_select() -> None:
    """Render advanced select section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Advanced SELECT** techniques for complex queries:
    
    - **CASE statements**: Conditional logic (if-then-else for data) to categorize rows
    - **GROUP BY**: Aggregate data by categories (combine with COUNT, SUM, AVG, etc.)
    - **HAVING**: Filter groups after aggregation (like WHERE but for GROUP BY)
    - **Window Functions**: Calculate values across sets of rows (ranking, running totals, etc.)
    - **CTEs (WITH)**: Temporary named result sets for cleaner, more readable queries
    - **Recursive CTEs**: Self-referencing queries for hierarchical data
    - **UNION**: Combine results from multiple queries (removes duplicates)
    - **EXCEPT**: Find rows in first query but not in second
    - **INTERSECT**: Find rows that appear in both queries
    """)
    
    layout.render_code_block("""
-- CASE statement - conditional selection
SELECT 
    id,
    username,
    CASE 
        WHEN total_posts > 100 THEN 'power_user'
        WHEN total_posts > 10 THEN 'active_user'
        ELSE 'new_user'
    END as user_type
FROM users;

-- GROUP BY - aggregate by category
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    MAX(price) as max_price
FROM products
GROUP BY category;

-- HAVING - filter groups
SELECT 
    user_id,
    COUNT(*) as post_count
FROM posts
GROUP BY user_id
HAVING COUNT(*) > 10;

-- Window functions - calculate over rows
SELECT 
    id,
    username,
    post_count,
    ROW_NUMBER() OVER (ORDER BY post_count DESC) as rank
FROM users;

-- CTE (Common Table Expression) - temporary result set
WITH active_users AS (
    SELECT * FROM users WHERE is_active = TRUE
)
SELECT * FROM active_users WHERE created_at > '2024-01-01';

-- Recursive CTE
WITH RECURSIVE numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;

-- UNION - combine results
SELECT username FROM users WHERE is_active = TRUE
UNION
SELECT bot_name FROM bots;

-- EXCEPT - difference between result sets
SELECT id FROM all_users
EXCEPT
SELECT id FROM deactivated_users;

-- INTERSECT - common rows
SELECT id FROM users
INTERSECT
SELECT user_id FROM orders;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Finding Customers Who Never Made a Purchase")
    st.markdown("""
    **Scenario:** Marketing team wants to re-engage registered users who haven't ordered
    
    ```sql
    -- Find users registered but never placed an order
    SELECT id, email, username, created_at
    FROM users
    WHERE id NOT IN (
        SELECT DISTINCT user_id FROM orders
    )
      AND created_at < CURRENT_DATE - INTERVAL '30 days'
    ORDER BY created_at DESC;
    ```
    
    **Why this matters:** Identify dormant users for re-engagement campaigns without scanning millions of order records individually.
    """)
    
    tips = [
        "Select only needed columns instead of SELECT *",
        "Use WHERE to filter early and reduce data processed",
        "Add indexes on columns used in WHERE clauses",
        "Use LIMIT for pagination instead of loading all data",
        "Use CTEs for complex queries with multiple steps",
        "Use EXPLAIN ANALYZE to understand query performance",
        "Avoid N+1 query problems - use joins instead",
        "Use DISTINCT sparingly as it requires sorting",
        "Window functions are powerful but can be slow on large datasets",
        "Test complex queries with EXPLAIN before production use"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
