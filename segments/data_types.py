"""
Data Types Segment
Covers PostgreSQL data types and their usage.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the data types segment."""
    layout = get_layout_manager()
    
    st.header("🔤 Data Types")
    
    layout.render_expandable_section(
        "📝 Numeric Types",
        lambda: _render_numeric_types(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Text Types",
        lambda: _render_text_types()
    )
    
    layout.render_expandable_section(
        "📝 Date/Time Types",
        lambda: _render_datetime_types()
    )
    
    layout.render_expandable_section(
        "📝 Other Types",
        lambda: _render_other_types()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_numeric_types() -> None:
    """Render numeric types section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- SMALLINT - 2 bytes, range: -32,768 to 32,767
CREATE TABLE table1 (
    status SMALLINT
);

-- INTEGER - 4 bytes, range: -2,147,483,648 to 2,147,483,647
CREATE TABLE table1 (
    count INTEGER
);

-- BIGINT - 8 bytes, range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
CREATE TABLE table1 (
    large_number BIGINT
);

-- SERIAL - Auto-incrementing 4-byte integer
CREATE TABLE users (
    id SERIAL PRIMARY KEY
);

-- BIGSERIAL - Auto-incrementing 8-byte integer
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY
);

-- DECIMAL/NUMERIC - Exact decimal, variable precision
CREATE TABLE products (
    price DECIMAL(10, 2)  -- 10 total digits, 2 after decimal
);

-- FLOAT/DOUBLE PRECISION - Approximate floating point
CREATE TABLE measurements (
    temperature FLOAT,
    value DOUBLE PRECISION
);

-- BOOLEAN - TRUE/FALSE
CREATE TABLE users (
    is_active BOOLEAN DEFAULT TRUE
);
    """, title="SQL Examples")
    
    layout.render_tip("Use BIGSERIAL for IDs to avoid overflow in large tables")


def _render_text_types() -> None:
    """Render text types section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- CHAR(n) - Fixed-length text (pads with spaces)
CREATE TABLE table1 (
    country_code CHAR(2)
);

-- VARCHAR(n) - Variable-length text with limit
CREATE TABLE users (
    username VARCHAR(50),
    email VARCHAR(100)
);

-- VARCHAR without limit
CREATE TABLE users (
    bio VARCHAR
);

-- TEXT - Unlimited text
CREATE TABLE articles (
    content TEXT
);

-- NAME - PostgreSQL internal type for identifiers
CREATE TABLE table1 (
    table_name NAME
);

-- UUID - Universally unique identifier
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50)
);

-- BYTEA - Binary data
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    content BYTEA
);

-- Type casting examples
SELECT CAST('123' AS INTEGER);
SELECT '2024-01-01'::TIMESTAMP;
SELECT id::TEXT FROM users;
    """, title="SQL Examples")


def _render_datetime_types() -> None:
    """Render datetime types section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- DATE - Only date (no time)
CREATE TABLE events (
    event_date DATE
);

-- TIME - Only time (no date)
CREATE TABLE schedule (
    start_time TIME
);

-- TIMESTAMP - Date and time
CREATE TABLE users (
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TIMESTAMP WITH TIME ZONE - Date/time with timezone
CREATE TABLE events (
    event_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- INTERVAL - Duration/difference
CREATE TABLE payments (
    id SERIAL,
    due_date DATE,
    payment_date DATE,
    days_overdue INTERVAL GENERATED ALWAYS AS (payment_date - due_date) STORED
);

-- Working with timestamps
INSERT INTO users (username, created_at) 
VALUES ('john', CURRENT_TIMESTAMP);

SELECT 
    username,
    created_at,
    CURRENT_TIMESTAMP - created_at as account_age
FROM users;

-- Date calculations
SELECT 
    event_date,
    event_date + INTERVAL '7 days' as one_week_later,
    event_date + INTERVAL '1 month' as one_month_later
FROM events;

-- Format timestamp
SELECT TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS');
    """, title="SQL Examples")


def _render_other_types() -> None:
    """Render other types section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- JSON - JSON data
CREATE TABLE settings (
    config JSON
);

-- JSONB - Binary JSON (better performance)
CREATE TABLE settings (
    config JSONB
);

-- Array types
CREATE TABLE tags (
    id SERIAL,
    article_id INTEGER,
    tags TEXT[] ARRAY
);

-- Range types
CREATE TABLE time_ranges (
    id SERIAL,
    duration TSRANGE  -- Timestamp range
);

-- Enumeration type
CREATE TYPE status_enum AS ENUM ('active', 'inactive', 'pending');

CREATE TABLE users (
    status status_enum DEFAULT 'active'
);

-- Composite types
CREATE TYPE address_type AS (
    street VARCHAR,
    city VARCHAR,
    zip_code VARCHAR
);

CREATE TABLE users (
    address address_type
);

-- Network types
CREATE TABLE servers (
    ip INET,
    network CIDR
);

-- Geometric types
CREATE TABLE shapes (
    point POINT,
    line LINE,
    circle CIRCLE,
    polygon POLYGON
);
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Use BIGSERIAL for primary keys to avoid overflow",
        "Use DECIMAL for money/prices, not FLOAT",
        "Use VARCHAR with limit for user input to prevent abuse",
        "Use TEXT for large text content (no performance penalty)",
        "Use TIMESTAMP WITH TIME ZONE for UTC consistency",
        "Use BOOLEAN instead of character flags for yes/no values",
        "Use JSONB instead of JSON for better performance",
        "Use UUID for distributed systems or microservices",
        "Choose appropriate precision for DECIMAL types",
        "Document your custom enum and composite types"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
