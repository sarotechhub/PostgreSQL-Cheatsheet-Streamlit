"""
Insert Segment
Covers inserting data into PostgreSQL tables.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the insert segment."""
    layout = get_layout_manager()
    
    st.header("➕ INSERT Operations")
    
    layout.render_expandable_section(
        "📝 Basic Insert",
        lambda: _render_basic_insert(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Advanced Insert",
        lambda: _render_advanced_insert()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_basic_insert() -> None:
    """Render basic insert section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Single row insert
INSERT INTO users (username, email)
VALUES ('john_doe', 'john@example.com');

-- Insert with all columns
INSERT INTO users (id, username, email, is_active)
VALUES (1, 'jane_doe', 'jane@example.com', TRUE);

-- Insert without specifying columns (must provide all)
INSERT INTO users
VALUES (2, 'bob_smith', 'bob@example.com', TRUE, CURRENT_TIMESTAMP);

-- Insert with default values
INSERT INTO users (username, email)
VALUES ('alice', 'alice@example.com');
-- Other columns use DEFAULT values

-- Insert multiple rows
INSERT INTO users (username, email) VALUES
('user1', 'user1@example.com'),
('user2', 'user2@example.com'),
('user3', 'user3@example.com');

-- Insert from SELECT
INSERT INTO users_backup
SELECT * FROM users WHERE created_at < '2020-01-01';

-- Insert with RETURNING clause
INSERT INTO users (username, email)
VALUES ('david', 'david@example.com')
RETURNING id, username, created_at;
    """, title="SQL Examples")
    
    layout.render_tip("Use RETURNING to get back generated IDs and timestamps")


def _render_advanced_insert() -> None:
    """Render advanced insert section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- INSERT ... ON CONFLICT (upsert)
INSERT INTO users (username, email) 
VALUES ('john', 'john@example.com')
ON CONFLICT (username) 
DO UPDATE SET email = 'john_new@example.com';

-- ON CONFLICT with multiple columns
INSERT INTO user_roles (user_id, role_id) 
VALUES (1, 1)
ON CONFLICT (user_id, role_id)
DO NOTHING;

-- Bulk insert with ON CONFLICT
INSERT INTO users (username, email) VALUES
('user1', 'user1@example.com'),
('user2', 'user2@example.com')
ON CONFLICT (username)
DO UPDATE SET 
    email = EXCLUDED.email,
    updated_at = CURRENT_TIMESTAMP;

-- Insert with expressions
INSERT INTO products (name, price, discount_price) 
VALUES ('Widget', 100.00, 100.00 * 0.9);

-- Conditional insert
INSERT INTO temp_table (col1, col2)
SELECT col1, col2 FROM source_table 
WHERE col1 > 100
  AND created_at > NOW() - INTERVAL '7 days';

-- Insert with window functions
INSERT INTO user_ranks (user_id, rank)
SELECT 
    user_id,
    ROW_NUMBER() OVER (ORDER BY total_posts DESC)
FROM user_stats;

-- Bulk insert performance (batch mode)
-- Wrap multiple inserts in a transaction
BEGIN;
INSERT INTO large_table VALUES (...);
INSERT INTO large_table VALUES (...);
-- ... more inserts
COMMIT;
    """, title="SQL Examples")
    
    layout.render_warning("ON CONFLICT DO UPDATE can have performance implications with large datasets")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Always specify column names in INSERT statements (avoid relying on column order)",
        "Use RETURNING clause to verify inserted data and get auto-generated values",
        "Use bulk inserts for multiple rows (wrap in transaction)",
        "Use ON CONFLICT for upsert operations instead of checking then inserting",
        "Validate data at application level before inserting",
        "Check for constraint violations before insert to provide better error messages",
        "Use transactions for related multi-table inserts",
        "Monitor INSERT performance with EXPLAIN ANALYZE",
        "Use COPY for very large bulk imports (much faster than INSERT)",
        "Remember that DEFAULT values execute at insert time, not table creation"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
