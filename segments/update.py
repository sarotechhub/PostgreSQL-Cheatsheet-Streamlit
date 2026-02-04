"""
Update Segment
Covers updating data in PostgreSQL tables.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the update segment."""
    layout = get_layout_manager()
    
    st.header("✏️ UPDATE Operations")
    
    layout.render_expandable_section(
        "📝 Basic Update",
        lambda: _render_basic_update(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Advanced Update",
        lambda: _render_advanced_update()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_basic_update() -> None:
    """Render basic update section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **UPDATE** statements modify existing data in tables:
    
    - **Single column update**: Change one field for rows matching criteria
    - **Multiple columns**: Update several fields at once
    - **WHERE clause**: Essential to specify which rows to update
    - **Update all rows**: Risky! Omit WHERE only if you mean to update everything
    - **CURRENT_TIMESTAMP**: Auto-set updated_at or modified timestamps
    - **RETURNING clause**: See what was changed
    - **FROM clause**: Update using data from another table/join
    """)
    
    layout.render_code_block("""
-- Update single column for matching rows
UPDATE users
SET is_active = FALSE
WHERE created_at < '2020-01-01';

-- Update multiple columns
UPDATE users
SET email = 'newemail@example.com',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- Update all rows
UPDATE products
SET discount_price = price * 0.9;

-- Update with WHERE clause
UPDATE orders
SET status = 'shipped'
WHERE id = 123;

-- Update with RETURNING
UPDATE users
SET is_active = TRUE
WHERE id = 5
RETURNING id, username, updated_at;

-- Update using FROM clause
UPDATE users u
SET last_login = CURRENT_TIMESTAMP
FROM login_history lh
WHERE u.id = lh.user_id
  AND lh.login_time = (
    SELECT MAX(login_time) FROM login_history WHERE user_id = u.id
  );
    """, title="SQL Examples")
    
    layout.render_tip("Always include WHERE clause to avoid updating all rows accidentally!")
    
    st.markdown("### 🏢 Real-World Example: Product Price Update After Discount")
    st.markdown("""
    **Scenario:** Running a 30% off sale on electronics category
    
    ```sql
    -- Update sale prices for all electronics
    UPDATE products
    SET 
        sale_price = price * 0.7,
        on_sale = TRUE,
        updated_at = CURRENT_TIMESTAMP
    WHERE category_id = 5  -- Electronics
      AND stock_level > 0
      AND is_active = TRUE
    RETURNING id, name, price, sale_price;
    
    -- RETURNING shows which products were updated for verification
    ```
    
    **Why this matters:** WHERE clause ensures only active products in the right category get updated. RETURNING verifies the sale price calculation worked correctly.
    """)


def _render_advanced_update() -> None:
    """Render advanced update section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Advanced UPDATE** techniques for complex modifications:
    
    - **Subquery in SET**: Use results from other queries
    - **CASE statements**: Conditional updates (different values for different rows)
    - **Window functions**: Update with rankings or row numbers
    - **Calculations**: Math operations on current values
    - **UPDATE with LIMIT**: Update only a batch using subquery
    - **Prepared statements**: Parameterized updates (safe, reusable)
    - **UPDATE with EXISTS**: Update when related data exists
    """)
    
    layout.render_code_block("""
-- Update with subquery
UPDATE users
SET total_posts = (
    SELECT COUNT(*) FROM posts WHERE user_id = users.id
)
WHERE id IN (SELECT DISTINCT user_id FROM posts);

-- Update with CASE statement
UPDATE users
SET tier = CASE 
    WHEN total_posts > 100 THEN 'gold'
    WHEN total_posts > 50 THEN 'silver'
    WHEN total_posts > 10 THEN 'bronze'
    ELSE 'basic'
END
WHERE total_posts > 0;

-- Update with window functions
UPDATE employees
SET salary_rank = ranked.rank
FROM (
    SELECT 
        id,
        ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE employees.id = ranked.id;

-- Update with calculation
UPDATE products
SET discount_price = price * (1 - discount_percent / 100.0),
    updated_at = CURRENT_TIMESTAMP
WHERE discount_percent > 0;

-- Update with LIMIT (non-standard, use subquery)
UPDATE orders
SET status = 'processing'
WHERE status = 'pending'
  AND id IN (
    SELECT id FROM orders 
    WHERE status = 'pending' 
    LIMIT 100
  );

-- Bulk update with prepared statement (application code)
PREPARE stmt (int, text) AS
UPDATE users SET email = $2 WHERE id = $1;

EXECUTE stmt(1, 'newmail@example.com');

-- Update with conflict handling (PostgreSQL 15+)
UPDATE users
SET last_login = CURRENT_TIMESTAMP
WHERE EXISTS (SELECT 1 FROM login_attempts WHERE user_id = users.id);
    """, title="SQL Examples")
    
    layout.render_warning("Test UPDATE statements with SELECT first to verify WHERE clause!")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Updating User Tier After Reaching Purchase Threshold")
    st.markdown("""
    **Scenario:** Promote users from 'Bronze' to 'Silver' tier when they spend $500
    
    ```sql
    -- Promote qualifying users based on total spending
    UPDATE users u
    SET 
        tier = CASE 
            WHEN order_total >= 2000 THEN 'gold'
            WHEN order_total >= 500 THEN 'silver'
            ELSE 'bronze'
        END,
        tier_updated_at = CURRENT_TIMESTAMP
    FROM (
        SELECT user_id, SUM(total) as order_total
        FROM orders
        WHERE status = 'completed'
        GROUP BY user_id
    ) stats
    WHERE u.id = stats.user_id
      AND u.tier != CASE WHEN stats.order_total >= 2000 THEN 'gold' WHEN stats.order_total >= 500 THEN 'silver' ELSE 'bronze' END;
    ```
    
    **Why this matters:** Uses CASE for tiered logic and calculates from related orders table, automating loyalty rewards without manual intervention.
    """)
    
    tips = [
        "ALWAYS test UPDATE with SELECT first to verify WHERE conditions",
        "Use RETURNING clause to verify update results",
        "Wrap updates in transactions for data consistency",
        "Update timestamps (updated_at) when modifying records",
        "Consider write performance when updating large tables",
        "Use CASE statements for conditional updates",
        "Test WHERE conditions thoroughly to avoid unintended updates",
        "Use FROM clause to join with other tables for complex updates",
        "Monitor UPDATE performance with EXPLAIN ANALYZE",
        "Create backup before bulk updates to production data"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
