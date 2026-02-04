"""
JSON Data Segment
Covers JSON and JSONB data types in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the JSON segment."""
    layout = get_layout_manager()
    
    st.header("📋 JSON & JSONB")
    
    layout.render_expandable_section(
        "📝 JSON Operations",
        lambda: _render_json_operations(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 JSON Functions",
        lambda: _render_json_functions()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_json_operations() -> None:
    """Render JSON operations section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **JSON/JSONB** types store semi-structured data:
    
    - **JSON**: Stores as text (slower but preserves formatting)
    - **JSONB**: Binary format (faster, supports indexing, no duplicate keys)
    - **Extract values**: Use -> operator to get fields
    - **Get as text**: Use ->> operator to return text instead of JSON
    - **Nested access**: Use -> with array indices or object keys
    - **JSON functions**: json_extract_path(), jsonb_agg(), etc.
    - **Querying**: Use @> (contains) operator to search JSON
    - **Indexing**: Create indexes on JSONB for performance
    """)
    
    layout.render_code_block("""
-- Create table with JSONB column
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR,
    metadata JSONB
);

-- Insert JSON data
INSERT INTO users (username, metadata) VALUES
('john', '{"age": 30, "city": "New York", "tags": ["admin", "user"]}'),
('jane', '{"age": 25, "city": "Los Angeles", "tags": ["user"]}');

-- Query JSON values
SELECT username, metadata->>'age' as age FROM users;

-- Query JSON array
SELECT username, metadata->'tags' as tags FROM users;

-- Query nested JSON
SELECT metadata->'address'->>'city' FROM users;

-- Filter by JSON value
SELECT * FROM users WHERE metadata->>'age' = '30';

-- Filter by JSON array contains
SELECT * FROM users 
WHERE metadata->'tags' @> '"admin"'::jsonb;

-- Update JSON value
UPDATE users 
SET metadata = jsonb_set(metadata, '{age}', '31')
WHERE username = 'john';

-- Add key to JSON
UPDATE users
SET metadata = metadata || '{"verified": true}'
WHERE username = 'john';

-- Remove key from JSON
UPDATE users
SET metadata = metadata - 'verified'
WHERE username = 'john';

-- Get all JSON keys
SELECT jsonb_object_keys(metadata) FROM users;

-- JSON to text
SELECT jsonb_pretty(metadata) FROM users;
    """, title="SQL Examples")
    
    layout.render_tip("Use JSONB instead of JSON for better performance and query capabilities")


def _render_json_functions() -> None:
    """Render JSON functions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- jsonb_object_keys - get all keys
SELECT jsonb_object_keys('{"a": 1, "b": 2}'::jsonb);

-- jsonb_array_length - array size
SELECT jsonb_array_length('[1, 2, 3, 4, 5]'::jsonb);

-- jsonb_array_elements - expand array
SELECT jsonb_array_elements('[1, 2, 3]'::jsonb);

-- jsonb_to_record - convert to record
SELECT * FROM jsonb_to_record(
    '{"name": "John", "age": 30}'::jsonb
) AS (name TEXT, age INT);

-- jsonb_each - expand object to key-value
SELECT key, value FROM jsonb_each('{"a": 1, "b": 2}'::jsonb);

-- jsonb_path_exists - check path exists
SELECT jsonb_path_exists('{"user": {"name": "John"}}'::jsonb, '$.user.name');

-- jsonb_path_query - query with path
SELECT jsonb_path_query(
    '{"a": [1, 2, 3]}'::jsonb,
    '$.a[*]'
);

-- jsonb_agg - aggregate to JSON array
SELECT jsonb_agg(username) FROM users;

-- json_build_object - build JSON
SELECT json_build_object('id', id, 'name', username) FROM users;

-- json_build_array - build JSON array
SELECT json_build_array(id, username, 'user') FROM users;

-- CAST to/from JSON
SELECT metadata::TEXT FROM users;
SELECT ('{"a": 1}'::TEXT)::JSONB;

-- Index JSON for performance
CREATE INDEX idx_users_metadata_age 
ON users USING GIN(metadata jsonb_path_ops);

-- Query with indexed JSON
SELECT * FROM users 
WHERE metadata @> '{"verified": true}'::jsonb;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Store User Preferences Flexibly")
    st.markdown("""
    **Scenario:** User preferences vary widely. Some prefer email, others SMS. Some use dark mode, others light.
    
    ```sql
    -- Traditional approach: Add column for every preference
    -- ALTER TABLE users ADD COLUMN prefer_email BOOLEAN;
    -- ALTER TABLE users ADD COLUMN prefer_sms BOOLEAN;
    -- ALTER TABLE users ADD COLUMN theme VARCHAR;
    -- ALTER TABLE users ADD COLUMN language VARCHAR;
    -- ALTER TABLE users ADD COLUMN timezone VARCHAR;
    -- Result: Table becomes unmaintainable with 100 columns!
    
    -- BETTER: Store flexible preferences as JSONB
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR,
        preferences JSONB DEFAULT '{}'
    );
    
    -- Insert flexible preferences
    INSERT INTO users (username, preferences) VALUES (
        'alice',
        '{"notifications": {"email": true, "sms": false, "push": true},
          "display": {"theme": "dark", "language": "es"},
          "privacy": {"profile_visible": true}}'
    );
    
    -- Query users with specific preference
    SELECT * FROM users WHERE preferences @> '{"display": {"theme": "dark"}}';
    
    -- Update nested preference
    UPDATE users SET preferences = jsonb_set(
        preferences, 
        '{notifications, email}', 
        'false'
    ) WHERE id = 1;
    ```
    
    **Why this matters:** No need to add columns. Preferences evolve without schema changes. New fields added instantly!
    """)
    
    tips = [
        "Use JSONB instead of JSON for better performance",
        "Create GIN indexes on JSONB columns for fast queries",
        "Validate JSON structure at application level",
        "Don't store everything as JSON - use proper columns for frequent queries",
        "Use jsonb_path_query for complex navigation",
        "Remember ->> returns text, -> returns JSONB",
        "Use @> for membership testing (requires GIN index)",
        "Test queries with EXPLAIN ANALYZE for performance",
        "Document JSON schema and expected structure",
        "Consider using JSON Schema validation for complex structures"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
