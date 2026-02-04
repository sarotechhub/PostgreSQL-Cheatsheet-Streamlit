"""
Schema Management Segment
Covers creating, managing, and organizing schemas in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the schema segment."""
    layout = get_layout_manager()
    
    st.header("📂 Schema Management")
    
    layout.render_expandable_section(
        "📝 Create Schema",
        lambda: _render_create_schema(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "🔍 List Schemas",
        lambda: _render_list_schemas()
    )
    
    layout.render_expandable_section(
        "🗑️ Drop Schema",
        lambda: _render_drop_schema()
    )
    
    layout.render_expandable_section(
        "🔐 Schema Permissions",
        lambda: _render_schema_permissions()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_schema() -> None:
    """Render create schema section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Schemas** organize database objects into logical namespaces:
    
    - **Schema**: A container for tables, views, functions, indexes, etc.
    - **public schema**: Default schema (exists by default)
    - **Namespace separation**: Same table name in different schemas allowed
    - **Organization**: Group related objects together
    - **Authorization**: Control access at schema level
    - **Search path**: Order of schemas to check when referencing objects
    - **schema.table notation**: Fully qualified name (schema.table_name)
    """)
    
    layout.render_code_block("""
-- Create basic schema
CREATE SCHEMA public;

-- Create schema with owner
CREATE SCHEMA analytics 
OWNER analytics_user;

-- Create schema with authorization
CREATE SCHEMA app_v1 
AUTHORIZATION app_owner;

-- Create if not exists
CREATE SCHEMA IF NOT EXISTS staging;

-- Set search path for schema access
SET search_path TO public, analytics, staging;

-- View current search path
SHOW search_path;
    """, title="SQL Examples")
    
    layout.render_tip("Use multiple schemas to organize tables by domain/module")


def _render_list_schemas() -> None:
    """Render list schemas section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- List schemas (psql command)
\\dn

-- Query system catalog
SELECT 
    nspname as schema_name,
    pg_catalog.pg_get_userbyid(nspowner) as owner,
    nspacl as permissions
FROM pg_namespace
WHERE nspname NOT LIKE 'pg_%'
  AND nspname != 'information_schema'
ORDER BY nspname;

-- List tables in specific schema
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public';

-- Count objects by schema
SELECT 
    n.nspname,
    COUNT(*) as object_count
FROM pg_class c
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE n.nspname NOT LIKE 'pg_%'
GROUP BY n.nspname
ORDER BY object_count DESC;
    """, title="SQL Examples")


def _render_drop_schema() -> None:
    """Render drop schema section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Drop empty schema
DROP SCHEMA analytics;

-- Drop schema if exists
DROP SCHEMA IF EXISTS staging;

-- Drop schema and all objects (CASCADE)
DROP SCHEMA analytics CASCADE;

-- Restrict dropping (default - fails if not empty)
DROP SCHEMA analytics RESTRICT;

-- Move tables out before deletion
ALTER TABLE analytics.users 
SET SCHEMA public;

DROP SCHEMA analytics;
    """, title="SQL Examples")
    
    layout.render_warning("CASCADE drops all objects in the schema - use carefully!")


def _render_schema_permissions() -> None:
    """Render schema permissions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Grant usage on schema
GRANT USAGE ON SCHEMA analytics 
TO app_user;

-- Grant create on schema
GRANT CREATE ON SCHEMA analytics 
TO app_user;

-- Grant all permissions
GRANT ALL ON SCHEMA analytics 
TO app_user;

-- Revoke permissions
REVOKE ALL ON SCHEMA analytics 
FROM app_user;

-- Grant to all users (public)
GRANT USAGE ON SCHEMA public 
TO PUBLIC;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES 
IN SCHEMA analytics 
GRANT SELECT ON TABLES TO readonly_user;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Organizing Multi-Tenant SaaS Database")
    st.markdown("""
    **Scenario:** Single database serves multiple customers, need data separation
    
    ```sql
    -- Create schema per customer
    CREATE SCHEMA customer_acme;
    CREATE SCHEMA customer_techcorp;
    
    -- Same table structure, different schemas
    CREATE TABLE customer_acme.users (id SERIAL PRIMARY KEY, ...);
    CREATE TABLE customer_techcorp.users (id SERIAL PRIMARY KEY, ...);
    
    -- Grant each customer access only to their schema
    CREATE ROLE customer_acme_app LOGIN;
    GRANT USAGE ON SCHEMA customer_acme TO customer_acme_app;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA customer_acme TO customer_acme_app;
    
    CREATE ROLE customer_techcorp_app LOGIN;
    GRANT USAGE ON SCHEMA customer_techcorp TO customer_techcorp_app;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA customer_techcorp TO customer_techcorp_app;
    
    -- In application, connect with customer-specific role
    -- App connects as 'customer_acme_app', can only access customer_acme schema
    ```
    
    **Why this matters:** Schemas provide logical data separation. Even if someone breaches one customer's app credentials, they can't access other customers' data!
    """)
    
    tips = [
        "Use schemas to organize tables by domain or application module",
        "Always specify schema explicitly in production queries",
        "Avoid using 'public' schema for application tables in large systems",
        "Use meaningful schema names that reflect their purpose",
        "Set appropriate search_path at database or user level",
        "Regularly audit schema permissions and ownership",
        "Keep related tables in the same schema for logical grouping",
        "Use CASCADE carefully when dropping schemas"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
