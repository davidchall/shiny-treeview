"""Utility functions for working with tree data structures."""

from typing import Optional

from .tree import TreeItem


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
