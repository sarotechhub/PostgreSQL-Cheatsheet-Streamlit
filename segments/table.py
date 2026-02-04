"""
Table Management Segment
Covers creating, altering, and managing tables in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the table segment."""
    layout = get_layout_manager()
    
    st.header("📋 Table Management")
    
    layout.render_expandable_section(
        "📝 Create Table",
        lambda: _render_create_table(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "✏️ Alter Table",
        lambda: _render_alter_table()
    )
    
    layout.render_expandable_section(
        "🗑️ Drop Table",
        lambda: _render_drop_table()
    )
    
    layout.render_expandable_section(
        "📊 Table Information",
        lambda: _render_table_info()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_table() -> None:
    """Render create table section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **CREATE TABLE** defines the structure and constraints for data storage:
    
    - **Column types**: SERIAL (auto-increment), VARCHAR, INT, DECIMAL, TIMESTAMP, etc.
    - **PRIMARY KEY**: Unique identifier for each row
    - **NOT NULL**: Column must always have a value
    - **UNIQUE**: Column values must be unique
    - **DEFAULT**: Default value if none provided
    - **FOREIGN KEY**: Reference to primary key in another table
    - **CHECK**: Constraint on allowed values
    - **ON DELETE CASCADE**: Automatically delete related rows
    - **UNLOGGED**: Fast but not crash-safe (for temporary data)
    """)
    
    layout.render_code_block("""
-- Basic table creation
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table with constraints
CREATE TABLE posts (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table with composite primary key
CREATE TABLE user_permissions (
    user_id INTEGER NOT NULL REFERENCES users(id),
    permission_id INTEGER NOT NULL REFERENCES permissions(id),
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, permission_id)
);

-- Create if not exists
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0)
);

-- Unlogged table (faster, not ACID)
CREATE UNLOGGED TABLE temp_data (
    id SERIAL PRIMARY KEY,
    data TEXT
);
    """, title="SQL Examples")
    
    layout.render_tip("Use SERIAL/BIGSERIAL for auto-incrementing IDs")


def _render_alter_table() -> None:
    """Render alter table section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Add column
ALTER TABLE users 
ADD COLUMN last_login TIMESTAMP;

-- Add column with default value
ALTER TABLE users 
ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- Add column with constraints
ALTER TABLE users 
ADD COLUMN phone VARCHAR(20) NOT NULL UNIQUE;

-- Drop column
ALTER TABLE users 
DROP COLUMN phone;

-- Drop column if exists (CASCADE to drop dependents)
ALTER TABLE users 
DROP COLUMN IF EXISTS phone CASCADE;

-- Rename column
ALTER TABLE users 
RENAME COLUMN created_at TO registered_at;

-- Rename table
ALTER TABLE users 
RENAME TO app_users;

-- Modify column type
ALTER TABLE users 
ALTER COLUMN username TYPE VARCHAR(100);

-- Add constraint
ALTER TABLE posts 
ADD CONSTRAINT fk_user 
FOREIGN KEY (user_id) REFERENCES users(id);

-- Add check constraint
ALTER TABLE products 
ADD CONSTRAINT check_price 
CHECK (price > 0);

-- Set default value
ALTER TABLE users 
ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;

-- Drop constraint
ALTER TABLE posts 
DROP CONSTRAINT fk_user;

-- Change table owner
ALTER TABLE users 
OWNER TO new_owner;
    """, title="SQL Examples")


def _render_drop_table() -> None:
    """Render drop table section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Drop single table
DROP TABLE users;

-- Drop if exists
DROP TABLE IF EXISTS users;

-- Drop multiple tables
DROP TABLE IF EXISTS users, posts, comments;

-- Drop with cascade (drops dependent objects)
DROP TABLE users CASCADE;

-- Drop with restrict (default - fails if dependencies exist)
DROP TABLE users RESTRICT;

-- Safely check for dependencies before drop
SELECT constraint_name, table_name 
FROM information_schema.table_constraints 
WHERE table_name = 'users';
    """, title="SQL Examples")
    
    layout.render_warning("CASCADE drops all dependent objects - use carefully!")
    
    st.markdown("### 🏢 Real-World Example: E-Commerce Database Schema")
    st.markdown("""
    **Scenario:** Design normalized tables for orders, customers, and products
    
    ```sql
    CREATE TABLE customers (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        sku VARCHAR(50) NOT NULL UNIQUE,
        price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
        stock_level INT DEFAULT 0,
        supplier_id INT REFERENCES suppliers(id)
    );
    
    CREATE TABLE orders (
        id BIGSERIAL PRIMARY KEY,
        customer_id INT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL(12, 2),
        status VARCHAR(20) DEFAULT 'pending'
    );
    
    CREATE TABLE order_items (
        id SERIAL PRIMARY KEY,
        order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
        product_id INT NOT NULL REFERENCES products(id),
        quantity INT NOT NULL CHECK (quantity > 0),
        unit_price DECIMAL(10, 2) NOT NULL
    );
    ```
    
    **Why this matters:** Proper schema design prevents data anomalies, makes queries efficient, and enforces business rules at the database level.
    """)


def _render_table_info() -> None:
    """Render table information section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- List tables (psql command)
\\dt

-- List tables in specific schema
\\dt schema_name.*

-- Detailed table structure
\\d table_name

-- List all columns in table
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users';

-- Get table size
SELECT 
    pg_size_pretty(pg_total_relation_size('users')) as size;

-- List all constraints on table
SELECT constraint_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'users';

-- Check table statistics
SELECT 
    schemaname,
    tablename,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE tablename = 'users';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Always define PRIMARY KEY for every table",
        "Use BIGSERIAL for IDs to avoid overflow issues",
        "Add timestamp columns with DEFAULT CURRENT_TIMESTAMP",
        "Use meaningful column names and appropriate data types",
        "Define FOREIGN KEYS to maintain referential integrity",
        "Add CHECK constraints to enforce business rules",
        "Use NOT NULL for required columns",
        "Test ALTER TABLE operations on a copy first",
        "Plan for future growth when choosing data types",
        "Regular VACUUM and ANALYZE for table statistics"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
