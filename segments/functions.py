"""
Functions Segment
Covers stored functions in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the functions segment."""
    layout = get_layout_manager()
    
    st.header("⚙️ Stored Functions")
    
    layout.render_expandable_section(
        "📝 Create Function",
        lambda: _render_create_function(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Function Details",
        lambda: _render_function_details()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_function() -> None:
    """Render create function section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Simple SQL function
CREATE FUNCTION get_user_post_count(user_id INT) 
RETURNS INT AS $$
    SELECT COUNT(*) FROM posts WHERE user_id = $1;
$$ LANGUAGE SQL;

-- Function with multiple parameters
CREATE FUNCTION calculate_discount(price DECIMAL, discount_percent INT) 
RETURNS DECIMAL AS $$
    SELECT price * (1 - discount_percent / 100.0);
$$ LANGUAGE SQL;

-- PL/pgSQL function (procedural)
CREATE FUNCTION increment_counter(counter_id INT) 
RETURNS INT AS $$
DECLARE
    current_value INT;
BEGIN
    SELECT value INTO current_value FROM counters WHERE id = counter_id;
    UPDATE counters SET value = value + 1 WHERE id = counter_id;
    RETURN current_value + 1;
END;
$$ LANGUAGE plpgsql;

-- Function returning table
CREATE FUNCTION get_user_details(user_id INT) 
RETURNS TABLE(
    username VARCHAR,
    email VARCHAR,
    created_at TIMESTAMP
) AS $$
    SELECT username, email, created_at FROM users WHERE id = user_id;
$$ LANGUAGE SQL;

-- Function with default parameters
CREATE FUNCTION paginate_results(
    page INT DEFAULT 1,
    page_size INT DEFAULT 10
) 
RETURNS TABLE(...) AS $$
    SELECT * FROM table LIMIT page_size OFFSET (page - 1) * page_size;
$$ LANGUAGE SQL;

-- Function with IMMUTABLE (optimization hint)
CREATE FUNCTION calculate_tax(amount DECIMAL) 
RETURNS DECIMAL AS $$
    SELECT amount * 0.1;
$$ LANGUAGE SQL IMMUTABLE;
    """, title="SQL Examples")
    
    layout.render_tip("Use IMMUTABLE and STABLE keywords for query optimizer to cache results")


def _render_function_details() -> None:
    """Render function details section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Call function
SELECT get_user_post_count(1);

-- Call function in WHERE clause
SELECT * FROM users WHERE get_user_post_count(id) > 5;

-- List functions
\\df

-- Drop function
DROP FUNCTION get_user_post_count(INT);

-- Drop function if exists
DROP FUNCTION IF EXISTS calculate_discount(DECIMAL, INT);

-- Replace function
CREATE OR REPLACE FUNCTION get_user_post_count(user_id INT) 
RETURNS INT AS $$
    SELECT COUNT(*) FROM posts WHERE user_id = $1;
$$ LANGUAGE SQL;

-- Complex function example
CREATE FUNCTION validate_email(email VARCHAR) 
RETURNS BOOLEAN AS $$
BEGIN
    IF email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$' THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function with exception handling
CREATE FUNCTION safe_divide(numerator INT, denominator INT) 
RETURNS DECIMAL AS $$
BEGIN
    IF denominator = 0 THEN
        RAISE EXCEPTION 'Division by zero';
    END IF;
    RETURN numerator::DECIMAL / denominator;
END;
$$ LANGUAGE plpgsql;

-- View function definition
SELECT prosrc FROM pg_proc WHERE proname = 'get_user_post_count';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Use parameter placeholders ($1, $2) to prevent SQL injection",
        "Use IMMUTABLE for functions that don't depend on database",
        "Use STABLE for functions that don't modify database",
        "Return appropriate types to avoid implicit casting",
        "Add error handling with RAISE EXCEPTION in PL/pgSQL",
        "Test functions thoroughly before using in production",
        "Use EXPLAIN ANALYZE to understand function performance",
        "Document function purpose and parameters in comments",
        "Use SET search_path to avoid ambiguous function names",
        "Monitor function calls - they can become bottlenecks"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
