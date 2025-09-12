"""Tests for treeview components inside Shiny modules."""

import pytest
from playwright.sync_api import Page
from shiny.playwright.controller import OutputText
from shiny.run import ShinyAppProc

from shiny_treeview.playwright import InputTreeView


class TestShinyIntegration:
    """Integration tests with Shiny app."""

    def test_multiple_modules_independence(self, page: Page, local_app: ShinyAppProc):
        """Test that multiple module instances work independently."""
        page.goto(local_app.url)

        file_tree = InputTreeView(page, "file_module-tree")
        settings_tree = InputTreeView(page, "settings_module-config_tree")
        nav_tree = InputTreeView(page, "nav_module-nav_tree")

        # Verify initial selections
        file_tree.expect_selected("doc1.pdf")
        settings_tree.expect_selected("theme")
        nav_tree.expect_selected(["overview", "users"])

        # Change file browser selection, others unchanged
        file_tree.select("doc2.docx")
        file_tree.expect_selected("doc2.docx")
        settings_tree.expect_selected("theme")
        nav_tree.expect_selected(["overview", "users"])

        # Change settings selection, others unchanged
        settings_tree.select("language")
        settings_tree.expect_selected("language")
        file_tree.expect_selected("doc2.docx")
        nav_tree.expect_selected(["overview", "users"])

    def test_module_outputs_update(self, page: Page, local_app: ShinyAppProc):
        """Test that module outputs update correctly when selections change."""
        page.goto(local_app.url)

        file_tree = InputTreeView(page, "file_module-tree")
        file_text = OutputText(page, "file_module-selected_file")
        settings_tree = InputTreeView(page, "settings_module-config_tree")
        settings_text = OutputText(page, "settings_module-selected_setting")

        # Test file browser output updates
        file_tree.select("readme.txt")
        file_text.expect_value("Selected file: readme.txt")

        # Test settings output updates
        settings_tree.select("security")
        settings_tree.select("encryption")
        settings_text.expect_value("Current setting: encryption")


@pytest.mark.snapshot
class TestVisualSnapshot:
    """Snapshot tests using component screenshots."""

    def test_snapshots(self, page: Page, local_app: ShinyAppProc, assert_snapshot):
        """Snapshot test of the file browser module."""
        page.goto(local_app.url)

        file_tree = InputTreeView(page, "file_module-tree")
        assert_snapshot(file_tree.loc.screenshot())

        settings_tree = InputTreeView(page, "settings_module-config_tree")
        assert_snapshot(settings_tree.loc.screenshot())

        nav_tree = InputTreeView(page, "nav_module-nav_tree")
        assert_snapshot(nav_tree.loc.screenshot())
