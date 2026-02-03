"""
Procedures Segment
Covers stored procedures in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the procedures segment."""
    layout = get_layout_manager()
    
    st.header("🔧 Stored Procedures")
    
    layout.render_expandable_section(
        "📝 Create Procedure",
        lambda: _render_create_procedure(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Procedure Details",
        lambda: _render_procedure_details()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_procedure() -> None:
    """Render create procedure section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Simple procedure
CREATE PROCEDURE update_user_status(
    user_id INT,
    new_status VARCHAR
) AS $$
BEGIN
    UPDATE users SET status = new_status WHERE id = user_id;
    COMMIT;
END;
$$ LANGUAGE plpgsql;

-- Procedure with transaction control
CREATE PROCEDURE transfer_balance(
    from_account INT,
    to_account INT,
    amount DECIMAL
) AS $$
BEGIN
    UPDATE accounts SET balance = balance - amount WHERE id = from_account;
    UPDATE accounts SET balance = balance + amount WHERE id = to_account;
    COMMIT;
EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
    RAISE EXCEPTION 'Transfer failed: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Procedure with OUT parameters
CREATE PROCEDURE get_account_info(
    account_id INT,
    OUT account_name VARCHAR,
    OUT balance DECIMAL,
    OUT last_transaction TIMESTAMP
) AS $$
BEGIN
    SELECT name, balance, last_transaction_date
    INTO account_name, balance, last_transaction
    FROM accounts
    WHERE id = account_id;
END;
$$ LANGUAGE plpgsql;

-- Procedure with INOUT parameters
CREATE PROCEDURE increment_value(
    INOUT value INT
) AS $$
BEGIN
    value := value + 1;
END;
$$ LANGUAGE plpgsql;

-- Procedure with loop
CREATE PROCEDURE bulk_insert_records(num_records INT) AS $$
DECLARE
    i INT := 1;
BEGIN
    WHILE i <= num_records LOOP
        INSERT INTO records (value) VALUES (i);
        i := i + 1;
    END LOOP;
    COMMIT;
END;
$$ LANGUAGE plpgsql;
    """, title="SQL Examples")
    
    layout.render_tip("Procedures can contain COMMIT/ROLLBACK, unlike functions")


def _render_procedure_details() -> None:
    """Render procedure details section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Call procedure
CALL update_user_status(1, 'active');

-- Call procedure with OUT parameters
CALL get_account_info(123, account_name => ?, balance => ?, last_transaction => ?);

-- List procedures (psql command)
\\df+ procedure_name

-- Drop procedure
DROP PROCEDURE update_user_status(INT, VARCHAR);

-- Drop procedure if exists
DROP PROCEDURE IF EXISTS transfer_balance;

-- View procedure source
SELECT prosrc FROM pg_proc WHERE proname = 'update_user_status';

-- Procedure with variable declarations
CREATE PROCEDURE calculate_summary() AS $$
DECLARE
    total_revenue DECIMAL;
    total_users INT;
    avg_order DECIMAL;
BEGIN
    SELECT SUM(amount) INTO total_revenue FROM orders;
    SELECT COUNT(*) INTO total_users FROM users;
    SELECT AVG(amount) INTO avg_order FROM orders;
    
    INSERT INTO summary_stats (revenue, users, avg_order)
    VALUES (total_revenue, total_users, avg_order);
    COMMIT;
END;
$$ LANGUAGE plpgsql;

-- Procedure with cursor
CREATE PROCEDURE process_users() AS $$
DECLARE
    user_cursor CURSOR FOR SELECT id, email FROM users;
    user_id INT;
    user_email VARCHAR;
BEGIN
    OPEN user_cursor;
    LOOP
        FETCH user_cursor INTO user_id, user_email;
        EXIT WHEN NOT FOUND;
        -- Process each user
        PERFORM process_user_email(user_id, user_email);
    END LOOP;
    CLOSE user_cursor;
    COMMIT;
END;
$$ LANGUAGE plpgsql;

-- Error handling
CREATE PROCEDURE safe_update(
    target_id INT,
    new_value VARCHAR
) AS $$
BEGIN
    UPDATE important_table SET value = new_value WHERE id = target_id;
    RAISE NOTICE 'Update successful for id %', target_id;
    COMMIT;
EXCEPTION WHEN unique_violation THEN
    RAISE EXCEPTION 'Value already exists';
EXCEPTION WHEN OTHERS THEN
    RAISE EXCEPTION 'Unexpected error: %', SQLERRM;
    ROLLBACK;
END;
$$ LANGUAGE plpgsql;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    tips = [
        "Use procedures for complex business logic with COMMIT/ROLLBACK",
        "Functions return values, procedures perform actions",
        "Use OUT parameters to return multiple values from procedures",
        "Always handle exceptions with BEGIN...EXCEPTION...END",
        "Use RAISE NOTICE for logging and debugging",
        "Test procedures thoroughly with various input scenarios",
        "Document procedure purpose, parameters, and side effects",
        "Use transactions carefully - keep them as short as possible",
        "Monitor procedure execution time with pg_stat_statements",
        "Avoid calling procedures in high-frequency queries"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
