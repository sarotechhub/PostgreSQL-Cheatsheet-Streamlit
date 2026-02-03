"""
Transactions Segment
Covers transaction control in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the transactions segment."""
    layout = get_layout_manager()
    
    st.header("🔄 Transactions")
    
    layout.render_expandable_section(
        "📝 Transaction Control",
        lambda: _render_transaction_control(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Isolation Levels",
        lambda: _render_isolation_levels()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_transaction_control() -> None:
    """Render transaction control section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Basic transaction
BEGIN;
INSERT INTO users (username, email) VALUES ('john', 'john@example.com');
UPDATE users SET is_active = TRUE WHERE username = 'john';
COMMIT;

-- Rollback transaction
BEGIN;
DELETE FROM users WHERE id = 1;
-- Changed mind - roll back
ROLLBACK;

-- Savepoint (nested transaction)
BEGIN;
INSERT INTO accounts (balance) VALUES (1000);
SAVEPOINT sp1;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- If error occurs
ROLLBACK TO sp1;  -- Rollback just to savepoint
COMMIT;

-- Implicit transaction
SET autocommit = OFF;
INSERT INTO table1 VALUES (...);
INSERT INTO table2 VALUES (...);
COMMIT;

-- Transaction with exception handling
BEGIN;
BEGIN
    INSERT INTO users (username) VALUES ('john');
EXCEPTION WHEN unique_violation THEN
    UPDATE users SET email = 'newemail@example.com' WHERE username = 'john';
END;
COMMIT;
    """, title="SQL Examples")
    
    layout.render_tip("Use transactions to ensure multiple statements succeed or fail together")


def _render_isolation_levels() -> None:
    """Render isolation levels section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- READ UNCOMMITTED (default behavior in PostgreSQL)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SELECT * FROM users WHERE balance > 100;
COMMIT;

-- READ COMMITTED (default, prevents dirty reads)
BEGIN;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SELECT * FROM accounts WHERE balance > 0;
COMMIT;

-- REPEATABLE READ (prevents phantom reads)
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT COUNT(*) FROM orders;
-- Will see same count even if other transactions insert
COMMIT;

-- SERIALIZABLE (strictest, prevents all anomalies)
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM inventory WHERE quantity < 100;
UPDATE inventory SET quantity = 0 WHERE id = 1;
COMMIT;

-- Check current transaction isolation level
SHOW transaction_isolation;

-- Set default for session
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Set default for database
ALTER DATABASE mydb SET default_transaction_isolation = 'repeatable read';

-- Deadlock handling
CREATE OR REPLACE FUNCTION retry_transaction() AS $$
DECLARE
    retry_count INT := 0;
BEGIN
    WHILE retry_count < 3 LOOP
        BEGIN
            BEGIN;
            -- Transaction logic here
            COMMIT;
            RETURN;
        EXCEPTION WHEN deadlock_detected THEN
            ROLLBACK;
            retry_count := retry_count + 1;
        END;
    END LOOP;
    RAISE EXCEPTION 'Transaction failed after retries';
END;
$$ LANGUAGE plpgsql;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Keep transactions as short as possible to reduce lock contention",
        "Use SERIALIZABLE only when necessary - it can cause performance issues",
        "Use REPEATABLE READ for most applications to prevent anomalies",
        "Always commit or rollback - don't leave transactions hanging",
        "Use savepoints for complex multi-step operations",
        "Implement retry logic for transient failures (deadlocks)",
        "Test concurrent transactions to understand isolation levels",
        "Use explicit transaction control (BEGIN...COMMIT) in application code",
        "Monitor active transactions with pg_stat_activity",
        "Document transaction semantics in your application"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
