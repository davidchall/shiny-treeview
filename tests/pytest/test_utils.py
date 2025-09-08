"""Tests for utility functions."""

from shiny_treeview import TreeItem
from shiny_treeview.utils import duplicate_ids, get_tree_path


def test_get_tree_path():
    """Test the get_tree_path function with various scenarios."""
    # Create test tree structure
    tree_data = [
        TreeItem(
            id="folder1",
            label="Folder 1",
            children=[
                TreeItem(id="file1", label="File 1"),
                TreeItem(id="file2", label="File 2"),
                TreeItem(
                    id="subfolder1",
                    label="Subfolder 1",
                    children=[
                        TreeItem(id="subfile1", label="Subfile 1"),
                        TreeItem(id="subfile2", label="Subfile 2"),
                    ],
                ),
            ],
        ),
        TreeItem(
            id="folder2",
            label="Folder 2",
            children=[
                TreeItem(id="file3", label="File 3"),
                TreeItem(id="file4", label="File 4", disabled=True),
            ],
        ),
        TreeItem(id="standalone", label="Standalone File"),
    ]

    # Test root level item
    assert get_tree_path(tree_data, "standalone") == ("standalone",)
    assert get_tree_path(tree_data, "folder1") == ("folder1",)

    # Test nested items
    assert get_tree_path(tree_data, "file1") == ("folder1", "file1")
    assert get_tree_path(tree_data, "file3") == ("folder2", "file3")
    assert get_tree_path(tree_data, "subfolder1") == ("folder1", "subfolder1")

    # Test deeply nested items
    assert get_tree_path(tree_data, "subfile1") == ("folder1", "subfolder1", "subfile1")
    assert get_tree_path(tree_data, "subfile2") == ("folder1", "subfolder1", "subfile2")

    # Test disabled item
    assert get_tree_path(tree_data, "file4") == ("folder2", "file4")

    # Test non-existent item
    assert get_tree_path(tree_data, "nonexistent") is None

    # Test empty tree
    assert get_tree_path([], "anything") is None


def test_duplicate_ids():
    """Test detection of duplicate IDs in tree structures."""
    # Test valid tree with unique IDs
    valid_tree = [
        TreeItem(
            id="folder1",
            label="Folder 1",
            children=[
                TreeItem(id="file1", label="File 1"),
                TreeItem(id="file2", label="File 2"),
            ],
        ),
        TreeItem(id="folder2", label="Folder 2"),
    ]

    # Should return empty list for unique IDs
    result = duplicate_ids(valid_tree)
    assert result == []

    # Test tree with duplicate IDs at same level
    duplicate_same_level = [
        TreeItem(id="folder1", label="Folder 1"),
        TreeItem(id="folder1", label="Duplicate Folder"),
    ]

    result = duplicate_ids(duplicate_same_level)
    assert result == ["folder1"]

    # Test tree with duplicate IDs across levels
    duplicate_cross_level = [
        TreeItem(
            id="folder1",
            label="Folder 1",
            children=[
                TreeItem(id="folder1", label="Same ID as parent"),
                TreeItem(id="file1", label="File 1"),
            ],
        ),
        TreeItem(id="folder2", label="Folder 2"),
    ]

    result = duplicate_ids(duplicate_cross_level)
    assert result == ["folder1"]

    # Test tree with multiple duplicate IDs
    multiple_duplicates = [
        TreeItem(id="item1", label="Item 1"),
        TreeItem(id="item1", label="Duplicate Item 1"),
        TreeItem(
            id="folder1",
            label="Folder 1",
            children=[
                TreeItem(id="item2", label="Item 2"),
                TreeItem(id="item2", label="Duplicate Item 2"),
                TreeItem(id="folder1", label="Duplicate Folder"),
            ],
        ),
    ]

    result = duplicate_ids(multiple_duplicates)
    assert sorted(result) == ["folder1", "item1", "item2"]

    # Test deeply nested duplicates
    deep_duplicates = [
        TreeItem(
            id="root",
            label="Root",
            children=[
                TreeItem(
                    id="level1",
                    label="Level 1",
                    children=[
                        TreeItem(
                            id="level2",
                            label="Level 2",
                            children=[
                                TreeItem(id="deep_item", label="Deep Item"),
                            ],
                        ),
                    ],
                ),
                TreeItem(id="deep_item", label="Duplicate Deep Item"),
            ],
        ),
    ]

    result = duplicate_ids(deep_duplicates)
    assert result == ["deep_item"]

    # Test empty tree
    result = duplicate_ids([])
    assert result == []

    # Test single item (no duplicates possible)
    single_item = [TreeItem(id="single", label="Single Item")]
    result = duplicate_ids(single_item)
    assert result == []
