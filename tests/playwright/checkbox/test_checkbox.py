"""Tests for checkbox treeview features."""

import pytest
from playwright.sync_api import Page
from shiny.playwright.controller import OutputCode
from shiny.run import ShinyAppProc

from shiny_treeview.playwright import InputTreeView


class TestShinyIntegration:
    """Integration tests with Shiny app."""

    def test_initial_selection(self, page: Page, local_app: ShinyAppProc):
        """Test that selected items are setup correctly."""
        page.goto(local_app.url)

        single_default = InputTreeView(page, "single_default")
        single_default_txt = OutputCode(page, "single_default_txt")
        single_default.expect_selected(None)
        single_default.expect_expanded(None)
        single_default.expect_multiple(False)
        single_default.expect_checkbox(True)
        single_default_txt.expect_value("None")

        multi_default = InputTreeView(page, "multi_default")
        multi_default_txt = OutputCode(page, "multi_default_txt")
        multi_default.expect_selected(None)
        multi_default.expect_expanded(None)
        multi_default.expect_multiple(True)
        multi_default.expect_checkbox(True)
        multi_default_txt.expect_value("None")

        single_with_selected = InputTreeView(page, "single_with_selected")
        single_with_selected_txt = OutputCode(page, "single_with_selected_txt")
        single_with_selected.expect_selected("file1")
        single_with_selected.expect_expanded("folder1")
        single_with_selected.expect_multiple(False)
        single_with_selected.expect_checkbox(True)
        single_with_selected_txt.expect_value("file1")

        multi_with_selected = InputTreeView(page, "multi_with_selected")
        multi_with_selected_txt = OutputCode(page, "multi_with_selected_txt")
        multi_with_selected.expect_selected(["file1", "file3"])
        multi_with_selected.expect_expanded(["folder1", "folder2"])
        multi_with_selected.expect_multiple(True)
        multi_with_selected.expect_checkbox(True)
        multi_with_selected_txt.expect_value("('file1', 'file3')")

    def test_interact_single(self, page: Page, local_app: ShinyAppProc):
        """Test interactions with the single-select treeview."""
        page.goto(local_app.url)

        tree = InputTreeView(page, "single_default")
        tree_txt = OutputCode(page, "single_default_txt")

        tree.select("standalone")
        tree.expect_expanded(None)
        tree.expect_selected("standalone")
        tree_txt.expect_value("standalone")

        tree.expand("folder1")
        tree.expect_selected("standalone")
        tree.select("file2")
        tree.expect_expanded("folder1")
        tree.expect_selected("file2")
        tree_txt.expect_value("file2")

        tree.select(["file1", "file2"])
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

        tree.select("standalone")
        tree.expect_expanded(None)
        tree.expect_selected("standalone")
        tree_txt.expect_value("('standalone',)")

        tree.expand("folder1")
        tree.expect_selected("standalone")
        tree.select("file2")
        tree.expect_expanded("folder1")
        tree.expect_selected(["file2", "standalone"])
        tree_txt.expect_value("('file2', 'standalone')")

        tree.expand("folder2")
        tree.expect_selected(["file2", "standalone"])
        tree.select(["file1", "file3"])
        tree.expect_expanded(["folder1", "folder2"])
        tree.expect_selected(["file1", "file2", "file3", "standalone"])
        tree_txt.expect_value("('file1', 'file2', 'file3', 'standalone')")

        tree.select(["file1", "file2", "file3", "standalone"])
        tree.expect_selected(None)

        tree.select_range("file1", "file2")
        tree.expect_expanded(["folder1", "folder2"])
        tree.expect_selected(["file1", "file2"])
        tree_txt.expect_value("('file1', 'file2')")

        tree.select_range("file1", "file3")
        tree.expect_expanded(["folder1", "folder2"])
        tree.expect_selected(["file1", "file2", "subfolder1", "folder2", "file3"])
        tree_txt.expect_value("('file1', 'file2', 'file3', 'folder2', 'subfolder1')")

    def test_interact_parent(self, page: Page, local_app: ShinyAppProc):
        """Test interactions with parent tree items."""
        page.goto(local_app.url)

        tree = InputTreeView(page, "multi_default")

        tree.select("folder1")
        tree.expect_selected("folder1")
        tree.expect_expanded(None)
        tree.select("folder1")
        tree.expect_selected(None)
        tree.expect_expanded(None)

        tree.expand("folder1")
        tree.expect_selected(None)
        tree.expect_expanded("folder1")

        tree.select("folder1")
        tree.expect_selected("folder1")
        tree.expect_expanded("folder1")
        tree.select("folder1")
        tree.expect_selected(None)
        tree.expect_expanded("folder1")

        tree.select("subfolder1")
        tree.expect_selected("subfolder1")
        tree.expect_expanded("folder1")
        tree.select("subfolder1")
        tree.expect_selected(None)
        tree.expect_expanded("folder1")

        tree.expand("subfolder1")
        tree.expect_selected(None)
        tree.expect_expanded(["folder1", "subfolder1"])
        tree.expand("subfolder1")
        tree.expect_selected(None)
        tree.expect_expanded("folder1")

        tree.expand("folder1")
        tree.expect_selected(None)
        tree.expect_expanded(None)


@pytest.mark.snapshot
class TestVisualSnapshot:
    """Snapshot tests using component screenshots."""

    def test_none(self, page: Page, local_app: ShinyAppProc, assert_snapshot):
        """Snapshot test with no items selected or expanded."""
        page.goto(local_app.url)

        single_default = InputTreeView(page, "single_default")
        assert_snapshot(single_default.loc.screenshot())

    def test_single(self, page: Page, local_app: ShinyAppProc, assert_snapshot):
        """Snapshot test with one item selected and expanded."""
        page.goto(local_app.url)

        single_default = InputTreeView(page, "single_with_selected")
        assert_snapshot(single_default.loc.screenshot())

    def test_multi(self, page: Page, local_app: ShinyAppProc, assert_snapshot):
        """Snapshot test with multiple items selected and expanded."""
        page.goto(local_app.url)

        multi_default = InputTreeView(page, "multi_with_selected")
        assert_snapshot(multi_default.loc.screenshot())
