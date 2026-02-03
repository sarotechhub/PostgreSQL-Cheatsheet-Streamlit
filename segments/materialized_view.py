"""
Materialized View Segment
Covers creating and managing materialized views in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the materialized view segment."""
    layout = get_layout_manager()
    
    st.header("📦 Materialized Views")
    
    layout.render_expandable_section(
        "📝 Create Materialized View",
        lambda: _render_create_materialized_view(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "🔄 Refresh View",
        lambda: _render_refresh_view()
    )
    
    layout.render_expandable_section(
        "🗑️ Drop Materialized View",
        lambda: _render_drop_materialized_view()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_materialized_view() -> None:
    """Render create materialized view section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Basic materialized view
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count,
    MAX(p.created_at) as last_post_date
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username;

-- Materialized view with data
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    COUNT(p.id) as post_count,
    COUNT(c.id) as comment_count,
    MAX(p.created_at) as last_post_date
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
LEFT JOIN comments c ON c.user_id = u.id
GROUP BY u.id, u.username;

-- Create with data
CREATE MATERIALIZED VIEW IF NOT EXISTS user_stats AS
SELECT 
    u.id,
    u.username,
    COUNT(DISTINCT p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username
WITH DATA;

-- Create without data (for later population)
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    0 as post_count
FROM users u
WITH NO DATA;
    """, title="SQL Examples")
    
    layout.render_tip("Materialized views store query results - perfect for heavy computations")


def _render_refresh_view() -> None:
    """Render refresh view section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Refresh materialized view (full refresh)
REFRESH MATERIALIZED VIEW user_stats;

-- Refresh without locking (PostgreSQL 9.5+)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;

-- Create index for concurrent refresh
CREATE UNIQUE INDEX user_stats_id 
ON user_stats(id);

-- Then refresh concurrently
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;

-- Conditional refresh based on schedule
-- Create table for refresh tracking
CREATE TABLE materialized_view_refresh_log (
    view_name TEXT PRIMARY KEY,
    last_refresh TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    refresh_interval INTERVAL DEFAULT '1 hour'
);

-- Insert initial entry
INSERT INTO materialized_view_refresh_log 
VALUES ('user_stats', CURRENT_TIMESTAMP, '1 hour');

-- Check if refresh needed
SELECT view_name 
FROM materialized_view_refresh_log 
WHERE last_refresh < CURRENT_TIMESTAMP - refresh_interval;
    """, title="SQL Examples")
    
    layout.render_warning("REFRESH MATERIALIZED VIEW locks the view - plan accordingly!")


def _render_drop_materialized_view() -> None:
    """Render drop materialized view section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Drop materialized view
DROP MATERIALIZED VIEW user_stats;

-- Drop if exists
DROP MATERIALIZED VIEW IF EXISTS user_stats;

-- Drop with cascade
DROP MATERIALIZED VIEW user_stats CASCADE;

-- List all materialized views
SELECT matviewname 
FROM pg_matviews;

-- View definition
SELECT definition 
FROM pg_matviews 
WHERE matviewname = 'user_stats';

-- Check indexes on materialized view
SELECT 
    schemaname,
    matviewname,
    indexname
FROM pg_indexes
WHERE matviewname = 'user_stats';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Use materialized views for expensive, frequently-accessed queries",
        "Create indexes on materialized views for better query performance",
        "Use REFRESH CONCURRENTLY for zero-downtime updates (requires unique index)",
        "Schedule regular refreshes using cron or pg_cron extension",
        "Monitor disk space - materialized views take storage",
        "Document refresh frequency and timing",
        "Test refresh performance before deploying to production",
        "Consider staleness requirements when planning refresh intervals",
        "Use WITH NO DATA for large views, populate on demand",
        "Materialized views don't auto-refresh - you must refresh manually"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
