import json
from pathlib import PurePath
from typing import Optional

from htmltools import HTMLDependency, Tag, TagList, tags
from shiny.module import resolve_id

from .__version__ import __version__
from .tree import TreeItem
from .utils import duplicate_ids, get_tree_path

treeview_deps = HTMLDependency(
    "shiny_treeview",
    __version__,
    source={
        "package": "shiny_treeview",
        "subdir": str(PurePath(__file__).parent / "distjs"),
    },
    script={"src": "index.js", "type": "module"},
)


def input_treeview(
    id: str,
    items: list[TreeItem],
    *,
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
    multiple : bool
        Whether to allow multiple selection.
    selected : Optional[str | list[str]]
        Initially selected item ID(s). If None (default), no items are selected.
    expanded : Optional[str | list[str]]
        Initially expanded item ID(s). If None (default), automatically expands all
        parents necessary to make visible the items in the `selected` argument.

    Returns
    -------
    Tag
        An element used when creating your Shiny app UI.

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
        "items": [x._to_dict() for x in items],
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
