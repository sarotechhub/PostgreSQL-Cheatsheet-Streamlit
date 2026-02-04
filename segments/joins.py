"""
Joins Segment
Covers JOIN operations in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the joins segment."""
    layout = get_layout_manager()
    
    st.header("🔗 Joins")
    
    layout.render_expandable_section(
        "📝 Join Types",
        lambda: _render_join_types(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Complex Joins",
        lambda: _render_complex_joins()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_join_types() -> None:
    """Render join types section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **JOIN Types** combine data from multiple tables based on relationships:
    
    - **INNER JOIN**: Returns only rows where join condition matches in BOTH tables
    - **LEFT JOIN**: Returns all rows from left table + matching rows from right
    - **RIGHT JOIN**: Returns all rows from right table + matching rows from left
    - **FULL OUTER JOIN**: Returns all rows from both tables (matching + non-matching)
    - **CROSS JOIN**: Cartesian product - combines every row with every other row
    - **Self Join**: Join a table to itself (useful for hierarchical data)
    - **Multiple Joins**: Combine more than 2 tables in one query
    """)
    
    layout.render_code_block("""
-- INNER JOIN - only matching rows from both tables
SELECT 
    u.id,
    u.username,
    p.title,
    p.created_at
FROM users u
INNER JOIN posts p ON u.id = p.user_id;

-- LEFT JOIN - all from left, matching from right
SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username;

-- RIGHT JOIN - all from right, matching from left
SELECT 
    u.id,
    u.username,
    c.comment
FROM users u
RIGHT JOIN comments c ON u.id = c.user_id;

-- FULL OUTER JOIN - all from both tables
SELECT 
    COALESCE(u.id, c.user_id) as user_id,
    u.username,
    c.comment
FROM users u
FULL OUTER JOIN comments c ON u.id = c.user_id;

-- CROSS JOIN - Cartesian product
SELECT 
    u.username,
    c.color
FROM users u
CROSS JOIN colors c
LIMIT 10;

-- Self join
SELECT 
    e1.id,
    e1.name,
    e2.name as manager_name
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;

-- Join with WHERE filter
SELECT 
    u.username,
    p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id
WHERE p.created_at > '2024-01-01';
    """, title="SQL Examples")
    
    layout.render_tip("Use INNER JOIN when you only need matching rows, LEFT JOIN to keep all from left table")


def _render_complex_joins() -> None:
    """Render complex joins section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Multiple joins
SELECT 
    u.username,
    p.title,
    c.comment
FROM users u
INNER JOIN posts p ON u.id = p.user_id
LEFT JOIN comments c ON p.id = c.post_id;

-- Join on multiple conditions
SELECT 
    o.id,
    c.name,
    p.name
FROM orders o
INNER JOIN customers c 
    ON o.customer_id = c.id 
    AND o.status = 'active'
INNER JOIN products p ON o.product_id = p.id;

-- Join with aggregate
SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count,
    AVG(LENGTH(p.content)) as avg_post_length
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username;

-- Join with window function
SELECT 
    u.username,
    p.title,
    ROW_NUMBER() OVER (PARTITION BY u.id ORDER BY p.created_at DESC) as post_rank
FROM users u
INNER JOIN posts p ON u.id = p.user_id;

-- Join with subquery
SELECT 
    u.username,
    recent_posts.count as recent_post_count
FROM users u
LEFT JOIN (
    SELECT user_id, COUNT(*) as count 
    FROM posts 
    WHERE created_at > CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
) recent_posts ON u.id = recent_posts.user_id;

-- Natural join (join on columns with same name)
SELECT *
FROM users
NATURAL JOIN user_profiles;

-- Join with USING clause
SELECT 
    u.id,
    u.username,
    p.title
FROM users u
INNER JOIN posts p USING (id);  -- Assumes same column name
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Order Report with Customer and Product Info")
    st.markdown("""
    **Scenario:** Generate monthly sales report showing customer names, product names, and amounts
    
    ```sql
    -- Get complete order information across 3 tables
    SELECT 
        o.id as order_id,
        c.name as customer_name,
        c.email,
        p.name as product_name,
        p.category,
        oi.quantity,
        oi.unit_price,
        (oi.quantity * oi.unit_price) as line_total,
        o.order_date
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.id
    INNER JOIN order_items oi ON o.id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.id
    WHERE o.order_date >= CURRENT_DATE - INTERVAL '1 month'
    ORDER BY o.order_date DESC;
    ```
    
    **Why this matters:** Without JOINS, you'd need to manually fetch customers and products for each order in your code. JOINS do this efficiently in one query!
    """)
    
    tips = [
        "Use explicit JOIN syntax instead of comma-separated tables",
        "Use INNER JOIN when you need only matching rows",
        "Use LEFT JOIN to preserve rows from the left table",
        "Index foreign key columns for better join performance",
        "Avoid unnecessary joins to improve query performance",
        "Use EXPLAIN ANALYZE to understand join performance",
        "Filter early with WHERE to reduce data before join",
        "Use aliases for table names to make queries readable",
        "Join on primary/foreign keys for data integrity",
        "Be careful with LEFT JOIN combined with WHERE - can turn into INNER JOIN"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
