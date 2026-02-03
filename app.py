"""
PostgreSQL Cheatsheet 📘
A comprehensive, interactive guide to PostgreSQL commands and best practices.
Built with Streamlit for an optimal developer experience.

Inspired by the Snowflake Cheatsheet model with professional layout and organization.
"""

import streamlit as st
from typing import List, Callable

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="PostgreSQL Cheatsheet 📘",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "PostgreSQL Cheatsheet - Your favorite reference guide! 🚀"
    }
)

# ============================================================================
# Custom CSS for Enhanced UI
# ============================================================================

st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
            text-align: center;
        }
        .header-container h1 {
            margin: 0;
            font-size: 2.5rem;
        }
        .header-container p {
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .logo-container {
            text-align: center;
            padding: 1rem;
            font-size: 4rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# Import Segment Functions
# ============================================================================

def import_segments() -> dict:
    """
    Dynamically import all segment modules.
    
    Returns:
        dict: Mapping of segment names to their render functions
    """
    segments = {}
    
    # Import all segment modules
    try:
        from segments import (
            database, schema, table, view, materialized_view,
            index, constraints, data_types, insert, update, delete,
            select, joins, aggregation, functions, procedures,
            triggers, transactions, roles_users, permissions,
            extensions, backup_restore, performance, partitioning,
            json_data, full_text_search, replication, monitoring
        )
        
        segment_modules = [
            ("🔤 Data Types", data_types),
            ("🗄️ Database", database),
            ("📂 Schema", schema),
            ("📊 Table", table),
            ("🔐 Constraints", constraints),
            ("⚡ Index", index),
            ("➕ Insert", insert),
            ("🔍 Select", select),
            ("✏️ Update", update),
            ("🗑️ Delete", delete),
            ("🔗 Joins", joins),
            ("📊 Aggregation", aggregation),
            ("⚙️ Functions", functions),
            ("📋 JSON", json_data),
            ("👁️ View", view),
            ("📸 Materialized View", materialized_view),
            ("📂 Partitioning", partitioning),
            ("⚡ Performance", performance),
            ("⚙️ Advanced Functions", functions),
            ("🔧 Procedures", procedures),
            ("⚡ Triggers", triggers),
            ("🔄 Transactions", transactions),
            ("👥 Roles & Users", roles_users),
            ("🔑 Permissions", permissions),
            ("💾 Backup & Restore", backup_restore),
            ("🧩 Extensions", extensions),
            ("🔎 Full Text Search", full_text_search),
            ("🔄 Replication", replication),
            ("📊 Monitoring", monitoring),
        ]
        
        for name, module in segment_modules:
            if hasattr(module, "render_segment"):
                segments[name] = module.render_segment
                
    except ImportError as e:
        st.error(f"Error importing segments: {e}")
        
    return segments

# ============================================================================
# Helper Functions
# ============================================================================

def render_logo_header() -> None:
    """Render the logo and header."""
    import os
    
    # Try to load PostgreSQL logo image
    logo_path = "logo/postgresql_logo.png"
    
    try:
        if os.path.exists(logo_path) and os.path.getsize(logo_path) > 0:
            st.image(logo_path, width='stretch')
        else:
            raise FileNotFoundError("Logo file not found or empty")
    except Exception as e:
        # Fallback to emoji header if image fails to load
        st.markdown("""
            <div class="header-container">
                <h1>🐘 PostgreSQL Cheatsheet 📘</h1>
                <p>Your comprehensive reference guide to PostgreSQL • Master databases with confidence</p>
            </div>
        """, unsafe_allow_html=True)


def default_layout(left_defaults: List[str], right_defaults: List[str]) -> None:
    """
    Reset to default layout.
    
    Args:
        left_defaults: Default segments for left column
        right_defaults: Default segments for right column
    """
    st.session_state.layout_left_column = left_defaults
    st.session_state.layout_right_column = right_defaults
    st.rerun()


def render_sidebar() -> str:
    """
    Render sidebar navigation.
    
    Returns:
        str: Selected segment name or "all" to show all
    """
    # Get all available segments
    segments = import_segments()
    all_segments = list(segments.keys())
    
    st.sidebar.markdown("---")
    
    # Navigation Section - Table of Contents
    st.sidebar.subheader("📑 Table of Contents")
    
    # Show all segments
    selected = st.sidebar.radio(
        "Select a topic to explore:",
        options=["📚 All Topics"] + all_segments,
        index=0,
        key="selected_segment"
    )
    
    st.sidebar.markdown("---")
    
    # Legend Section
    with st.sidebar.expander("� Legend", expanded=True):
        st.markdown("""
        - Text inside `[ BRACKETS ]` indicates *optional parameters* that can be omitted. Drop carefully!
        - Text inside `{ CURLY | BRACKETS }` indicates *available options* for the command. Choose wisely!   
        - Text inside `< angle.brackets >` indicates *entity names* (e.g. table, schema, etc.). Pick responsibly!
        - `--` indicates SQL comments
        - `;` indicates statement terminator
        """)
    
    st.sidebar.markdown("---")
    
    # How to Use Section
    with st.sidebar.expander("📖 How to Use This Cheat Sheet"):
        st.markdown("""
        **Quick Start:**
        
        1. **Browse Topics**: Select from the table of contents above
        2. **Copy Snippets**: Click the copy icon on any code block
        3. **Learn Tips**: Each section has best practices and gotchas
        4. **Test Safely**: Always test queries in a development environment
        
        **Pro Tips:**
        - 🔍 Use Ctrl+F to search within the page
        - 💾 Bookmark this page for quick reference
        - ⚡ Test all queries in dev environment first
        - 📚 Read the tips section for each topic
        """)
    
    st.sidebar.markdown("---")
    
    # Info Section
    st.sidebar.info("""
    This online cheatsheet for PostgreSQL is based on materials from the [PostgreSQL documentation website](https://www.postgresql.org/docs/). 
    This cheatsheet is community-driven and not officially affiliated with the PostgreSQL Global Development Group. 
    Please refer to the official PostgreSQL documentation for detailed information and updates.
    """)
    
    st.sidebar.markdown("---")
    
    # Footer
    st.sidebar.markdown("""
    **PostgreSQL Cheatsheet v2.0**
    
    Made with ❤️ for the PostgreSQL community
    
    *Powered by Saravanakumar - AWS Developer*
    """)
    
    return selected

# ============================================================================
# Main Application
# ============================================================================

def main() -> None:
    """Main application entry point."""
    
    # Render logo and header
    render_logo_header()
    
    # "How to Use" section with expander
    _, exp_col, _ = st.columns([1, 6, 1])
    with exp_col:
        with st.expander("**📖 A Developer's Guide to PostgreSQL Commands**"):
            st.markdown("""
                Use it however you like! 🤷
                
                Here's my recommendation:
                
                In a typical PostgreSQL work session, you might find yourself juggling various commands such as 
                creating databases and schemas, designing tables, manipulating data, querying results, managing users and permissions, 
                optimizing performance, setting up replication, and much more!
                
                Now, keeping the precise syntax of all these commands at your fingertips, especially for the less-frequently-used ones, 
                can be quite a challenge. I recommend keeping this cheat sheet open in a tab while you work. This way, you can swiftly 
                refer to the provided code snippets and easily adapt them to your specific tasks.
                
                Within each segment, you'll find best practices tips ⚡: a bonus section to elevate your PostgreSQL skills. 
                I suggest that whenever you are using a command for the first time, spend a few minutes reading the tips and hopefully pick up something new.
                """)
            
            st.info("""
                This guide is not intended to be a replacement for the official [PostgreSQL documentation](https://www.postgresql.org/docs/) 
                (which is fantastic by the way!). For a comprehensive reference of all objects and methods, make sure to explore the official documentation.
                """)
            
            st.markdown("""
                If you happen to spot any errors or have suggestions for improving the descriptions or tips, please don't hesitate to reach out. 
                Your feedback is invaluable in keeping this guide accurate and useful.
                
                👈 Don't forget to check the sidebar for additional options!
                
                Now, go build something awesome with PostgreSQL! 🚀
                """)
    
    st.sidebar.title("🐘 PostgreSQL Cheatsheet")
    st.sidebar.caption("A comprehensive PostgreSQL reference guide for developers")
    
    selected = render_sidebar()
    
    # Import segments
    segments = import_segments()
    all_segments = list(segments.keys())
    
    # Display content based on selection
    if selected == "📚 All Topics":
        # Show all topics
        for seg_name in all_segments:
            if seg_name in segments:
                try:
                    segments[seg_name]()
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Error rendering {seg_name}: {str(e)}")
    else:
        # Show specific selected topic
        if selected in segments:
            try:
                segments[selected]()
            except Exception as e:
                st.error(f"Error rendering {selected}: {str(e)}")

# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    main()
