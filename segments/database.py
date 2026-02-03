"""
Database Creation and Management Segment
Covers creating, dropping, and managing databases in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the database segment."""
    layout = get_layout_manager()
    
    st.header("🗄️ Database Creation & Management")
    
    # Create Database
    layout.render_expandable_section(
        "📝 Create Database",
        lambda: _render_create_database(),
        expanded=True
    )
    
    # Drop Database
    layout.render_expandable_section(
        "🗑️ Drop Database",
        lambda: _render_drop_database()
    )
    
    # List Databases
    layout.render_expandable_section(
        "📋 List Databases",
        lambda: _render_list_databases()
    )
    
    # Database Properties
    layout.render_expandable_section(
        "⚙️ Database Properties",
        lambda: _render_database_properties()
    )
    
    # Best Practices
    layout.render_expandable_section(
        "✅ Best Practices & Tips",
        lambda: _render_best_practices()
    )


def _render_create_database() -> None:
    """Render create database section."""
    st.markdown("### Basic Creation")
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Simple database creation
CREATE DATABASE myapp_db;

-- With specific encoding (UTF-8 recommended)
CREATE DATABASE myapp_db 
ENCODING 'UTF8';

-- With owner specification
CREATE DATABASE myapp_db 
OWNER postgres 
ENCODING 'UTF8';

-- With custom template and locale
CREATE DATABASE myapp_db 
OWNER postgres 
TEMPLATE template0
ENCODING 'UTF8'
LC_COLLATE 'C'
LC_CTYPE 'C';

-- With tablespace assignment
CREATE DATABASE myapp_db 
TABLESPACE custom_space;

-- With connection limit
CREATE DATABASE myapp_db 
CONNECTION LIMIT 100;
    """, title="SQL Examples")
    
    layout.render_tip("Always use UTF-8 encoding for international support")


def _render_drop_database() -> None:
    """Render drop database section."""
    st.markdown("### Dropping Databases")
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Drop database (fails if users connected)
DROP DATABASE myapp_db;

-- Drop database if it exists
DROP DATABASE IF EXISTS myapp_db;

-- Force drop database (terminate all connections)
DROP DATABASE myapp_db 
WITH (FORCE);

-- Disconnect all users before drop
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'myapp_db'
  AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS myapp_db;
    """, title="SQL Examples")
    
    layout.render_warning("Use WITH (FORCE) carefully - it terminates active connections!")


def _render_list_databases() -> None:
    """Render list databases section."""
    st.markdown("### Viewing Databases")
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- List all databases (psql command)
\\l

-- Query system catalog
SELECT 
    datname,
    owner_name,
    encoding,
    datcollate,
    datctype
FROM (
    SELECT 
        d.datname,
        r.rolname as owner_name,
        pg_encoding_to_char(d.encoding) as encoding,
        d.datcollate,
        d.datctype
    FROM pg_database d
    JOIN pg_roles r ON d.datdba = r.oid
) AS db_info
ORDER BY datname;

-- Get database size
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
    """, title="SQL Examples")


def _render_database_properties() -> None:
    """Render database properties section."""
    st.markdown("### Modifying Database Properties")
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Change database owner
ALTER DATABASE myapp_db 
OWNER TO new_owner;

-- Change connection limit
ALTER DATABASE myapp_db 
SET connection_limit TO 50;

-- Rename database
ALTER DATABASE old_name 
RENAME TO new_name;

-- Allow/Disallow connections
ALTER DATABASE myapp_db 
ALLOW_CONNECTIONS false;

-- Set default transaction isolation level
ALTER DATABASE myapp_db 
SET default_transaction_isolation TO 'serializable';

-- Reset all settings to defaults
ALTER DATABASE myapp_db 
RESET ALL;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Use explicit ENCODING 'UTF8' for international text support",
        "Assign clear owners and manage permissions properly",
        "Monitor database size regularly with pg_database_size()",
        "Use FORCE option carefully - it disconnects active users",
        "Create separate databases for separate applications",
        "Test database operations in development first",
        "Keep backup copies before major changes",
        "Document your database naming conventions",
        "Set appropriate CONNECTION_LIMIT to prevent resource exhaustion"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
