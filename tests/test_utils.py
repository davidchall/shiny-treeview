"""Tests for utility functions."""

import pytest

from shiny_treeview import TreeItem
from shiny_treeview.utils import duplicate_ids, get_tree_path, stratify


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


class TestStratify:
    """Test the stratify function."""

    def test_simple_tree(self):
        """Test stratifying a simple parent-child tree."""
        items = [
            TreeItem(id="root", label="Root"),
            TreeItem(id="child1", label="Child 1"),
            TreeItem(id="child2", label="Child 2"),
        ]
        parent_ids = [None, "root", "root"]

        result = stratify(items, parent_ids)

        assert len(result) == 1  # One root item
        root = result[0]
        assert root.id == "root"
        assert root.label == "Root"
        assert len(root.children) == 2

        child_ids = [child.id for child in root.children]
        assert "child1" in child_ids
        assert "child2" in child_ids

    def test_multi_level_tree(self):
        """Test stratifying a multi-level tree."""
        items = [
            TreeItem(id="root", label="Root"),
            TreeItem(id="child1", label="Child 1"),
            TreeItem(id="child2", label="Child 2"),
            TreeItem(id="grandchild", label="Grandchild"),
        ]
        parent_ids = [None, "root", "root", "child1"]

        result = stratify(items, parent_ids)

        assert len(result) == 1
        root = result[0]
        assert len(root.children) == 2

        # Find child1 and verify it has grandchild
        child1 = next(child for child in root.children if child.id == "child1")
        assert len(child1.children) == 1
        assert child1.children[0].id == "grandchild"

        # Verify child2 has no children
        child2 = next(child for child in root.children if child.id == "child2")
        assert len(child2.children) == 0

    def test_multiple_roots(self):
        """Test stratifying with multiple root items."""
        items = [
            TreeItem(id="root1", label="Root 1"),
            TreeItem(id="root2", label="Root 2"),
            TreeItem(id="child1", label="Child 1"),
            TreeItem(id="child2", label="Child 2"),
        ]
        parent_ids = [None, None, "root1", "root2"]

        result = stratify(items, parent_ids)

        assert len(result) == 2  # Two root items
        root_ids = [item.id for item in result]
        assert "root1" in root_ids
        assert "root2" in root_ids

        # Verify each root has its correct child
        for root in result:
            if root.id == "root1":
                assert len(root.children) == 1
                assert root.children[0].id == "child1"
            elif root.id == "root2":
                assert len(root.children) == 1
                assert root.children[0].id == "child2"

    def test_disabled_items(self):
        """Test that disabled property is preserved."""
        items = [
            TreeItem(id="root", label="Root", disabled=True),
            TreeItem(id="child", label="Child", disabled=False),
        ]
        parent_ids = [None, "root"]

        result = stratify(items, parent_ids)

        assert len(result) == 1
        root = result[0]
        assert root.disabled is True
        assert root.children[0].disabled is False

    def test_empty_input(self):
        """Test stratifying empty lists."""
        result = stratify([], [])
        assert result == []

    def test_mismatched_lengths(self):
        """Test error when items and parent_ids have different lengths."""
        items = [TreeItem(id="root", label="Root")]
        parent_ids = [None, "root"]  # Too many parent_ids

        with pytest.raises(
            ValueError, match="items and parent_ids lists must have the same length"
        ):
            stratify(items, parent_ids)

    def test_duplicate_ids(self):
        """Test error when TreeItem IDs are not unique."""
        items = [
            TreeItem(id="duplicate", label="First"),
            TreeItem(id="duplicate", label="Second"),
        ]
        parent_ids = [None, None]

        with pytest.raises(ValueError, match="All TreeItem IDs must be unique"):
            stratify(items, parent_ids)

    def test_invalid_parent_id(self):
        """Test error when parent_id references non-existent item."""
        items = [TreeItem(id="child", label="Child")]
        parent_ids = ["nonexistent"]

        with pytest.raises(
            ValueError,
            match="Parent ID 'nonexistent' at index 0 does not reference an existing item",
        ):
            stratify(items, parent_ids)

    def test_circular_reference(self):
        """Test error when circular references are detected."""
        items = [
            TreeItem(id="a", label="A"),
            TreeItem(id="b", label="B"),
            TreeItem(id="c", label="C"),
        ]
        parent_ids = ["b", "c", "a"]  # a -> b -> c -> a (circular)

        with pytest.raises(ValueError, match="Circular reference detected"):
            stratify(items, parent_ids)

    def test_original_items_unchanged(self):
        """Test that original TreeItem objects are not modified."""
        original_items = [
            TreeItem(id="root", label="Root"),
            TreeItem(id="child", label="Child"),
        ]
        parent_ids = [None, "root"]

        # Store original children references
        original_children = [item.children for item in original_items]

        result = stratify(original_items, parent_ids)

        # Original items should be unchanged
        for i, item in enumerate(original_items):
            assert item.children is original_children[i]
            assert len(item.children) == 0  # Should still be empty

        # Result should have populated children
        assert len(result[0].children) == 1

    def test_complex_tree_structure(self):
        """Test a more complex tree structure similar to file system."""
        items = [
            TreeItem(id="documents", label="📁 Documents"),
            TreeItem(id="downloads", label="📁 Downloads"),
            TreeItem(id="doc1", label="📄 Report.pdf"),
            TreeItem(id="doc2", label="📄 Presentation.pptx"),
            TreeItem(id="archive", label="📁 Archive"),
            TreeItem(id="archive1", label="📄 Old_Report.pdf"),
            TreeItem(id="download1", label="📦 software.zip"),
        ]
        parent_ids = [
            None,
            None,
            "documents",
            "documents",
            "documents",
            "archive",
            "downloads",
        ]

        result = stratify(items, parent_ids)

        assert len(result) == 2  # documents and downloads

        # Find documents folder
        documents = next(item for item in result if item.id == "documents")
        assert len(documents.children) == 3  # doc1, doc2, archive

        # Find archive subfolder
        archive = next(child for child in documents.children if child.id == "archive")
        assert len(archive.children) == 1  # archive1

        # Find downloads folder
        downloads = next(item for item in result if item.id == "downloads")
        assert len(downloads.children) == 1  # download1
