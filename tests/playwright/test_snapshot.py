"""Visual snapshot tests for the treeview component."""

from playwright.sync_api import Page
from shiny.run import ShinyAppProc

from .controller import InputTreeView


class TestVisualSnapshot:
    """Snapshot tests using component screenshots."""

    def test_basic(self, page: Page, local_app: ShinyAppProc, assert_snapshot):
        """Test basic features (selected and expanded items)."""
        page.goto(local_app.url)

        single_default = InputTreeView(page, "single_with_selected")
        assert_snapshot(single_default.loc.screenshot())

    def test_disabled(self, page: Page, local_app: ShinyAppProc, assert_snapshot):
        """Test disabled tree item."""
        page.goto(local_app.url)

        single_default = InputTreeView(page, "multi_with_selected")
        assert_snapshot(single_default.loc.screenshot())
