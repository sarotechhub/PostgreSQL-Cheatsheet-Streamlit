"""
Roles and Users Segment
Covers creating and managing database roles/users in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the roles and users segment."""
    layout = get_layout_manager()
    
    st.header("👤 Roles & Users")
    
    layout.render_expandable_section(
        "📝 Create Role/User",
        lambda: _render_create_role(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "📝 Manage Roles",
        lambda: _render_manage_roles()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_create_role() -> None:
    """Render create role section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Roles and Users** control database access and permissions:
    
    - **ROLE**: Database object for managing permissions (can't login by default)
    - **USER**: Shorthand for role with LOGIN privilege
    - **PASSWORD**: Required for login (never hardcode, use environment variables)
    - **SUPERUSER**: Extreme privilege - use only for admins
    - **CREATEDB**: Allows user to create new databases
    - **CREATEUSER**: Allows user to create new roles
    - **INHERIT**: Role inherits permissions from groups
    - **Role membership**: Assign roles to users for permission grouping
    """)
    
    layout.render_code_block("""
-- Create basic role (cannot login)
CREATE ROLE admin_group;

-- Create user (can login)
CREATE USER john_user WITH PASSWORD 'secure_password';

-- Role with login privilege
CREATE ROLE app_user WITH LOGIN PASSWORD 'password123';

-- Role with superuser privilege (dangerous!)
CREATE ROLE superuser_role WITH SUPERUSER LOGIN PASSWORD 'password';

-- Role with create database privilege
CREATE ROLE db_creator WITH CREATEDB LOGIN PASSWORD 'password';

-- Role with create role privilege
CREATE ROLE role_manager WITH CREATEROLE LOGIN PASSWORD 'password';

-- Role with expiration date
CREATE ROLE temporary_user 
WITH LOGIN PASSWORD 'password' 
VALID UNTIL '2025-12-31 23:59:59';

-- Role with connection limit
CREATE ROLE limited_user 
WITH LOGIN PASSWORD 'password' 
CONNECTION LIMIT 5;

-- Inherit from another role
CREATE ROLE developer_role;
CREATE ROLE junior_dev ROLE developer_role;
    """, title="SQL Examples")
    
    layout.render_tip("Use strong passwords and follow principle of least privilege")


def _render_manage_roles() -> None:
    """Render manage roles section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- List all roles
\\du

-- List roles with details
SELECT 
    rolname,
    rolsuper,
    rolinherit,
    rolcreaterole,
    rolcreatedb,
    rolcanlogin
FROM pg_roles
WHERE rolname NOT LIKE 'pg_%';

-- Alter role (change password)
ALTER ROLE john_user WITH PASSWORD 'new_password';

-- Alter role options
ALTER ROLE app_user WITH NOLOGIN;  -- Disable login
ALTER ROLE app_user WITH LOGIN;    -- Enable login

-- Alter connection limit
ALTER ROLE limited_user CONNECTION LIMIT 10;

-- Alter role expiration
ALTER ROLE temporary_user VALID UNTIL '2025-06-30';

-- Rename role
ALTER ROLE old_name RENAME TO new_name;

-- Drop role
DROP ROLE old_user;

-- Drop role if exists
DROP ROLE IF EXISTS unused_role;

-- Drop role and reassign owned objects
DROP ROLE user_to_delete;
-- First reassign objects
REASSIGN OWNED BY user_to_delete TO new_owner;
DROP ROLE user_to_delete;

-- List role memberships
SELECT 
    member.rolname,
    role.rolname as role
FROM pg_auth_members
JOIN pg_roles member ON pg_auth_members.member = member.oid
JOIN pg_roles role ON pg_auth_members.role = role.oid;

-- Grant role to user
GRANT developer_role TO john_user;

-- Revoke role from user
REVOKE developer_role FROM john_user;

-- Set default privileges for role
ALTER DEFAULT PRIVILEGES FOR USER app_role 
GRANT SELECT ON TABLES TO readonly_group;
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Implementing Principle of Least Privilege")
    st.markdown("""
    **Scenario:** Different teams need different database access levels
    
    ```sql
    -- Create role groups
    CREATE ROLE developers NOINHERIT;
    CREATE ROLE data_analysts NOINHERIT;
    CREATE ROLE read_only_users NOINHERIT;
    
    -- Individual user accounts that inherit role permissions
    CREATE USER alice WITH PASSWORD 'secure_pass123';
    CREATE USER bob WITH PASSWORD 'secure_pass456';
    CREATE USER charlie WITH PASSWORD 'secure_pass789';
    
    -- Assign roles based on job function
    GRANT developers TO alice;        -- Alice can write code, modify schema
    GRANT data_analysts TO bob;       -- Bob can only SELECT, no writes
    GRANT read_only_users TO charlie; -- Charlie can only read, for dashboards
    
    -- Grant specific permissions per role group
    GRANT USAGE ON SCHEMA public TO developers;
    GRANT CREATE ON SCHEMA public TO developers;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO developers;
    
    GRANT USAGE ON SCHEMA public TO data_analysts;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO data_analysts;
    
    GRANT USAGE ON SCHEMA public TO read_only_users;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only_users;
    
    -- Now: If alice's credentials leak, attacker can only do what developers can do
    -- Can't do what data_analysts or read_only_users can do
    ```
    
    **Why this matters:** Limits damage from compromised credentials. Developer with SELECT-only access can't accidentally DROP tables!
    """)
    
    tips = [
        "Create separate roles for different application users",
        "Use strong, randomly generated passwords",
        "Follow principle of least privilege - grant minimum needed permissions",
        "Use role inheritance to manage permissions efficiently",
        "Never grant superuser to application users",
        "Regularly audit role memberships and permissions",
        "Set appropriate connection limits to prevent DoS",
        "Use SET ROLE to switch between roles for testing",
        "Document role purposes and permission levels",
        "Disable unused roles instead of deleting them immediately"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
