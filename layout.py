"""
Layout management system for PostgreSQL Cheatsheet app.
Handles multi-column layouts and responsive design.
"""

import streamlit as st
from typing import Callable, List


class LayoutManager:
    """Manages layout rendering for cheatsheet segments."""

    def __init__(self):
        """Initialize layout manager."""
        self.left_column = None
        self.right_column = None

    def setup_two_column_layout(self) -> tuple:
        """
        Create a two-column layout.
        
        Returns:
            tuple: (left_column, right_column) containers
        """
        left, right = st.columns([1, 1])
        self.left_column = left
        self.right_column = right
        return left, right

    def render_segment_single_column(self, segment_func: Callable) -> None:
        """
        Render a segment in single column mode.
        
        Args:
            segment_func: Function that renders the segment
        """
        segment_func()

    def render_segment_two_columns(self, segment_func: Callable, position: str = "left") -> None:
        """
        Render a segment in two-column mode.
        
        Args:
            segment_func: Function that renders the segment
            position: "left" or "right" column position
        """
        if position == "left" and self.left_column:
            with self.left_column:
                segment_func()
        elif position == "right" and self.right_column:
            with self.right_column:
                segment_func()
        else:
            segment_func()

    @staticmethod
    def render_code_block(
        sql_code: str,
        language: str = "sql",
        title: str = ""
    ) -> None:
        """
        Render a code block with copy button.
        
        Args:
            sql_code: Code content
            language: Programming language
            title: Optional title for code block
        """
        if title:
            st.subheader(title)
        st.code(sql_code, language=language)

    @staticmethod
    def render_expandable_section(
        title: str,
        content_func: Callable,
        expanded: bool = False
    ) -> None:
        """
        Render an expandable section.
        
        Args:
            title: Section title
            content_func: Function that renders content
            expanded: Whether section starts expanded
        """
        with st.expander(title, expanded=expanded):
            content_func()

    @staticmethod
    def render_tip(tip_text: str, icon: str = "💡") -> None:
        """
        Render a tip/note box.
        
        Args:
            tip_text: Tip content
            icon: Emoji icon prefix
        """
        st.info(f"{icon} **Tip:** {tip_text}")

    @staticmethod
    def render_warning(warning_text: str, icon: str = "⚠️") -> None:
        """
        Render a warning box.
        
        Args:
            warning_text: Warning content
            icon: Emoji icon prefix
        """
        st.warning(f"{icon} **Warning:** {warning_text}")

    @staticmethod
    def render_success(success_text: str, icon: str = "✅") -> None:
        """
        Render a success message box.
        
        Args:
            success_text: Success content
            icon: Emoji icon prefix
        """
        st.success(f"{icon} {success_text}")

    @staticmethod
    def render_section_header(title: str, level: int = 2) -> None:
        """
        Render a section header.
        
        Args:
            title: Header text
            level: Header level (1-3)
        """
        if level == 1:
            st.header(title)
        elif level == 2:
            st.subheader(title)
        else:
            st.markdown(f"### {title}")


def get_layout_manager() -> LayoutManager:
    """
    Get or create layout manager singleton.
    
    Returns:
        LayoutManager: Shared layout manager instance
    """
    if "layout_manager" not in st.session_state:
        st.session_state.layout_manager = LayoutManager()
    return st.session_state.layout_manager
