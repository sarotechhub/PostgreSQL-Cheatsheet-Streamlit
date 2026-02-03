"""
Utility functions for PostgreSQL Cheatsheet
Provides helper functions for rendering code blocks, tabs, and other UI elements.
"""

import streamlit as st
from typing import List, Callable


def st_code_block(
    code_id: str,
    description: str,
    code: str,
    language: str = "sql"
) -> None:
    """
    Render a code block with description and copy functionality.
    
    Args:
        code_id: Unique identifier for the code block
        description: Description of what the code does
        code: The code to display
        language: Programming language (default: sql)
    """
    st.write(f"**{description}**")
    st.code(code, language=language)


def make_tabs(tab_names: List[str]) -> tuple:
    """
    Create multiple tabs.
    
    Args:
        tab_names: List of tab names
        
    Returns:
        tuple: Tuple of tab containers
    """
    tabs = st.tabs(tab_names)
    return tuple(tabs)


def render_tip(tip_text: str, icon: str = "💡") -> None:
    """
    Render a tip box.
    
    Args:
        tip_text: The tip text to display
        icon: Emoji icon to use
    """
    st.info(f"{icon} **Tip:** {tip_text}")


def render_warning(warning_text: str, icon: str = "⚠️") -> None:
    """
    Render a warning box.
    
    Args:
        warning_text: The warning text to display
        icon: Emoji icon to use
    """
    st.warning(f"{icon} **Warning:** {warning_text}")


def render_doc_link(doc_url: str, link_text: str = "📖 Official Docs") -> None:
    """
    Render a link to documentation.
    
    Args:
        doc_url: URL to documentation
        link_text: Text to display for the link
    """
    st.markdown(f"[{link_text}]({doc_url})")
