"""
Backup and Restore Segment
Covers backing up and restoring PostgreSQL databases.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the backup and restore segment."""
    layout = get_layout_manager()
    
    st.header("💾 Backup & Restore")
    
    layout.render_expandable_section(
        "📝 Backup Methods",
        lambda: _render_backup_methods(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Restore Methods",
        lambda: _render_restore_methods()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_backup_methods() -> None:
    """Render backup methods section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- SQL dump (text format)
pg_dump -U postgres mydb > backup.sql

-- SQL dump with custom format (binary)
pg_dump -U postgres -Fc mydb > backup.dump

-- SQL dump with data only
pg_dump -U postgres --data-only mydb > data_backup.sql

-- SQL dump with schema only
pg_dump -U postgres --schema-only mydb > schema_backup.sql

-- Dump specific table
pg_dump -U postgres -t users mydb > users_backup.sql

-- Dump multiple tables
pg_dump -U postgres -t users -t posts mydb > tables_backup.sql

-- Dump schema(s)
pg_dump -U postgres -n analytics mydb > schema_backup.sql

-- Backup with verbose output
pg_dump -U postgres -v mydb > backup.sql

-- Backup all databases
pg_dumpall -U postgres > all_databases.sql

-- Backup with compression
pg_dump -U postgres -Fc mydb | gzip > backup.dump.gz

-- Continuous WAL archiving (Point-in-time recovery)
-- Enable in postgresql.conf:
-- wal_level = archive
-- archive_mode = on
-- archive_command = 'test ! -f /path/to/archive/%f && cp %p /path/to/archive/%f'
    """, title="Shell Commands")
    
    layout.render_tip("Use pg_dump with custom format (-Fc) for smaller files and parallel restore")


def _render_restore_methods() -> None:
    """Render restore methods section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Restore from SQL dump
psql -U postgres mydb < backup.sql

-- Restore from custom format
pg_restore -U postgres -d mydb backup.dump

-- Restore with verbose output
pg_restore -U postgres -v -d mydb backup.dump

-- Restore specific table
pg_restore -U postgres -t users -d mydb backup.dump

-- Restore data only (schema must exist)
pg_restore -U postgres --data-only -d mydb backup.dump

-- Restore schema only
pg_restore -U postgres --schema-only -d mydb backup.dump

-- Parallel restore (multiple jobs)
pg_restore -U postgres -j 4 -d mydb backup.dump

-- Restore to new database
pg_restore -U postgres -C -d postgres backup.dump

-- Restore with drop existing objects
pg_restore -U postgres --clean -d mydb backup.dump

-- Restore all databases
psql -U postgres < all_databases.sql

-- Partial restore from compressed backup
zcat backup.dump.gz | pg_restore -U postgres -d mydb

-- Skip errors during restore
pg_restore -U postgres --exit-on-error=false -d mydb backup.dump
    """, title="Shell Commands")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Take regular backups - automate with cron or scheduler",
        "Use custom format (-Fc) for better compression and selective restore",
        "Test restores regularly - a backup is only good if it works",
        "Store backups in multiple locations (local and remote)",
        "Keep incremental backups with WAL archiving for point-in-time recovery",
        "Use pg_dump for logical backups, WAL archiving for physical backups",
        "Backup before major changes or migrations",
        "Encrypt backups if they contain sensitive data",
        "Monitor backup size and success/failure status",
        "Document backup and restore procedures"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
