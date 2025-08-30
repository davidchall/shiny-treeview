"""Utility functions for working with tree data structures."""

from dataclasses import replace
from typing import Optional

from .data import TreeItem


def get_tree_path(items: list[TreeItem], id: str) -> Optional[tuple[str, ...]]:
    """
    Get the path to a tree item by traversing ancestors.

    Searches the tree structure for the TreeItem with the matching id attribute
    and returns a tuple containing the id attributes for all its ancestors,
    ending with the matching id.

    Parameters
    ----------
    items
        List of TreeItem objects to search through
    id
        The id of the target TreeItem to find

    Returns
    -------
    Optional[tuple[str, ...]]
        Tuple of ancestor ids ending with the target id, or None if not found.

        For example, if searching for "file1" in a tree like:
        folder1 -> subfolder1 -> file1.
        Returns: ("folder1", "subfolder1", "file1")
    """

    def _search_recursive(
        items: list[TreeItem], target_id: str, path: list[str]
    ) -> Optional[tuple[str, ...]]:
        """Recursively search for the target item and build path."""
        for item in items:
            current_path = path + [item.id]

            # Found the target item
            if item.id == target_id:
                return tuple(current_path)

            # Search in children if they exist
            if item.children:
                result = _search_recursive(item.children, target_id, current_path)
                if result is not None:
                    return result

        return None

    return _search_recursive(items, id, [])


def duplicate_ids(items: list[TreeItem]) -> list[str]:
    """
    Find duplicate TreeItem IDs in a tree structure.

    Parameters
    ----------
    items
        List of TreeItem objects to check for duplicate IDs.

    Returns
    -------
    list[str]
        List of duplicate IDs found in the tree. If no duplicates, returns an empty list.
    """

    def _collect_all_ids(items: list[TreeItem]) -> list[str]:
        """Recursively collect all IDs from a tree structure."""
        all_ids = []
        for item in items:
            all_ids.append(item.id)
            if item.children:
                all_ids.extend(_collect_all_ids(item.children))
        return all_ids

    all_ids = _collect_all_ids(items)
    seen_ids = set()
    duplicate_ids = set()

    for item_id in all_ids:
        if item_id in seen_ids:
            duplicate_ids.add(item_id)
        else:
            seen_ids.add(item_id)

    return sorted(duplicate_ids)


def stratify(items: list[TreeItem], parent_ids: list[Optional[str]]) -> list[TreeItem]:
    """
    Convert flat TreeItem data with parent-child relationships to hierarchical structure.

    Takes a list of TreeItem objects where parent-child relationships are expressed
    through a separate list of parent_ids, and returns tree data where the
    parent-child relationships are expressed through the TreeItem children attribute.

    This function preserves all fields and attributes from the original TreeItem objects,
    including any additional fields that may be added in future versions or custom extensions.

    Parameters
    ----------
    items
        List of TreeItem objects with empty children lists
    parent_ids
        List of parent IDs corresponding to each TreeItem. None indicates a root item.
        Must be the same length as items list.

    Returns
    -------
    list[TreeItem]
        List of root TreeItem objects with populated children attributes.
        All original fields and attributes are preserved.

    Raises
    ------
    ValueError
        If items and parent_ids lists have different lengths
        If a parent_id references a non-existent item
        If circular references are detected

    Example
    -------
    ```python
    from shiny_treeview import TreeItem, stratify

    # Flat data with parent-child relationships
    items = [
        TreeItem(id="root", label="Root"),
        TreeItem(id="child1", label="Child 1"),
        TreeItem(id="child2", label="Child 2"),
        TreeItem(id="grandchild", label="Grandchild")
    ]
    parent_ids = [None, "root", "root", "child1"]

    # Convert to hierarchical structure
    tree = stratify(items, parent_ids)
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
