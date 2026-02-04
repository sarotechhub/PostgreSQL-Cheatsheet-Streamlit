"""
Performance Tuning Segment
Covers query optimization and performance analysis in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the performance segment."""
    layout = get_layout_manager()
    
    st.header("⚡ Performance Tuning")
    
    layout.render_expandable_section(
        "📝 Query Analysis",
        lambda: _render_query_analysis(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Optimization Techniques",
        lambda: _render_optimization()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_query_analysis() -> None:
    """Render query analysis section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Query Analysis** helps understand how PostgreSQL executes queries:
    
    - **EXPLAIN**: Show query plan WITHOUT executing (cost estimation)
    - **EXPLAIN ANALYZE**: Execute and show actual time/rows processed
    - **Query plan**: Step-by-step how database accesses data
    - **Seq Scan**: Full table scan (slow for large tables)
    - **Index Scan**: Using index (fast for targeted queries)
    - **Nested Loop**: Join method (slow, usually)
    - **Hash Join**: Join method (faster for large datasets)
    - **BUFFERS option**: Shows cache/disk usage
    - **Actual vs estimated**: Difference indicates stats accuracy
    """)
    
    layout.render_code_block("""
-- EXPLAIN (show query plan, don't execute)
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN ANALYZE (execute and show actual stats)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- EXPLAIN with options
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM posts WHERE user_id = 1;

-- EXPLAIN ANALYZE verbose
EXPLAIN (ANALYZE, VERBOSE) SELECT * FROM users;

-- View execution time breakdown
EXPLAIN (ANALYZE, BUFFERS, TIMING) 
SELECT u.username, COUNT(p.id)
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.username;

-- Check query statistics
SELECT 
    query,
    calls,
    total_time,
    mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Enable query statistics collection
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
SELECT pg_stat_statements_reset();

-- Monitor slow queries (log queries taking >1000ms)
SET log_min_duration_statement = 1000;

-- Check table statistics
SELECT 
    schemaname,
    tablename,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows,
    last_analyze
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
    """, title="SQL Examples")
    
    layout.render_tip("Use EXPLAIN ANALYZE to understand actual query execution")


def _render_optimization() -> None:
    """Render optimization techniques section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Create index on slow column
CREATE INDEX idx_users_email ON users(email);

-- Analyze table for better query planning
ANALYZE users;

-- Full vacuum (reclaim space, update stats)
VACUUM FULL ANALYZE users;

-- Auto-vacuum maintenance
ALTER TABLE users SET (autovacuum_vacuum_scale_factor = 0.05);

-- Reindex fragmented index
REINDEX INDEX idx_users_email;

-- Use EXPLAIN to find missing indexes
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 1 AND status = 'pending';
-- If uses sequential scan, add index on (user_id, status)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Query optimization examples

-- BEFORE: Slow subquery
SELECT * FROM orders 
WHERE user_id IN (SELECT id FROM users WHERE country = 'USA');

-- AFTER: Use JOIN
SELECT DISTINCT o.* FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.country = 'USA';

-- BEFORE: N+1 problem
SELECT id FROM users;
-- Then loop and SELECT posts for each user

-- AFTER: Single query with aggregate
SELECT u.id, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;

-- Use LIMIT for pagination (not OFFSET for large numbers)
SELECT * FROM users LIMIT 10 OFFSET 100;  -- Slow on large offsets

-- Use keyset pagination instead
SELECT * FROM users 
WHERE id > last_seen_id
ORDER BY id
LIMIT 10;

-- Enable parallel query execution
SET max_parallel_workers_per_gather = 4;

-- Use appropriate data types (saves space and improves speed)
-- SMALLINT instead of INT if values fit
-- VARCHAR(255) instead of TEXT for short strings
-- DECIMAL(10,2) instead of FLOAT for money
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Optimize Slow E-Commerce Search")
    st.markdown("""
    **Scenario:** Product search takes 30 seconds, customers abandon carts
    
    ```sql
    -- BEFORE: Slow search query
    EXPLAIN ANALYZE
    SELECT p.* FROM products p
    WHERE p.name LIKE '%laptop%'
       OR p.description LIKE '%laptop%'
    LIMIT 50;
    -- Output: Seq Scan on products (30 seconds) - full table scan!
    
    -- STEP 1: Add indexes
    CREATE INDEX idx_products_name ON products(name);
    CREATE INDEX idx_products_description_tsvector 
        ON products USING GIN(to_tsvector('english', description));
    
    -- STEP 2: Rewrite using indexes
    EXPLAIN ANALYZE
    SELECT p.* FROM products p
    WHERE p.name ILIKE '%laptop%'  -- ILIKE uses index
       OR to_tsvector('english', p.description) @@ to_tsquery('laptop')
    LIMIT 50;
    -- Output: Index Scan (100ms) - 300x faster!
    
    -- STEP 3: Use window function for ranking
    SELECT 
        id, name, price,
        CASE 
            WHEN name ILIKE '%laptop%' THEN 1
            ELSE 2
        END as relevance
    FROM products p
    WHERE name ILIKE '%laptop%'
       OR to_tsvector('english', p.description) @@ to_tsquery('laptop')
    ORDER BY relevance, price
    LIMIT 50;
    
    -- STEP 4: Cache with materialized view
    CREATE MATERIALIZED VIEW popular_searches AS
    SELECT id, name, price FROM products WHERE views > 1000;
    CREATE INDEX idx_popular_searches ON popular_searches(id);
    ```
    
    **Why this matters:** 30s → 100ms = 300x improvement! Customers see results instantly. Sales increase!
    """)
    
    tips = [
        "Always use EXPLAIN ANALYZE before optimizing",
        "Create indexes on columns used in WHERE, JOIN, ORDER BY",
        "Regularly run ANALYZE to update table statistics",
        "Monitor slow queries using pg_stat_statements",
        "Avoid SELECT * - specify needed columns",
        "Use LIMIT for pagination, not OFFSET for large numbers",
        "Consider denormalization for read-heavy workloads",
        "Batch writes into transactions for better performance",
        "Use connection pooling to avoid connection overhead",
        "Monitor table bloat and run VACUUM periodically"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
