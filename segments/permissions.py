"""
Permissions Segment
Covers granting and managing permissions in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the permissions segment."""
    layout = get_layout_manager()
    
    st.header("🔐 Permissions & Grants")
    
    layout.render_expandable_section(
        "📝 Grant Permissions",
        lambda: _render_grant_permissions(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Manage Permissions",
        lambda: _render_manage_permissions()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_grant_permissions() -> None:
    """Render grant permissions section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Permissions** control who can access what objects:
    
    - **GRANT**: Give permissions to users/roles
    - **SELECT**: Read permission (query data)
    - **INSERT**: Add new rows
    - **UPDATE**: Modify existing data
    - **DELETE**: Remove rows
    - **EXECUTE**: Run functions/procedures
    - **ALL PRIVILEGES**: Grant all permissions
    - **ON ALL TABLES**: Apply to all tables in schema
    - **WITH GRANT OPTION**: User can grant permissions to others
    - **REVOKE**: Remove permissions
    """)
    
    layout.render_code_block("""
-- Grant SELECT (read) permission on table
GRANT SELECT ON users TO app_user;

-- Grant SELECT on all tables in schema
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

-- Grant INSERT, UPDATE, DELETE (write) permissions
GRANT INSERT, UPDATE, DELETE ON products TO editor_user;

-- Grant all privileges on table
GRANT ALL PRIVILEGES ON users TO app_owner;

-- Grant on specific columns
GRANT SELECT (id, username, email) ON users TO restricted_user;

-- Grant permission on sequence (for auto-increment)
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO app_user;

-- Grant schema usage (can access objects in schema)
GRANT USAGE ON SCHEMA public TO app_user;

-- Grant schema create (can create objects in schema)
GRANT CREATE ON SCHEMA analytics TO analyst_user;

-- Grant database connection
GRANT CONNECT ON DATABASE mydb TO external_user;

-- Grant execute on function
GRANT EXECUTE ON FUNCTION calculate_discount(DECIMAL) TO app_user;

-- Grant with grant option (can give permission to others)
GRANT SELECT ON users TO trusted_user WITH GRANT OPTION;

-- Grant to PUBLIC (all users)
GRANT SELECT ON public_data TO PUBLIC;
    """, title="SQL Examples")
    
    layout.render_tip("Use column-level permissions to restrict access to sensitive data")


def _render_manage_permissions() -> None:
    """Render manage permissions section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Revoke permission
REVOKE SELECT ON users FROM restricted_user;

-- Revoke all permissions
REVOKE ALL PRIVILEGES ON users FROM user_name;

-- Revoke with cascade (revoke from those they granted to)
REVOKE SELECT ON users FROM trusted_user CASCADE;

-- Revoke grant option
REVOKE GRANT OPTION FOR SELECT ON users FROM trusted_user;

-- Check permissions on table
SELECT grantee, privilege_type 
FROM information_schema.role_table_grants
WHERE table_name = 'users';

-- Check permissions on schema
SELECT grantee, privilege_type
FROM information_schema.role_usage_grants
WHERE object_catalog = 'current_database'
  AND object_schema = 'public';

-- Check function permissions
SELECT 
    proacl,
    proname
FROM pg_proc
WHERE proname = 'calculate_discount';

-- List all role permissions
SELECT 
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.role_table_grants
WHERE grantee = 'app_user'
ORDER BY table_name, privilege_type;

-- Set default permissions for future objects
ALTER DEFAULT PRIVILEGES 
GRANT SELECT ON TABLES TO readonly_user;

-- Set default privileges for specific role's future objects
ALTER DEFAULT PRIVILEGES FOR USER app_owner 
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_owner;

-- Reset default privileges
ALTER DEFAULT PRIVILEGES RESET ALL;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Setting Up Audit Trail with Limited Permissions")
    st.markdown("""
    **Scenario:** Audit table should be writable by app, readable by auditors, protected from users
    
    ```sql
    -- Create audit table
    CREATE TABLE audit_log (
        id BIGSERIAL PRIMARY KEY,
        table_name VARCHAR,
        operation VARCHAR(10),
        old_values JSONB,
        new_values JSONB,
        changed_by VARCHAR,
        changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create function to log changes (protected, only accessible internally)
    CREATE FUNCTION log_audit_change() RETURNS TRIGGER AS $$ 
    BEGIN
        INSERT INTO audit_log VALUES (DEFAULT, TG_TABLE_NAME, TG_OP, row_to_json(OLD), row_to_json(NEW), current_user, NOW());
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql SECURITY DEFINER;
    
    -- App can INSERT/SELECT but not UPDATE/DELETE audit logs
    GRANT SELECT, INSERT ON audit_log TO app_user;
    
    -- Auditors can only READ, not modify
    GRANT SELECT ON audit_log TO auditors;
    
    -- Regular users cannot access audit table at all
    REVOKE ALL ON audit_log FROM public;
    
    -- Even if attacker gains app credentials, they can't DELETE audit logs!
    ```
    
    **Why this matters:** Audit trail is tamper-proof. If hacker compromises app account, they can still write logs but can't delete evidence of their actions.
    """)
    
    tips = [
        "Grant minimum necessary permissions (principle of least privilege)",
        "Use column-level permissions for sensitive data",
        "Grant to roles, not individual users when possible",
        "Separate read-only and write roles",
        "Regularly audit granted permissions",
        "Use REVOKE to remove unnecessary permissions",
        "Never grant ALL to application users",
        "Set default privileges for future tables when creating schema",
        "Document permission assignments and reasons",
        "Test permission levels with non-admin users regularly"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
