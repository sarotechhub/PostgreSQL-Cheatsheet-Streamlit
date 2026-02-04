"""
View Management Segment
Covers creating and managing views in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the view segment."""
    layout = get_layout_manager()
    
    st.header("👁️ Views")
    
    layout.render_expandable_section(
        "📝 Create View",
        lambda: _render_create_view(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "✏️ Alter View",
        lambda: _render_alter_view()
    )
    
    layout.render_expandable_section(
        "🔍 List Views",
        lambda: _render_list_views()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_view() -> None:
    """Render create view section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Views** are saved queries that act like virtual tables:
    
    - **Simple view**: SELECT from one table with filtering
    - **Complex view**: JOINs, aggregations, and multiple tables
    - **CREATE OR REPLACE**: Update existing view (same structure)
    - **Temporary view**: Session-only views (auto-deleted at disconnect)
    - **Materialized view**: Pre-computed results stored as physical data
    - **Security barrier**: Prevents subquery attacks (row-level security)
    - **Regular vs materialized**: Regular = computed on query, materialized = pre-computed
    """)
    
    layout.render_code_block("""
-- Simple view
CREATE VIEW active_users AS
SELECT id, username, email 
FROM users 
WHERE is_active = TRUE;

-- Create or replace view
CREATE OR REPLACE VIEW active_users AS
SELECT id, username, email, created_at
FROM users 
WHERE is_active = TRUE;

-- View with join
CREATE VIEW user_post_count AS
SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username;

-- View with complex logic
CREATE VIEW recent_posts AS
SELECT 
    p.id,
    p.title,
    u.username,
    p.created_at,
    p.published
FROM posts p
JOIN users u ON p.user_id = u.id
WHERE p.created_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY p.created_at DESC;

-- Create temporary view
CREATE TEMP VIEW temp_calculation AS
SELECT 
    SUM(amount) as total,
    AVG(amount) as average
FROM transactions;

-- View with security barrier
CREATE VIEW public_posts WITH (security_barrier) AS
SELECT id, title, content, created_at 
FROM posts 
WHERE published = TRUE;
    """, title="SQL Examples")
    
    layout.render_tip("Use views to simplify complex queries and hide table structure")


def _render_alter_view() -> None:
    """Render alter view section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Rename view
ALTER VIEW active_users 
RENAME TO active_user_list;

-- Change view owner
ALTER VIEW active_users 
OWNER TO new_owner;

-- Set schema
ALTER VIEW active_users 
SET SCHEMA public;

-- Drop view
DROP VIEW active_users;

-- Drop view if exists
DROP VIEW IF EXISTS active_users;

-- Drop view and dependents
DROP VIEW active_users CASCADE;

-- Redefine view (replace definition)
CREATE OR REPLACE VIEW active_users AS
SELECT id, username, email, is_active, created_at
FROM users 
WHERE is_active = TRUE;
    """, title="SQL Examples")


def _render_list_views() -> None:
    """Render list views section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- List all views (psql)
\\dv

-- List views in specific schema
\\dv schema_name.*

-- Query system catalog
SELECT 
    schemaname,
    viewname,
    viewowner
FROM pg_views
WHERE schemaname NOT IN ('pg_catalog', 'information_schema');

-- View definition
SELECT definition 
FROM pg_views 
WHERE viewname = 'active_users';

-- More details with psql
\\d+ view_name

-- Find views depending on a table
SELECT 
    definition,
    viewname
FROM pg_views
WHERE definition LIKE '%users%';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Simplify Dashboard Queries with Views")
    st.markdown("""
    **Scenario:** Dashboard needs active users with their order stats
    
    ```sql
    -- Create view that hides complexity from dashboard
    CREATE VIEW dashboard_user_stats AS
    SELECT 
        u.id,
        u.username,
        u.email,
        COUNT(o.id) as total_orders,
        SUM(o.total_amount) as lifetime_value,
        MAX(o.order_date) as last_order_date,
        AVG(o.total_amount) as avg_order_value
    FROM users u
    LEFT JOIN orders o ON u.id = o.customer_id
    WHERE u.is_active = TRUE
      AND u.deleted_at IS NULL
    GROUP BY u.id, u.username, u.email;
    
    -- Dashboard just does simple query (views hide complexity)
    SELECT * FROM dashboard_user_stats 
    ORDER BY lifetime_value DESC;
    ```
    
    **Why this matters:** Dashboard developers don't need to know about JOIN/GROUP BY/WHERE logic. If business rules change (e.g., exclude test users), you update the view once - all dashboards benefit!
    """)
    
    tips = [
        "Use views to abstract complex queries",
        "Name views descriptively (e.g., active_users, recent_orders)",
        "Keep view logic simple and readable",
        "Document the purpose of views in comments",
        "Use CREATE OR REPLACE for iterative development",
        "Consider performance impact of view definitions",
        "Views don't improve query performance - they're for convenience",
        "Use materialized views for complex, slow queries",
        "Limit view access with appropriate permissions",
        "Remember views are dynamic - they always show current data"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
