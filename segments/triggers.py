"""
Triggers Segment
Covers creating and managing triggers in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the triggers segment."""
    layout = get_layout_manager()
    
    st.header("⚡ Triggers")
    
    layout.render_expandable_section(
        "📝 Create Trigger",
        lambda: _render_create_trigger(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Trigger Functions",
        lambda: _render_trigger_functions()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_trigger() -> None:
    """Render create trigger section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Triggers** are automated actions that run when table data changes:
    
    - **Trigger function**: The code that executes (must return TRIGGER type)
    - **BEFORE/AFTER**: Run before or after the triggering event
    - **INSERT/UPDATE/DELETE**: Trigger on specific data modification event
    - **FOR EACH ROW**: Execute once per affected row (vs once per statement)
    - **NEW**: Reference to new row values (for INSERT/UPDATE)
    - **OLD**: Reference to old row values (for DELETE/UPDATE)
    - **Conditional triggers (WHEN)**: Only fire under specific conditions
    - **RAISE EXCEPTION**: Abort the operation with an error message
    """)
    
    layout.render_code_block("""
-- Trigger function (called by trigger)
CREATE FUNCTION update_user_timestamp() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER users_update_timestamp
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_user_timestamp();

-- After insert trigger
CREATE FUNCTION audit_user_insert() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_audit (user_id, action, created_at)
    VALUES (NEW.id, 'INSERT', CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_audit_insert
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION audit_user_insert();

-- Delete trigger
CREATE FUNCTION archive_user_delete() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_archive SELECT OLD.*;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_archive_delete
BEFORE DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION archive_user_delete();

-- Trigger with condition
CREATE FUNCTION validate_email_on_update() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.email NOT LIKE '%@%.%' THEN
        RAISE EXCEPTION 'Invalid email format';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_validate_email
BEFORE UPDATE ON users
FOR EACH ROW
WHEN (NEW.email IS DISTINCT FROM OLD.email)
EXECUTE FUNCTION validate_email_on_update();
    """, title="SQL Examples")
    
    layout.render_tip("Triggers automatically execute in response to table events (INSERT, UPDATE, DELETE)")


def _render_trigger_functions() -> None:
    """Render trigger functions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Trigger that updates related table
CREATE FUNCTION update_post_count() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE users SET post_count = post_count + 1 WHERE id = NEW.user_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE users SET post_count = post_count - 1 WHERE id = OLD.user_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER posts_update_user_count
AFTER INSERT OR DELETE ON posts
FOR EACH ROW
EXECUTE FUNCTION update_post_count();

-- Trigger with INSTEAD OF (for views)
CREATE FUNCTION handle_user_view_insert() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO users (username, email) VALUES (NEW.username, NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_view_insert
INSTEAD OF INSERT ON users_view
FOR EACH ROW
EXECUTE FUNCTION handle_user_view_insert();

-- List triggers
\\dt+ table_name

-- Drop trigger
DROP TRIGGER users_update_timestamp ON users;

-- Drop trigger if exists
DROP TRIGGER IF EXISTS users_update_timestamp ON users;

-- Disable trigger
ALTER TABLE users DISABLE TRIGGER users_update_timestamp;

-- Enable trigger
ALTER TABLE users ENABLE TRIGGER users_update_timestamp;

-- View trigger information
SELECT 
    trigger_name,
    event_object_table,
    event_manipulation,
    action_timing
FROM information_schema.triggers
WHERE trigger_schema = 'public';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Automatically Update Last Modified Timestamp")
    st.markdown("""
    **Scenario:** Track when any user profile was last modified
    
    ```sql
    -- Trigger function to auto-update modified_at
    CREATE FUNCTION update_user_modified() RETURNS TRIGGER AS $$
    BEGIN
        NEW.modified_at = CURRENT_TIMESTAMP;
        NEW.modifier_id = current_user_id();  -- Track who modified it
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Attach to UPDATE operations
    CREATE TRIGGER users_update_modified
    BEFORE UPDATE ON users
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)  -- Only if something actually changed
    EXECUTE FUNCTION update_user_modified();
    
    -- Now whenever someone updates a user, modified_at is automatic
    UPDATE users SET email = 'newemail@test.com' WHERE id = 5;
    -- modified_at is automatically set to NOW()
    ```
    
    **Why this matters:** Eliminates bug where developers forget to update the timestamp. Automatically tracks data lineage and modification history.
    """)
    
    tips = [
        "Keep trigger functions small and focused",
        "Use BEFORE triggers for validation, AFTER for logging",
        "Remember NEW is NULL for DELETE, OLD is NULL for INSERT",
        "Use TG_OP to distinguish between INSERT, UPDATE, DELETE",
        "Don't use triggers for complex business logic - use procedures",
        "Test triggers thoroughly - they run on every operation",
        "Document trigger purposes clearly",
        "Avoid triggers that trigger other triggers (cascading)",
        "Monitor trigger performance - they add overhead",
        "Use triggers sparingly - consider application logic instead"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
