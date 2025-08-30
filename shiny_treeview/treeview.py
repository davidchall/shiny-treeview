import json
from pathlib import PurePath
from typing import Optional

from htmltools import HTMLDependency, Tag, TagList, tags
from shiny.module import resolve_id

from .data import TreeItem
from .utils import duplicate_ids, get_tree_path

treeview_deps = HTMLDependency(
    "shiny_treeview",
    "0.1.0",
    source={
        "package": "shiny_treeview",
        "subdir": str(PurePath(__file__).parent / "distjs"),
    },
    script={"src": "index.js", "type": "module"},
)


def input_treeview(
    id: str,
    items: list[TreeItem],
    multiple: bool = False,
    selected: Optional[str | list[str]] = None,
    expanded: Optional[str | list[str]] = None,
) -> Tag:
    """
    Create a treeview input component.

    Parameters
    ----------
    id : str
        The input id.
    items : list[TreeItem]
        A list of TreeItem objects representing the tree data.
    multiple : bool, optional
        Whether to allow multiple selection. Defaults to False.
    selected : Optional[str | list[str]]
        Initially selected item ID(s). If multiple=True, should be a list.
        If multiple=False, should be a string. Defaults to None.
    expanded : Optional[str | list[str]]
        Initially expanded item ID(s). Can be a single string or list of strings.
        Expanded items will show their children when the tree loads.
        If None (default), automatically expands all parents necessary to make the
        selected items visible.

    Returns
    -------
    Tag
        A Tag object representing the tree view component.

    Notes
    -----
    If `multiple=False`, the server value is a string with the ID of the selected item.
    If `multiple=True`, the server value is a tuple containing the IDs of the
    selected items. When nothing is selected, this value will be `None`.
    """
    duplicates = duplicate_ids(items)
    if duplicates:
        raise ValueError(
            f"Duplicate TreeItem IDs found: {duplicates}. All TreeItem IDs must be unique across the entire tree."
        )

    # Normalize selected items to always be a list
    if selected is None:
        selected_items = []
    elif isinstance(selected, str):
        selected_items = [selected] if selected else []
    else:
        selected_items = selected

    # Normalize expanded items to always be a list
    if expanded is None:
        # Auto-expand: find all ancestors of selected items to make them visible
        expanded_items = []
        for selected_id in selected_items:
            tree_path = get_tree_path(items, selected_id)
            if tree_path is not None:
                expanded_items.extend(tree_path[:-1])

        expanded_items = list(dict.fromkeys(expanded_items))
    elif isinstance(expanded, str):
        expanded_items = [expanded] if expanded else []
    else:
        expanded_items = expanded

    payload = {
        "items": [x.to_dict() for x in items],
        "multiple": multiple,
        "selected": selected_items,
        "expanded": expanded_items,
    }

    return tags.div(
        TagList(
            tags.script(
                json.dumps(payload),
                type="application/json",
                data_for=resolve_id(id),
            ),
            treeview_deps,
        ),
        id=resolve_id(id),
        class_="shiny-treeview",
    )
