"""
Index Management Segment
Covers creating and managing indexes in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the index segment."""
    layout = get_layout_manager()
    
    st.header("⚡ Indexes")
    
    layout.render_expandable_section(
        "📝 Create Index",
        lambda: _render_create_index(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "🔍 Index Types",
        lambda: _render_index_types()
    )
    
    layout.render_expandable_section(
        "✏️ Manage Indexes",
        lambda: _render_manage_indexes()
    )
    
    layout.render_expandable_section(
        "📊 Index Performance",
        lambda: _render_index_performance()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_index() -> None:
    """Render create index section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Basic index on single column
CREATE INDEX idx_users_email 
ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_username 
ON users(username);

-- Composite index (multiple columns)
CREATE INDEX idx_posts_user_created 
ON posts(user_id, created_at DESC);

-- Partial index (on subset of rows)
CREATE INDEX idx_active_users 
ON users(email) 
WHERE is_active = TRUE;

-- Index with custom collation
CREATE INDEX idx_case_insensitive_email 
ON users(LOWER(email));

-- Concurrently (doesn't lock table for writes)
CREATE INDEX CONCURRENTLY idx_large_table_col 
ON large_table(column_name);

-- Create if not exists
CREATE INDEX IF NOT EXISTS idx_posts_date 
ON posts(created_at DESC);

-- Expression index
CREATE INDEX idx_posts_lower_title 
ON posts(LOWER(title));

-- Array column index
CREATE INDEX idx_tags 
ON articles USING GIN(tags);
    """, title="SQL Examples")
    
    layout.render_tip("Use CONCURRENTLY on production to avoid locking")


def _render_index_types() -> None:
    """Render index types section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- B-TREE Index (default, good for range queries)
CREATE INDEX idx_btree_age 
ON users USING BTREE(age);

-- HASH Index (equality only, faster for exact matches)
CREATE INDEX idx_hash_email 
ON users USING HASH(email);

-- GIN Index (good for arrays and full text search)
CREATE INDEX idx_gin_tags 
ON articles USING GIN(tags);
CREATE INDEX idx_gin_fts 
ON documents USING GIN(to_tsvector('english', content));

-- GIST Index (good for geometric data and full text search)
CREATE INDEX idx_gist_location 
ON venues USING GIST(location);

-- BRIN Index (good for very large tables)
CREATE INDEX idx_brin_date 
ON large_table USING BRIN(created_at);

-- Bloom Index (approximate matching, PostgreSQL 10+)
CREATE INDEX idx_bloom_columns 
ON table_name USING BLOOM(col1, col2);

-- Query which indexes use which method
SELECT 
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'users';
    """, title="SQL Examples")


def _render_manage_indexes() -> None:
    """Render manage indexes section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Rename index
ALTER INDEX idx_users_email 
RENAME TO idx_users_email_v2;

-- Change index tablespace
ALTER INDEX idx_users_email 
SET TABLESPACE new_tablespace;

-- Drop index
DROP INDEX idx_users_email;

-- Drop if exists
DROP INDEX IF EXISTS idx_users_email;

-- Drop with cascade
DROP INDEX idx_users_email CASCADE;

-- List all indexes on a table
\\d+ table_name

-- Query system catalog for indexes
SELECT 
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'users'
ORDER BY indexname;

-- Reindex (rebuild index)
REINDEX INDEX idx_users_email;

-- Reindex entire table
REINDEX TABLE users;

-- Concurrent reindex
REINDEX INDEX CONCURRENTLY idx_users_email;
    """, title="SQL Examples")


def _render_index_performance() -> None:
    """Render index performance section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Check index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Index size
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexrelname)) as size
FROM pg_indexes
JOIN pg_class ON pg_class.relname = indexname
ORDER BY pg_relation_size(indexrelid) DESC;

-- Duplicate indexes
SELECT 
    a.indexname,
    b.indexname
FROM pg_indexes a
JOIN pg_indexes b ON 
    a.tablename = b.tablename 
    AND a.indexdef = b.indexdef 
    AND a.indexname < b.indexname;

-- Missing indexes based on query execution
EXPLAIN ANALYZE 
SELECT * FROM users WHERE email = 'test@example.com';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Index columns used frequently in WHERE, JOIN, and ORDER BY clauses",
        "Avoid creating too many indexes - they slow down INSERT/UPDATE/DELETE",
        "Use CONCURRENTLY to create indexes without locking in production",
        "Drop unused indexes to save space and improve write performance",
        "Create indexes on foreign key columns for better join performance",
        "B-TREE indexes are the default and work for most cases",
        "Use partial indexes to index only active/relevant rows",
        "Monitor index usage with pg_stat_user_indexes",
        "Composite indexes can help multiple similar queries",
        "Reindex occasionally as indexes can fragment over time"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
