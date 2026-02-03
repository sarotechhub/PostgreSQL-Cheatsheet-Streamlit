"""
Delete Segment
Covers deleting data from PostgreSQL tables.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the delete segment."""
    layout = get_layout_manager()
    
    st.header("🗑️ DELETE Operations")
    
    layout.render_expandable_section(
        "📝 Basic Delete",
        lambda: _render_basic_delete(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Advanced Delete",
        lambda: _render_advanced_delete()
    )
    
    layout.render_expandable_section(
        "⚠️ Safe Delete Patterns",
        lambda: _render_safe_patterns()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_basic_delete() -> None:
    """Render basic delete section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Delete rows matching condition
DELETE FROM users
WHERE is_active = FALSE;

-- Delete by primary key
DELETE FROM users
WHERE id = 123;

-- Delete with RETURNING
DELETE FROM users
WHERE created_at < '2020-01-01'
RETURNING id, username, email;

-- Delete with multiple conditions
DELETE FROM orders
WHERE status = 'cancelled'
  AND created_at < CURRENT_DATE - INTERVAL '90 days';

-- Delete all rows (be careful!)
DELETE FROM temp_table;

-- Delete with IN clause
DELETE FROM users
WHERE id IN (1, 2, 3, 4, 5);
    """, title="SQL Examples")
    
    layout.render_warning("DELETE without WHERE clause deletes ALL rows! Always be careful!")


def _render_advanced_delete() -> None:
    """Render advanced delete section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Delete using subquery
DELETE FROM orders
WHERE user_id IN (
    SELECT id FROM users 
    WHERE created_at < '2015-01-01'
);

-- Delete with JOIN using FROM clause
DELETE FROM orders o
USING users u
WHERE o.user_id = u.id
  AND u.is_active = FALSE;

-- Delete with EXISTS
DELETE FROM comments c
WHERE NOT EXISTS (
    SELECT 1 FROM posts p WHERE p.id = c.post_id
);

-- Delete duplicates (keep first)
DELETE FROM users
WHERE id NOT IN (
    SELECT MIN(id) FROM users GROUP BY email
);

-- Delete old records (keep recent)
DELETE FROM logs
WHERE created_at < CURRENT_DATE - INTERVAL '30 days';

-- Soft delete (mark as deleted instead of removing)
UPDATE users
SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
WHERE id = 123;

-- Hard delete (physical removal) of soft-deleted records
DELETE FROM users
WHERE is_deleted = TRUE
  AND deleted_at < CURRENT_DATE - INTERVAL '365 days';

-- Delete with LIMIT using CTE
WITH rows_to_delete AS (
    SELECT id FROM large_table 
    WHERE status = 'inactive' 
    LIMIT 1000
)
DELETE FROM large_table
WHERE id IN (SELECT id FROM rows_to_delete);
    """, title="SQL Examples")
    
    layout.render_warning("Test DELETE statements with SELECT first to verify WHERE clause!")


def _render_safe_patterns() -> None:
    """Render safe delete patterns section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- SAFE PATTERN 1: Preview before delete
-- Step 1: Check what will be deleted
SELECT COUNT(*) FROM users WHERE is_active = FALSE;
SELECT * FROM users WHERE is_active = FALSE LIMIT 10;

-- Step 2: Delete in transaction (can rollback if needed)
BEGIN;
DELETE FROM users WHERE is_active = FALSE;
-- Review results, then either COMMIT or ROLLBACK
COMMIT;

-- SAFE PATTERN 2: Archive before delete
-- Step 1: Archive to backup table
INSERT INTO users_archive
SELECT * FROM users WHERE created_at < '2015-01-01';

-- Step 2: Delete original
DELETE FROM users WHERE id IN (SELECT id FROM users_archive);

-- SAFE PATTERN 3: Soft delete
-- Instead of deleting, mark as deleted
UPDATE users SET is_deleted = TRUE WHERE id = 123;

-- Query excludes deleted records
SELECT * FROM users WHERE is_deleted = FALSE;

-- SAFE PATTERN 4: Batch delete
-- Delete in chunks to avoid locking table too long
DELETE FROM large_table
WHERE id IN (
    SELECT id FROM large_table 
    WHERE status = 'inactive'
    LIMIT 10000  -- Delete in batches
);

-- SAFE PATTERN 5: Transaction with backup
BEGIN;
CREATE TEMP TABLE deleted_records AS
SELECT * FROM users WHERE is_active = FALSE;

DELETE FROM users WHERE is_active = FALSE;

-- Keep backup for review
COMMIT;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "ALWAYS use WHERE clause in DELETE statements - never delete all rows accidentally",
        "Test DELETE with SELECT first to verify WHERE conditions",
        "Use transactions (BEGIN...COMMIT) to allow rollback if needed",
        "Archive important data before deletion for audit trail",
        "Use soft delete (mark as deleted) for important data",
        "Delete in batches for large tables to avoid long locks",
        "Use RETURNING to verify deleted rows",
        "Check for foreign key constraints before deleting",
        "Cascade DELETE is powerful but dangerous - test thoroughly",
        "Set up backups before bulk delete operations"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
