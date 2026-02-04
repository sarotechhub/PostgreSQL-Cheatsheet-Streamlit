"""
Full Text Search Segment
Covers full text search capabilities in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the full text search segment."""
    layout = get_layout_manager()
    
    st.header("🔎 Full Text Search")
    
    layout.render_expandable_section(
        "📝 FTS Setup",
        lambda: _render_fts_setup(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Search Queries",
        lambda: _render_search_queries()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_fts_setup() -> None:
    """Render FTS setup section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Full Text Search** enables efficient text searching and ranking:
    
    - **TSVECTOR**: Text search vector (preprocessed searchable text)
    - **TSQUERY**: Text search query (what you're searching for)
    - **to_tsvector()**: Convert text to searchable vector
    - **plainto_tsquery()**: Convert plain text to search query
    - **@@ operator**: Matches if tsvector contains tsquery
    - **setweight()**: Assign importance weights (A=highest, D=lowest)
    - **Trigger function**: Auto-update search vector on data changes
    - **Index creation**: GIN index on tsvector for speed
    - **Ranking**: Use ts_rank() to order results by relevance
    """)
    
    layout.render_code_block("""
-- Create table with text search column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    content TEXT,
    search_vector TSVECTOR
);

-- Create function to update search vector
CREATE FUNCTION update_search_vector() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', NEW.title), 'A') ||
        setweight(to_tsvector('english', NEW.content), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update search vector
CREATE TRIGGER documents_search_update
BEFORE INSERT OR UPDATE ON documents
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

-- Create GIN index for fast search
CREATE INDEX idx_documents_search 
ON documents USING GIN(search_vector);

-- Simple insert (trigger updates search_vector)
INSERT INTO documents (title, content) VALUES
('PostgreSQL Guide', 'Learn PostgreSQL database management'),
('MySQL Tutorial', 'Database tutorial for MySQL'),
('SQLite Basics', 'Introduction to SQLite database');

-- Generated column approach (PostgreSQL 12+)
ALTER TABLE documents ADD COLUMN fts TSVECTOR 
    GENERATED ALWAYS AS (
        setweight(to_tsvector('english', title), 'A') ||
        setweight(to_tsvector('english', content), 'B')
    ) STORED;

CREATE INDEX idx_documents_fts ON documents USING GIN(fts);
    """, title="SQL Examples")
    
    layout.render_tip("Use GIN indexes for full text search performance")


def _render_search_queries() -> None:
    """Render search queries section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Simple search (using @@)
SELECT id, title, content
FROM documents
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL');

-- Search with multiple terms (AND)
SELECT id, title
FROM documents
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL & database');

-- Search with OR
SELECT id, title
FROM documents
WHERE search_vector @@ to_tsquery('english', 'PostgreSQL | MySQL');

-- Search with NOT
SELECT id, title
FROM documents
WHERE search_vector @@ to_tsquery('english', 'database & !MySQL');

-- Phrase search
SELECT id, title
FROM documents
WHERE search_vector @@ to_tsquery('english', '"text search"');

-- Prefix search (truncation)
SELECT id, title
FROM documents
WHERE search_vector @@ to_tsquery('english', 'Post:*');

-- Rank results by relevance
SELECT 
    id,
    title,
    ts_rank(search_vector, query) as rank
FROM documents,
    to_tsquery('english', 'PostgreSQL') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Highlight search results
SELECT 
    id,
    title,
    ts_headline(content, query)
FROM documents,
    to_tsquery('english', 'PostgreSQL') query
WHERE search_vector @@ query;

-- Plainto_tsquery (safer for user input)
SELECT *
FROM documents
WHERE search_vector @@ plainto_tsquery('english', 'PostgreSQL database');

-- Websearch query (PostgreSQL 11+)
SELECT *
FROM documents
WHERE search_vector @@ websearch_to_tsquery('english', 'PostgreSQL -MySQL');

-- Get snippets from search results
SELECT 
    id,
    title,
    snippet(content, query, 'short') as snippet
FROM documents,
    to_tsquery('english', 'PostgreSQL') query
WHERE search_vector @@ query;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Search Blog Posts Like Google")
    st.markdown("""
    **Scenario:** Blog with 100k articles. Need fast search with relevance ranking.
    
    ```sql
    -- Create table with search capabilities
    CREATE TABLE blog_posts (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        content TEXT,
        author_id INT,
        published_at TIMESTAMP,
        search_vector TSVECTOR
    );
    
    -- Trigger to auto-update search vector
    CREATE FUNCTION update_blog_search_vector() RETURNS TRIGGER AS $$
    BEGIN
        NEW.search_vector := 
            setweight(to_tsvector('english', NEW.title), 'A') ||
            setweight(to_tsvector('english', NEW.content), 'B');
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER blog_search_update 
    BEFORE INSERT OR UPDATE ON blog_posts
    FOR EACH ROW
    EXECUTE FUNCTION update_blog_search_vector();
    
    -- Index for speed
    CREATE INDEX idx_blog_search ON blog_posts USING GIN(search_vector);
    
    -- User searches, get ranked results
    SELECT 
        id, title, author_id,
        ts_rank(search_vector, query) as relevance,
        ts_headline(content, query, 'short') as snippet
    FROM blog_posts,
        plainto_tsquery('english', 'PostgreSQL optimization') AS query
    WHERE search_vector @@ query
      AND published_at > CURRENT_DATE - INTERVAL '1 year'
    ORDER BY relevance DESC
    LIMIT 10;
    
    -- Result: Fast, ranked search like Google, not LIKE %pattern%!
    ```
    
    **Why this matters:** LIKE queries scan every row slowly. FTS indexes make searches instant even on 1M articles. Ranking shows relevant results first.
    """)
    
    tips = [
        "Use GIN indexes for optimal FTS performance",
        "Use plainto_tsquery for user input (safer than to_tsquery)",
        "Create search vector at insert time with triggers or generated columns",
        "Choose appropriate language ('english', 'french', etc.) for stemming",
        "Use ts_rank to order results by relevance",
        "Use ts_headline to show context around matches",
        "Test FTS queries with EXPLAIN ANALYZE for performance",
        "Document search configuration and supported languages",
        "Consider stemming and stop words in your language setup",
        "Use websearch_to_tsquery for Google-like search syntax"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
