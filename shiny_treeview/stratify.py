"""Helper functions to convert flat data to hierarchical tree data."""

from dataclasses import replace
from typing import Optional

from .tree import TreeItem


def stratify_by_parent(
    items: list[TreeItem], parent_ids: list[Optional[str]]
) -> list[TreeItem]:
    """
    Convert flat data to hierarchical tree data via parent-child relationships.

    Takes a list of TreeItem objects where parent-child relationships are expressed
    through a separate list of parent_ids, and returns tree data where the
    parent-child relationships are expressed through the TreeItem children attribute.

    Parameters
    ----------
    items : list[TreeItem]
        List of TreeItem objects with empty children lists
    parent_ids : list[Optional[str]]
        List of parent IDs corresponding to each TreeItem. None indicates a root item.
        Must be the same length as items list.

    Returns
    -------
    list[TreeItem]
        List of root TreeItem objects with populated children attributes.
        All original attributes are preserved.

    Raises
    ------
    ValueError
        If items and parent_ids lists have different lengths.
        If a parent_id references a non-existent item.
        If circular references are detected.

    Examples
    --------
    ```python
    from shiny_treeview import TreeItem, stratify_by_parent

    # Flat data with parent-child relationships
    items = [
        TreeItem(id="root", label="Root"),
        TreeItem(id="child1", label="Child 1"),
        TreeItem(id="child2", label="Child 2"),
        TreeItem(id="grandchild", label="Grandchild")
    ]
    parent_ids = [None, "root", "root", "child1"]

    # Convert to hierarchical structure
    tree = stratify_by_parent(items, parent_ids)
    # Result: root item with child1 and child2 as children,
    # and grandchild as a child of child1
    ```
    """
    if len(items) != len(parent_ids):
        raise ValueError("items and parent_ids lists must have the same length")

    # Create a mapping from item ID to TreeItem for quick lookup
    item_map = {item.id: item for item in items}

    # Check for duplicate IDs
    if len(item_map) != len(items):
        raise ValueError("All TreeItem IDs must be unique")

    # Validate that all parent_ids reference existing items (or are None)
    for i, parent_id in enumerate(parent_ids):
        if parent_id is not None and parent_id not in item_map:
            raise ValueError(
                f"Parent ID '{parent_id}' at index {i} does not reference an existing item"
            )

    # Create a mapping from parent ID to list of children
    children_map = {}
    root_items = []

    for item, parent_id in zip(items, parent_ids):
        # Create a new TreeItem to avoid modifying the original
        new_item = replace(item, children=[])

        if parent_id is None:
            # This is a root item
            root_items.append(new_item)
        else:
            # Add to parent's children list
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(new_item)

        # Update the item_map for easy access to the new item
        item_map[item.id] = new_item

    # Populate children for all items
    for parent_id, children in children_map.items():
        if parent_id in item_map:
            item_map[parent_id].children = children

    def _has_circular_reference() -> bool:
        """Check if there are any circular references in the parent-child relationships."""
        # Create a mapping from item_id to parent_id for efficient lookup
        parent_map = {item.id: parent_id for item, parent_id in zip(items, parent_ids)}

        # For each item, trace its ancestry to see if we loop back
        for item_id in parent_map:
            visited = set()
            current_id = parent_map.get(item_id)

            # Follow the parent chain
            while current_id is not None:
                if current_id in visited:
                    return True
                visited.add(current_id)
                current_id = parent_map.get(current_id)

        return False

    if _has_circular_reference():
        raise ValueError("Circular reference detected in parent-child relationships")

    return root_items
