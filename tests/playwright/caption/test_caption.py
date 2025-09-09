"""Tests for TreeItem caption functionality."""

import pytest
from playwright.sync_api import Page
from shiny.run import ShinyAppProc

from shiny_treeview.playwright import InputTreeView


@pytest.mark.snapshot
class TestVisualSnapshot:
    """Snapshot tests using component screenshots."""

    def test_caption_display(
        self, page: Page, local_app: ShinyAppProc, assert_snapshot
    ):
        """Snapshot test with tree item captions."""
        page.goto(local_app.url)

        tree = InputTreeView(page, "my_treeview")
        assert_snapshot(tree.loc.screenshot())
