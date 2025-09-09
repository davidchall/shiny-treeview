"""Tests for TreeItem data class validation."""

import pytest

from shiny_treeview import TreeItem


class TestTreeItemValidation:
    """Test TreeItem validation in __post_init__."""

    def test_valid_tree_item(self):
        """Test that valid TreeItem instances are created successfully."""
        # Simple leaf item
        item = TreeItem(id="test_id", label="Test Label")
        assert item.id == "test_id"
        assert item.label == "Test Label"
        assert item.children == []
        assert item.disabled is False

        # Item with all properties
        item_full = TreeItem(
            id="full_item",
            label="Full Item",
            children=[TreeItem(id="child", label="Child")],
            disabled=True,
        )
        assert item_full.id == "full_item"
        assert item_full.label == "Full Item"
        assert len(item_full.children) == 1
        assert item_full.disabled is True

    def test_id_validation(self):
        """Test TreeItem id validation."""
        # Valid IDs
        TreeItem(id="valid_id", label="Label")
        TreeItem(id="valid-id", label="Label")
        TreeItem(id="valid.id", label="Label")
        TreeItem(id="ValidID123", label="Label")
        TreeItem(id="_private", label="Label")

        # Invalid type
        with pytest.raises(ValueError, match="TreeItem id must be a string"):
            TreeItem(id=123, label="Label")

        with pytest.raises(ValueError, match="TreeItem id must be a string"):
            TreeItem(id=None, label="Label")

        # Empty string
        with pytest.raises(
            ValueError, match="TreeItem id cannot be empty or contain whitespace"
        ):
            TreeItem(id="", label="Label")

        # Whitespace characters
        with pytest.raises(
            ValueError, match="TreeItem id cannot be empty or contain whitespace"
        ):
            TreeItem(id="id with space", label="Label")

        with pytest.raises(
            ValueError, match="TreeItem id cannot be empty or contain whitespace"
        ):
            TreeItem(id="id\twith\ttab", label="Label")

        with pytest.raises(
            ValueError, match="TreeItem id cannot be empty or contain whitespace"
        ):
            TreeItem(id="id\nwith\nnewline", label="Label")

        with pytest.raises(
            ValueError, match="TreeItem id cannot be empty or contain whitespace"
        ):
            TreeItem(id=" leading_space", label="Label")

        with pytest.raises(
            ValueError, match="TreeItem id cannot be empty or contain whitespace"
        ):
            TreeItem(id="trailing_space ", label="Label")

    def test_label_validation(self):
        """Test TreeItem label validation."""
        # Valid labels
        TreeItem(id="id", label="Valid Label")
        TreeItem(id="id", label="Label with 🚀 emoji")
        TreeItem(id="id", label="Label with special chars: @#$%^&*()")
        TreeItem(id="id", label=" Label with spaces ")

        # Invalid type
        with pytest.raises(ValueError, match="TreeItem label must be a string"):
            TreeItem(id="id", label=123)

        with pytest.raises(ValueError, match="TreeItem label must be a string"):
            TreeItem(id="id", label=None)

        with pytest.raises(ValueError, match="TreeItem label must be a string"):
            TreeItem(id="id", label=[])

        # Empty or whitespace-only labels
        with pytest.raises(
            ValueError, match="TreeItem label cannot be empty or whitespace only"
        ):
            TreeItem(id="id", label="")

        with pytest.raises(
            ValueError, match="TreeItem label cannot be empty or whitespace only"
        ):
            TreeItem(id="id", label="   ")

        with pytest.raises(
            ValueError, match="TreeItem label cannot be empty or whitespace only"
        ):
            TreeItem(id="id", label="\t\n")

    def test_disabled_validation(self):
        """Test TreeItem disabled validation."""
        # Valid disabled values
        TreeItem(id="id", label="Label", disabled=True)
        TreeItem(id="id", label="Label", disabled=False)

        # Invalid type
        with pytest.raises(ValueError, match="TreeItem disabled must be a boolean"):
            TreeItem(id="id", label="Label", disabled="true")

        with pytest.raises(ValueError, match="TreeItem disabled must be a boolean"):
            TreeItem(id="id", label="Label", disabled=1)

        with pytest.raises(ValueError, match="TreeItem disabled must be a boolean"):
            TreeItem(id="id", label="Label", disabled=None)

    def test_children_validation(self):
        """Test TreeItem children validation."""
        # Valid children
        child1 = TreeItem(id="child1", label="Child 1")
        child2 = TreeItem(id="child2", label="Child 2")

        TreeItem(id="parent", label="Parent", children=[])
        TreeItem(id="parent", label="Parent", children=[child1])
        TreeItem(id="parent", label="Parent", children=[child1, child2])

        # Invalid type
        with pytest.raises(ValueError, match="TreeItem children must be a list"):
            TreeItem(id="id", label="Label", children="not a list")

        with pytest.raises(ValueError, match="TreeItem children must be a list"):
            TreeItem(id="id", label="Label", children=None)

        with pytest.raises(ValueError, match="TreeItem children must be a list"):
            TreeItem(id="id", label="Label", children=child1)

        # Invalid children elements
        with pytest.raises(
            ValueError, match="TreeItem children\\[0\\] must be a TreeItem instance"
        ):
            TreeItem(id="id", label="Label", children=["not a TreeItem"])

        with pytest.raises(
            ValueError, match="TreeItem children\\[1\\] must be a TreeItem instance"
        ):
            TreeItem(id="id", label="Label", children=[child1, "invalid"])

        with pytest.raises(
            ValueError, match="TreeItem children\\[0\\] must be a TreeItem instance"
        ):
            TreeItem(id="id", label="Label", children=[{"id": "dict", "label": "Dict"}])

    def test_nested_validation(self):
        """Test that validation works for nested TreeItem structures."""
        # Valid nested structure
        leaf1 = TreeItem(id="leaf1", label="Leaf 1")
        leaf2 = TreeItem(id="leaf2", label="Leaf 2")
        branch = TreeItem(id="branch", label="Branch", children=[leaf1, leaf2])
        root = TreeItem(id="root", label="Root", children=[branch])

        assert root.id == "root"
        assert len(root.children) == 1
        assert root.children[0].id == "branch"
        assert len(root.children[0].children) == 2

        # Invalid nested structure - child with invalid ID
        with pytest.raises(
            ValueError, match="TreeItem id cannot be empty or contain whitespace"
        ):
            TreeItem(
                id="root",
                label="Root",
                children=[
                    TreeItem(id="valid", label="Valid"),
                    TreeItem(id="invalid id", label="Invalid"),  # Space in ID
                ],
            )

        # Invalid nested structure - grandchild with invalid label
        with pytest.raises(
            ValueError, match="TreeItem label cannot be empty or whitespace only"
        ):
            TreeItem(
                id="root",
                label="Root",
                children=[
                    TreeItem(
                        id="parent",
                        label="Parent",
                        children=[TreeItem(id="child", label="")],  # Empty label
                    )
                ],
            )


