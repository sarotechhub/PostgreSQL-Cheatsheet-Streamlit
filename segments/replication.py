"""
Replication Segment
Covers PostgreSQL replication and streaming replication.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the replication segment."""
    layout = get_layout_manager()
    
    st.header("🔄 Replication")
    
    layout.render_expandable_section(
        "📝 Replication Setup",
        lambda: _render_replication_setup(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Monitor Replication",
        lambda: _render_monitor_replication()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_replication_setup() -> None:
    """Render replication setup section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Replication** copies data from primary to standby servers:
    
    - **Primary server**: Main database receiving writes
    - **Standby server**: Copy of primary for failover/read scaling
    - **Streaming replication**: Real-time log shipping
    - **WAL (Write-Ahead Log)**: Transaction log sent to standby
    - **Synchronous replication**: Wait for standby before committing
    - **Asynchronous replication**: Commit before standby confirms
    - **Replication slots**: Ensure standby doesn't miss WAL
    - **High availability**: Automatic failover if primary fails
    - **Read-only standby**: Use for reporting without burdening primary
    """)
    
    layout.render_code_block("""
-- PRIMARY SERVER (postgresql.conf)
# Enable WAL archiving
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10

# WAL retention
wal_keep_size = 1GB
# Or use replication slots

# Replication user setup
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'repl_password';

-- PRIMARY SERVER (pg_hba.conf)
# Allow replication from standby
host    replication     replicator    <standby_ip>/32    md5

-- STANDBY SERVER (recovery.conf or postgresql.conf)
primary_conninfo = 'host=primary_server port=5432 user=replicator password=repl_password'
restore_command = 'cp /path/to/archive/%f %p'
standby_mode = on

-- List replication slots
SELECT * FROM pg_replication_slots;

-- Create replication slot (for logical replication)
SELECT * FROM pg_create_physical_replication_slot('slot_name');

-- Monitor replication lag
SELECT 
    pid,
    usesysid,
    usename,
    application_name,
    client_addr,
    backend_start,
    state,
    sync_state
FROM pg_stat_replication;

-- Check replication slot status
SELECT 
    slot_name,
    slot_type,
    active,
    restart_lsn
FROM pg_replication_slots;
    """, title="SQL/Config Examples")
    
    layout.render_tip("Streaming replication provides near real-time data synchronization")


def _render_monitor_replication() -> None:
    """Render monitor replication section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Check replication status (on PRIMARY)
SELECT 
    usename,
    application_name,
    state,
    sync_state,
    replay_lag
FROM pg_stat_replication;

-- Check WAL info
SELECT * FROM pg_current_wal_lsn();

-- Check standby progress
SELECT 
    slot_name,
    restart_lsn,
    confirmed_flush_lsn,
    last_restart_time
FROM pg_replication_slots;

-- Monitor replication delay
SELECT 
    application_name,
    client_addr,
    state,
    sync_state,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication
ORDER BY replay_lag DESC;

-- Promote standby to primary (on STANDBY)
SELECT pg_promote();

-- Or use pg_ctl on the command line
-- pg_ctl promote -D /path/to/data/directory

-- Re-establish replication after promotion (on old PRIMARY)
-- Set up as standby and configure connection to new primary

-- Check if server is primary or standby
SELECT pg_is_in_recovery();

-- View replication slot details
SELECT 
    slot_name,
    slot_type,
    datoid,
    database,
    active,
    restart_lsn,
    confirmed_flush_lsn
FROM pg_replication_slots;

-- List WAL files
SELECT * FROM pg_ls_waldir();

-- Check replication lag in bytes
SELECT 
    client_addr,
    application_name,
    (
        '0/0'::pg_lsn + pg_wal_lsn_diff(
            pg_current_wal_lsn(),
            replay_lsn
        )
    ) as replication_lag_bytes
FROM pg_stat_replication;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Disaster Recovery with Replication")
    st.markdown("""
    **Scenario:** Production database crashes. Need instant failover to standby in another data center
    
    ```
    SETUP:
    - Primary: New York (production)
    - Standby: California (hot backup, read-only)
    
    PRIMARY CONFIG (postgresql.conf):
    wal_level = replica
    max_wal_senders = 10
    wal_keep_size = 1GB
    max_replication_slots = 10
    
    -- Create replication user
    CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'secure_password';
    
    STANDBY SETUP:
    1. Take base backup from primary
       pg_basebackup -h primary.example.com -D /var/lib/postgresql/14/main -U replicator
    
    2. Create recovery configuration
       # recovery.conf
       primary_conninfo = 'host=primary.example.com user=replicator password=secure_password'
       
    3. Start standby server
       pg_ctl start
    
    DURING NORMAL OPERATION:
    -- Primary handles all writes
    SELECT count(*) FROM users;  -- On primary, instant
    
    -- Standby handles reads (offload reporting)
    SELECT count(*) FROM orders;  -- On standby, instant
    
    ON DISASTER (Primary dies):
    -- Promote standby to primary
    SELECT pg_promote();
    -- Standby is now primary, accepts writes
    
    -- Redirect applications to new primary (California)
    -- Previous primary can be added as standby once fixed
    
    MONITORING:
    -- Check replication lag
    SELECT 
        client_addr,
        (pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn))::text as lag_bytes
    FROM pg_stat_replication;
    ```
    
    **Why this matters:** Without replication, primary crash = hours of downtime. With it, you're back online in seconds. SLA uptime goes from 99.5% to 99.99%!
    """)
    
    tips = [
        "Use replication for high availability and read scaling",
        "Set up monitoring to track replication lag",
        "Use synchronous replication for critical data (with performance cost)",
        "Implement connection pooling to manage replica connections",
        "Create replication slots to prevent WAL deletion",
        "Test failover procedures regularly",
        "Document failover procedures and steps",
        "Monitor disk space for WAL files and archives",
        "Set up automated backup of replicas for additional redundancy",
        "Use asynchronous replication by default for better performance"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
