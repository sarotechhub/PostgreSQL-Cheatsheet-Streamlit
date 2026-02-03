"""
Extensions Segment
Covers PostgreSQL extensions.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the extensions segment."""
    layout = get_layout_manager()
    
    st.header("🧩 Extensions")
    
    layout.render_expandable_section(
        "📝 Install & Use Extensions",
        lambda: _render_install_extensions(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Popular Extensions",
        lambda: _render_popular_extensions()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_install_extensions() -> None:
    """Render install extensions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Install extension
CREATE EXTENSION uuid-ossp;

-- Install extension if not exists
CREATE EXTENSION IF NOT EXISTS uuid-ossp;

-- Install extension in specific schema
CREATE EXTENSION uuid-ossp SCHEMA public;

-- Generate UUID with extension
SELECT uuid_generate_v1();
SELECT uuid_generate_v4();

-- List installed extensions
\\dx

-- Check available extensions
SELECT * FROM pg_available_extensions;

-- Drop extension
DROP EXTENSION uuid-ossp;

-- Drop extension with cascade
DROP EXTENSION uuid-ossp CASCADE;

-- Update extension
ALTER EXTENSION uuid-ossp UPDATE;

-- Check extension version
SELECT extname, extversion FROM pg_extension WHERE extname = 'uuid-ossp';
    """, title="SQL Examples")
    
    layout.render_tip("Use extensions to add powerful features without custom code")


def _render_popular_extensions() -> None:
    """Render popular extensions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- UUID generation
CREATE EXTENSION uuid-ossp;
SELECT uuid_generate_v4() as new_id;

-- Full text search
CREATE EXTENSION fuzzystrmatch;
SELECT levenshtein('hello', 'hallo');

-- PostGIS (geographical queries)
CREATE EXTENSION postgis;
SELECT ST_Distance(point1, point2) FROM locations;

-- JSON extensions (built-in, no install needed)
SELECT '{"name": "John"}'::JSONB;
SELECT jsonb_pretty('{"a": 1, "b": 2}');

-- Array utilities
CREATE EXTENSION intarray;
SELECT array_append(ARRAY[1, 2, 3], 4);

-- Trigram similarity
CREATE EXTENSION pg_trgm;
SELECT similarity('hello', 'hallo');

-- pg_cron (schedule jobs)
CREATE EXTENSION pg_cron;
SELECT cron.schedule('job_name', '0 0 * * *', 'VACUUM ANALYZE;');

-- pg_tblspc (tablespace management)
CREATE EXTENSION pg_tblspc;

-- hstore (key-value storage)
CREATE EXTENSION hstore;
SELECT 'name => John, age => 30'::hstore;

-- Range types (built-in)
SELECT '[2024-01-01, 2024-12-31]'::daterange;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Verify extension availability before creating",
        "Use CREATE EXTENSION IF NOT EXISTS for idempotent scripts",
        "Install extensions before creating dependent objects",
        "Keep extensions updated for security and features",
        "Document why each extension is used",
        "Test extensions in development before production",
        "Some extensions require special system packages - check docs",
        "Extensions can impact performance - monitor carefully",
        "Review extension permissions and access control",
        "Consider maintenance burden of third-party extensions"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
