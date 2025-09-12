"""Tests for disabled items in the treeview."""

import pytest
from playwright.sync_api import Page
from shiny.run import ShinyAppProc

from shiny_treeview.playwright import InputTreeView


class TestShinyIntegration:
    """Integration tests with Shiny app."""

    def test_disabled_items(self, page: Page, local_app: ShinyAppProc):
        """Test that disabled items are setup correctly."""
        page.goto(local_app.url)

        treeview = InputTreeView(page, "my_treeview")
        treeview.expect_disabled("file2")

    def test_cannot_select_disabled(self, page: Page, local_app: ShinyAppProc):
        """Test that disabled items cannot be selected."""
        page.goto(local_app.url)

        treeview = InputTreeView(page, "my_treeview")
        treeview.select("file2")
        treeview.expect_selected("file1")


@pytest.mark.snapshot
class TestVisualSnapshot:
    """Snapshot tests using component screenshots."""

    def test_disabled(self, page: Page, local_app: ShinyAppProc, assert_snapshot):
        """Snapshot test with disabled items."""
        page.goto(local_app.url)

        treeview = InputTreeView(page, "my_treeview")
        assert_snapshot(treeview.loc.screenshot())
