"""
Partitioning Segment
Covers table partitioning in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the partitioning segment."""
    layout = get_layout_manager()
    
    st.header("📂 Partitioning")
    
    layout.render_expandable_section(
        "📝 Partition Types",
        lambda: _render_partition_types(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Manage Partitions",
        lambda: _render_manage_partitions()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_partition_types() -> None:
    """Render partition types section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Partitioning** divides large tables into smaller parts:
    
    - **Range partitioning**: Divide by value ranges (e.g., dates)
    - **List partitioning**: Divide by specific values (e.g., regions)
    - **Hash partitioning**: Divide using hash function for even distribution
    - **Composite partitioning**: Combine methods (range then list)
    - **Benefits**: Faster queries, easier maintenance, parallel processing
    - **Pruning**: Query planner skips partitions not matching condition
    - **Partition inheritance**: Child tables inherit from parent
    - **Management**: Easy to add/remove partitions
    - **Performance**: Large tables become manageable chunks
    """)
    
    layout.render_code_block("""
-- Range partition (by date range)
CREATE TABLE orders (
    id BIGSERIAL,
    user_id INT,
    order_date DATE,
    amount DECIMAL,
    PRIMARY KEY (id, order_date)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

-- List partition (by category)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    country VARCHAR,
    data TEXT
) PARTITION BY LIST (country);

CREATE TABLE customers_usa PARTITION OF customers
    FOR VALUES IN ('USA', 'US');

CREATE TABLE customers_europe PARTITION OF customers
    FOR VALUES IN ('UK', 'DE', 'FR');

-- Hash partition (even distribution)
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR,
    event_data JSONB
) PARTITION BY HASH (id);

CREATE TABLE events_p0 PARTITION OF events
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE events_p1 PARTITION OF events
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- Subpartition (partition by multiple columns)
CREATE TABLE transactions (
    id BIGSERIAL,
    user_id INT,
    tx_date DATE,
    amount DECIMAL,
    PRIMARY KEY (id, user_id, tx_date)
) PARTITION BY RANGE (tx_date)
  SUBPARTITION BY LIST (user_id);
    """, title="SQL Examples")
    
    layout.render_tip("Use range partitions for time-series data, list for categories")


def _render_manage_partitions() -> None:
    """Render manage partitions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- List partitions
SELECT 
    schemaname,
    tablename,
    parenttablename
FROM pg_tables
WHERE parenttablename IS NOT NULL
ORDER BY parenttablename;

-- List partition ranges
SELECT 
    tablename,
    pg_get_expr(relpartbound, oid) as bounds
FROM pg_class c
JOIN pg_tables t ON c.relname = t.tablename
WHERE t.parenttablename = 'orders';

-- Add new partition
ALTER TABLE orders ADD PARTITION orders_2024_q3
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

-- Rename partition
ALTER TABLE orders_2024_q1 RENAME TO orders_jan_mar_2024;

-- Detach partition
ALTER TABLE orders DETACH PARTITION orders_2024_q1;

-- Detach partition (concurrently)
ALTER TABLE orders DETACH PARTITION orders_2024_q1 CONCURRENTLY;

-- Attach partition
ALTER TABLE orders ATTACH PARTITION orders_2024_q1
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

-- Drop partition
DROP TABLE orders_2024_q1;

-- Check table partitions
\\d+ orders

-- Indexes on partitions (index parent, not individual partitions)
CREATE INDEX idx_orders_user ON orders(user_id);

-- Query a specific partition
SELECT * FROM orders_2024_q1 WHERE user_id = 123;

-- Partition constraint exists
SELECT schemaname, tablename, constraint_definition
FROM information_schema.constraint_column_usage cc
JOIN information_schema.table_constraints tc 
    ON cc.table_name = tc.table_name
WHERE table_name = 'orders_2024_q1';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Archive Old Orders Efficiently")
    st.markdown("""
    **Scenario:** Your orders table has 500 million rows. Queries are slow because of data volume.
    
    ```sql
    -- BEFORE: One massive table
    -- SELECT count(*) FROM orders takes 10 minutes!
    
    -- AFTER: Partition by year
    CREATE TABLE orders (
        id BIGSERIAL,
        customer_id INT,
        order_date DATE,
        total DECIMAL,
        PRIMARY KEY (id, order_date)
    ) PARTITION BY RANGE (EXTRACT(YEAR FROM order_date));
    
    CREATE TABLE orders_2022 PARTITION OF orders
        FOR VALUES FROM (2022) TO (2023);
    CREATE TABLE orders_2023 PARTITION OF orders
        FOR VALUES FROM (2023) TO (2024);
    CREATE TABLE orders_2024 PARTITION OF orders
        FOR VALUES FROM (2024) TO (2025);
    
    -- Query only current year - queries on orders_2024 are instant!
    SELECT COUNT(*) FROM orders WHERE EXTRACT(YEAR FROM order_date) = 2024;
    -- Only scans orders_2024 partition = 50 million rows instead of 500 million
    
    -- Old year can be archived to cheaper storage
    ALTER TABLE orders DETACH PARTITION orders_2022;
    CREATE TABLE orders_2022_archive AS SELECT * FROM orders_2022;
    DROP TABLE orders_2022;  -- Free up space
    ```
    
    **Why this matters:** Queries on orders_2024 are 10x faster. Can archive old years. Maintenance (VACUUM, ANALYZE) is faster on smaller tables.
    """)
    
    tips = [
        "Use partitioning for very large tables (100GB+)",
        "Range partition by date for time-series data",
        "Consider query patterns before choosing partition column",
        "Maintain consistent partition sizes when possible",
        "Use automated partition creation for future periods",
        "Index at parent table level, not on individual partitions",
        "Monitor partition sizes and rebalance if needed",
        "Test partitioning strategy with realistic data",
        "Plan retention - drop old partitions instead of deleting rows",
        "Understand constraints - some limitations on partitioned tables"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
