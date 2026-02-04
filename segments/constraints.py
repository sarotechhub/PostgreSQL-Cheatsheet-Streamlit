"""
Constraints Segment
Covers creating and managing constraints in PostgreSQL.
"""

import streamlit as st
from layout import get_layout_manager


def render_segment() -> None:
    """Render the constraints segment."""
    layout = get_layout_manager()
    
    st.header("🔐 Constraints")
    
    layout.render_expandable_section(
        "📝 Constraint Types",
        lambda: _render_constraint_types(),
        expanded=True
    )
    
    layout.render_expandable_section(
        "✏️ Add/Drop Constraints",
        lambda: _render_add_drop_constraints()
    )
    
    layout.render_expandable_section(
        "🔍 View Constraints",
        lambda: _render_view_constraints()
    )
    
    layout.render_expandable_section(
        "✅ Best Practices",
        lambda: _render_best_practices()
    )


def _render_constraint_types() -> None:
    """Render constraint types section."""
    layout = get_layout_manager()
    
    st.markdown("""
    **Constraints** enforce data integrity rules:
    
    - **PRIMARY KEY**: Uniquely identifies each row (one per table)
    - **UNIQUE**: Ensures column values are unique (multiple allowed)
    - **NOT NULL**: Requires column to have a value
    - **FOREIGN KEY**: References primary key in another table
    - **CHECK**: Validates data (e.g., price > 0)
    - **DEFAULT**: Provides value if none supplied
    - **EXCLUDE**: Prevents overlapping data (ranges, ranges)
    - **Referential integrity**: Maintains relationships between tables
    - **ON DELETE/UPDATE**: Actions when referenced rows change
    """)
    
    layout.render_code_block("""
-- PRIMARY KEY - Unique identifier for row
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

-- UNIQUE - Ensure column values are unique
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- NOT NULL - Column must have a value
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

-- CHECK - Custom validation rule
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0)
);

-- FOREIGN KEY - Reference another table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id)
);

-- FOREIGN KEY with actions
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- FOREIGN KEY defer options
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) 
        DEFERRABLE INITIALLY DEFERRED
);

-- Composite UNIQUE constraint
CREATE TABLE user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    UNIQUE(user_id, role_id)
);

-- Named constraints
ALTER TABLE users 
ADD CONSTRAINT email_length_check CHECK (LENGTH(email) > 0);
    """, title="SQL Examples")


def _render_add_drop_constraints() -> None:
    """Render add/drop constraints section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Add NOT NULL constraint
ALTER TABLE users 
ALTER COLUMN email SET NOT NULL;

-- Remove NOT NULL constraint
ALTER TABLE users 
ALTER COLUMN email DROP NOT NULL;

-- Add UNIQUE constraint
ALTER TABLE users 
ADD CONSTRAINT unique_email UNIQUE(email);

-- Add CHECK constraint
ALTER TABLE products 
ADD CONSTRAINT check_positive_price CHECK (price > 0);

-- Add FOREIGN KEY constraint
ALTER TABLE posts 
ADD CONSTRAINT fk_posts_user_id 
FOREIGN KEY (user_id) REFERENCES users(id);

-- Add PRIMARY KEY constraint (if not exists)
ALTER TABLE users 
ADD CONSTRAINT pk_users PRIMARY KEY(id);

-- Drop constraint by name
ALTER TABLE users 
DROP CONSTRAINT unique_email;

-- Drop constraint (cascade dependents)
ALTER TABLE users 
DROP CONSTRAINT unique_email CASCADE;

-- Drop NOT NULL
ALTER TABLE users 
ALTER COLUMN email DROP NOT NULL;

-- List all constraints
\\d+ table_name

-- Query constraints
SELECT constraint_name, constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'users';
    """, title="SQL Examples")


def _render_view_constraints() -> None:
    """Render view constraints section."""
    layout = get_layout_manager()
    
    layout.render_code_block("""
-- Get all constraints for a table
SELECT 
    constraint_name,
    constraint_type,
    table_name
FROM information_schema.table_constraints
WHERE table_name = 'users';

-- Get check constraints details
SELECT 
    constraint_name,
    check_clause
FROM information_schema.check_constraints
WHERE constraint_schema = 'public';

-- Get key column usage (FK, PK, etc)
SELECT 
    constraint_name,
    table_name,
    column_name,
    ordinal_position
FROM information_schema.key_column_usage
WHERE table_name = 'posts'
ORDER BY ordinal_position;

-- Get referential constraints (FKs)
SELECT 
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
FROM information_schema.referential_constraints rc
JOIN information_schema.key_column_usage kcu 
    ON rc.constraint_name = kcu.constraint_name;

-- Find foreign keys referencing a table
SELECT 
    constraint_name,
    table_name
FROM information_schema.referential_constraints
WHERE referenced_table_name = 'users';
    """, title="SQL Examples")


def _render_best_practices() -> None:
    """Render best practices section."""
    layout = get_layout_manager()
    
    st.markdown("### 🏢 Real-World Example: Enforce Business Rules with Constraints")
    st.markdown("""
    **Scenario:** Prevent invalid data at database level for e-commerce system
    
    ```sql
    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        sku VARCHAR(50) UNIQUE NOT NULL,  -- Prevent duplicate SKUs
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL CHECK (price > 0),  -- No negative prices
        cost DECIMAL(10, 2) NOT NULL CHECK (cost > 0),
        stock INT DEFAULT 0 CHECK (stock >= 0),  -- No negative inventory
        CONSTRAINT price_higher_than_cost CHECK (price > cost)  -- Price > cost
    );
    
    CREATE TABLE orders (
        id BIGSERIAL PRIMARY KEY,
        customer_id INT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
        status VARCHAR(20) CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled')),
        total DECIMAL(12, 2) NOT NULL CHECK (total >= 0),
        created_at TIMESTAMP NOT NULL,
        shipped_at TIMESTAMP CHECK (shipped_at >= created_at OR shipped_at IS NULL)
    );
    ```
    
    **Why this matters:** Constraints prevent bugs before they happen. Trying to insert price=-100 or stock=-50 gets rejected immediately, not hours later when customers complain.
    """)
    
    tips = [
        "Use PRIMARY KEY on every table - it's essential for data integrity",
        "Define FOREIGN KEYs to maintain referential integrity",
        "Use NOT NULL for required columns to prevent NULL surprises",
        "Add CHECK constraints to enforce business rules at the database level",
        "Name constraints explicitly for easier management",
        "Use ON DELETE CASCADE carefully - test thoroughly first",
        "Use DEFERRABLE constraints when you need to defer checks in transactions",
        "Validate data at application level AND database level",
        "Document constraint purposes in comments",
        "Monitor constraint violations to catch data quality issues early"
    ]
    
    for tip in tips:
        layout.render_tip(tip)
