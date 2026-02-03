"""
Monitoring Segment
Covers monitoring PostgreSQL performance and activity.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the monitoring segment."""
    layout = get_layout_manager()
    
    st.header("📊 Monitoring")
    
    layout.render_expandable_section(
        "📝 Activity Monitoring",
        lambda: _render_activity_monitoring(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Performance Monitoring",
        lambda: _render_performance_monitoring()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_activity_monitoring() -> None:
    """Render activity monitoring section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- List active connections
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Find long-running queries
SELECT 
    pid,
    usename,
    query,
    query_start,
    state_change,
    (NOW() - query_start) as duration
FROM pg_stat_activity
WHERE state != 'idle'
  AND query NOT LIKE '%pg_stat_activity%'
ORDER BY duration DESC;

-- Find idle connections
SELECT 
    pid,
    usename,
    state,
    (NOW() - state_change) as idle_time
FROM pg_stat_activity
WHERE state = 'idle'
  AND query_start < NOW() - INTERVAL '30 minutes'
ORDER BY idle_time DESC;

-- Kill a session
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid = <pid_number>;

-- Kill all connections to database
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'dbname'
  AND pid <> pg_backend_pid();

-- View connection information
SELECT 
    datname,
    count(*) as connection_count
FROM pg_stat_activity
GROUP BY datname
ORDER BY connection_count DESC;

-- Blocking queries
SELECT 
    blocking.pid as blocking_pid,
    blocking.usename as blocking_user,
    blocking.query as blocking_query,
    blocked.pid as blocked_pid,
    blocked.usename as blocked_user,
    blocked.query as blocked_query
FROM pg_stat_activity blocking
JOIN pg_stat_activity blocked ON blocking.locktype IS NOT NULL
    AND blocking.relation IS NOT DISTINCT FROM blocked.relation
    AND blocking.page IS NOT DISTINCT FROM blocked.page
    AND blocking.tuple IS NOT DISTINCT FROM blocked.tuple
    AND blocking.pid != blocked.pid;
    """, title="SQL Examples")
    
    layout.render_tip("Use pg_stat_activity to monitor current database activity")


def _render_performance_monitoring() -> None:
    """Render performance monitoring section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Enable query statistics
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Most expensive queries
SELECT 
    query,
    calls,
    mean_time,
    total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Most frequently called queries
SELECT 
    query,
    calls,
    mean_time
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 10;

-- Slowest total time
SELECT 
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Database size
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- Table size
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;

-- Table bloat (dead rows)
SELECT 
    schemaname,
    tablename,
    n_live_tup,
    n_dead_tup,
    ROUND(100 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_live_tup > 0
ORDER BY n_dead_tup DESC;

-- Index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Cache hit ratio
SELECT 
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;

-- Reset statistics
SELECT pg_stat_statements_reset();
SELECT pg_stat_reset();
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Enable pg_stat_statements to track query performance",
        "Monitor connection count to detect connection leaks",
        "Set up alerts for long-running queries",
        "Regularly check for unused indexes to save space",
        "Monitor table bloat and schedule VACUUM",
        "Track cache hit ratio - below 99% suggests missing indexes",
        "Monitor disk space regularly",
        "Set statement_timeout to kill runaway queries",
        "Use log_min_duration_statement to log slow queries",
        "Implement centralized monitoring with tools like pgAdmin or custom scripts"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
