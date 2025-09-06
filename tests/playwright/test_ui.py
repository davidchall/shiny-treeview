from playwright.sync_api import Page
from shiny.playwright.controller import OutputCode
from shiny.run import ShinyAppProc

from .controller import InputTreeView


class TestUserInteractions:
    """Tests for user interactions."""

    def test_initial_selection(self, page: Page, local_app: ShinyAppProc):
        """Test the InputTreeView controller methods."""
        page.goto(local_app.url)

        single_default = InputTreeView(page, "single_default")
        single_default_txt = OutputCode(page, "single_default_txt")
        single_default.expect_multiple(False)
        single_default.expect_selected(None)
        single_default.expect_expanded(None)
        single_default.expect_disabled(None)
        single_default_txt.expect_value("None")

        multi_default = InputTreeView(page, "multi_default")
        multi_default_txt = OutputCode(page, "multi_default_txt")
        multi_default.expect_multiple(True)
        multi_default.expect_selected(None)
        multi_default.expect_expanded(None)
        multi_default.expect_disabled(None)
        multi_default_txt.expect_value("None")

        single_with_selected = InputTreeView(page, "single_with_selected")
        single_with_selected_txt = OutputCode(page, "single_with_selected_txt")
        single_with_selected.expect_multiple(False)
        single_with_selected.expect_selected("file1")
        single_with_selected.expect_expanded("folder1")
        single_with_selected.expect_disabled(None)
        single_with_selected_txt.expect_value("file1")

        multi_with_selected = InputTreeView(page, "multi_with_selected")
        multi_with_selected_txt = OutputCode(page, "multi_with_selected_txt")
        multi_with_selected.expect_multiple(True)
        multi_with_selected.expect_selected(["file1", "file3"])
        multi_with_selected.expect_expanded(["folder1", "folder2"])
        multi_with_selected.expect_disabled("file4")
        multi_with_selected_txt.expect_value("('file1', 'file3')")

    def test_interact_single(self, page: Page, local_app: ShinyAppProc):
        """Test interactions with the single-select treeview."""
        page.goto(local_app.url)

        tree = InputTreeView(page, "single_default")
        tree_txt = OutputCode(page, "single_default_txt")

        tree.select_single("standalone")
        tree.expect_expanded(None)
        tree.expect_selected("standalone")
        tree_txt.expect_value("standalone")

        tree.select_single("folder1")
        tree.select_single("file2")
        tree.expect_expanded("folder1")
        tree.expect_selected("file2")
        tree_txt.expect_value("file2")

        tree.select_multiple(["file1", "file2"])
        tree.expect_selected("file2")
        tree_txt.expect_value("file2")

        tree.select_range("file2", "file1")
        tree.expect_selected("file1")
        tree_txt.expect_value("file1")

    def test_interact_multi(self, page: Page, local_app: ShinyAppProc):
        """Test interactions with the multi-select treeview."""
        page.goto(local_app.url)

        tree = InputTreeView(page, "multi_default")
        tree_txt = OutputCode(page, "multi_default_txt")

        tree.select_single("standalone")
        tree.expect_expanded(None)
        tree.expect_selected("standalone")
        tree_txt.expect_value("('standalone',)")

        tree.select_single("folder1")
        tree.select_single("file2")
        tree.expect_expanded("folder1")
        tree.expect_selected("file2")
        tree_txt.expect_value("('file2',)")

        tree.select_single("folder2")
        tree.select_multiple(["file1", "file3"])
        tree.expect_expanded(["folder1", "folder2"])
        tree.expect_selected(["file1", "file3"])
        tree_txt.expect_value("('file1', 'file3')")

        tree.select_range("file1", "file2")
        tree.expect_expanded(["folder1", "folder2"])
        tree.expect_selected(["file1", "file2"])
        tree_txt.expect_value("('file1', 'file2')")

        tree.select_range("file1", "file3")
        tree.expect_expanded(["folder1", "folder2"])
        tree.expect_selected(["file1", "file2", "subfolder1", "folder2", "file3"])
        tree_txt.expect_value("('file1', 'file2', 'file3', 'folder2', 'subfolder1')")


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