class TestTreeItemToDict:
    """Test TreeItem._to_dict() method."""

    def test_simple_item_to_dict(self):
        """Test converting simple TreeItem to dict."""
        item = TreeItem(id="test", label="Test Item")
        result = item._to_dict()

        expected = {"id": "test", "label": "Test Item"}
        assert result == expected

    def test_disabled_item_to_dict(self):
        """Test converting disabled TreeItem to dict."""
        item = TreeItem(id="disabled", label="Disabled Item", disabled=True)
        result = item._to_dict()

        expected = {"id": "disabled", "label": "Disabled Item", "disabled": True}
        assert result == expected

    def test_item_with_children_to_dict(self):
        """Test converting TreeItem with children to dict."""
        child1 = TreeItem(id="child1", label="Child 1")
        child2 = TreeItem(id="child2", label="Child 2", disabled=True)
        parent = TreeItem(id="parent", label="Parent", children=[child1, child2])

        result = parent._to_dict()

        expected = {
            "id": "parent",
            "label": "Parent",
            "children": [
                {"id": "child1", "label": "Child 1"},
                {"id": "child2", "label": "Child 2", "disabled": True},
            ],
        }
        assert result == expected

    def test_complex_nested_structure_to_dict(self):
        """Test converting complex nested TreeItem structure to dict."""
        grandchild = TreeItem(id="grandchild", label="Grandchild", disabled=True)
        child = TreeItem(id="child", label="Child", children=[grandchild])
        root = TreeItem(id="root", label="Root", children=[child])

        result = root._to_dict()

        expected = {
            "id": "root",
            "label": "Root",
            "children": [
                {
                    "id": "child",
                    "label": "Child",
                    "children": [
                        {"id": "grandchild", "label": "Grandchild", "disabled": True}
                    ],
                }
            ],
        }
        assert result == expected

    def test_enabled_item_omits_disabled_field(self):
        """Test that enabled items don't include disabled field in dict."""
        item = TreeItem(id="enabled", label="Enabled Item", disabled=False)
        result = item._to_dict()

        # disabled=False should not appear in the dict
        expected = {"id": "enabled", "label": "Enabled Item"}
        assert result == expected
        assert "disabled" not in result

    def test_item_with_caption_to_dict(self):
        """Test TreeItem with caption serializes correctly."""
        item = TreeItem(id="caption_item", label="Test Label", caption="Test caption")
        result = item._to_dict()

        expected = {
            "id": "caption_item",
            "label": "Test Label",
            "caption": "Test caption",
        }
        assert result == expected

    def test_empty_caption_omitted_from_dict(self):
        """Test that empty caption is omitted from dict."""
        item = TreeItem(id="no_caption", label="No Caption", caption="")
        result = item._to_dict()

        expected = {"id": "no_caption", "label": "No Caption"}
        assert result == expected
        assert "caption" not in result


class TestTreeItemCaptionValidation:
    """Test TreeItem caption field validation."""

    def test_valid_caption(self):
        """Test that valid captions are accepted."""
        # Empty caption (default)
        item = TreeItem(id="test", label="Test")
        assert item.caption == ""

        # Non-empty caption
        item_with_caption = TreeItem(id="test", label="Test", caption="A caption")
        assert item_with_caption.caption == "A caption"

    def test_caption_must_be_string(self):
        """Test that caption must be a string."""
        with pytest.raises(ValueError, match="TreeItem caption must be a string"):
            TreeItem(id="test", label="Test", caption=123)

        with pytest.raises(ValueError, match="TreeItem caption must be a string"):
            TreeItem(id="test", label="Test", caption=None)

        with pytest.raises(ValueError, match="TreeItem caption must be a string"):
            TreeItem(id="test", label="Test", caption=["not", "a", "string"])
