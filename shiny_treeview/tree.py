"""Data structures for shiny-treeview."""

import string
from dataclasses import dataclass, field


@dataclass
class TreeItem:
    """
    Represents a single item in a tree view.

    Attributes
    ----------
    id : str
        Unique identifier for the tree item. Must be unique across all items in the tree.
    label : str
        Display text for the tree item. Can include emoji and other characters.
    children : list[TreeItem]
        List of child TreeItem objects. Defaults to empty list for leaf nodes.
    disabled : bool
        Whether the item is disabled (non-selectable). Defaults to False.

    Examples
    --------
    Simple leaf item:

    >>> from shiny_treeview import TreeItem
    >>> leaf = TreeItem(id="doc1", label="📄 Document.pdf")

    Parent item with children:

    >>> folder = TreeItem(
    ...     id="documents",
    ...     label="📁 Documents",
    ...     children=[
    ...         TreeItem(id="doc1", label="📄 Report.pdf"),
    ...         TreeItem(id="doc2", label="📄 Presentation.pptx", disabled=True)
    ...     ]
    ... )
    """

    id: str
    label: str
    children: list["TreeItem"] = field(default_factory=list)
    disabled: bool = False

    def __post_init__(self):
        # Validate id
        if not isinstance(self.id, str):
            raise ValueError("TreeItem id must be a string")

        if self.id == "" or any(char in string.whitespace for char in self.id):
            raise ValueError("TreeItem id cannot be empty or contain whitespace")

        # Validate label
        if not isinstance(self.label, str):
            raise ValueError("TreeItem label must be a string")

        if not self.label.strip():
            raise ValueError("TreeItem label cannot be empty or whitespace only")

        # Validate disabled
        if not isinstance(self.disabled, bool):
            raise ValueError("TreeItem disabled must be a boolean")

        # Validate children
        if not isinstance(self.children, list):
            raise ValueError("TreeItem children must be a list")

        for i, child in enumerate(self.children):
            if not isinstance(child, TreeItem):
                raise ValueError(f"TreeItem children[{i}] must be a TreeItem instance")

    def to_dict(self) -> dict:
        """
        Convert TreeItem to dictionary format compatible with MUI RichTreeView.

        Returns
        -------
        dict
            Dictionary representation of the tree item.
        """
        result = {"id": self.id, "label": self.label}

        if self.disabled:
            result["disabled"] = True

        if self.children:
            result["children"] = [child.to_dict() for child in self.children]

        return result
