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
    
    st.markdown("""
    **Backup Methods** protect your data from loss:
    
    - **SQL dump (text)**: Human-readable SQL commands (pg_dump)
    - **Custom/Binary format**: Compressed, faster restore (pg_dump -Fc)
    - **Data only**: Just data, no schema (--data-only)
    - **Schema only**: Just structure, no data (--schema-only)
    - **Specific table**: Backup single table (--table)
    - **Full backup**: Database structure + data + sequences
    - **Incremental backup**: Only changes since last backup
    - **Point-in-time recovery**: Restore to specific timestamp
    - **Frequency**: Regular backups prevent data loss
    """)
    
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
    
    st.markdown("### 🏢 Real-World Example: Automated Backup Strategy")
    st.markdown("""
    **Scenario:** 24/7 SaaS app, can't afford data loss, need fast restore
    
    ```bash
    #!/bin/bash
    # Daily backup script (run via cron)
    
    BACKUP_DIR="/backups/postgresql"
    DB_NAME="production_db"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    
    # Full backup at midnight
    pg_dump -U postgres -Fc $DB_NAME | gzip > $BACKUP_DIR/full_$TIMESTAMP.dump.gz
    
    # Verify backup is valid (test restore)
    pg_restore -U postgres --list $BACKUP_DIR/full_$TIMESTAMP.dump.gz > /dev/null
    
    # Keep only last 30 days
    find $BACKUP_DIR -name "full_*.dump.gz" -mtime +30 -delete
    
    # Alert if backup fails
    if [ $? -ne 0 ]; then
        echo "BACKUP FAILED!" | mail -s "Critical: DB Backup Failed" admin@example.com
    fi
    
    # Crontab entry
    # 0 2 * * * /scripts/backup_db.sh  (Run daily at 2 AM)
    
    # On disaster, restore from backup
    createdb restored_db
    pg_restore -U postgres -d restored_db /backups/postgresql/full_20250205_000000.dump.gz
    ```
    
    **Why this matters:** Automated backups save your business. Without them, one SQL mistake deletes everything. gzip saves 70% disk space. Testing restore ensures backups actually work!
    """)
    
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
