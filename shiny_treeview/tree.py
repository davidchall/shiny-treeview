"""Data structures for shiny-treeview."""

import string
from dataclasses import dataclass, field


@dataclass
class TreeItem:
    """
    Represents a single item in a tree data structure. Passed to `input_treeview()`.

    Parameters
    ----------
    id : str
        Unique identifier for the tree item. Must be unique across all items in the tree.
    label : str
        Display text for the tree item. Can include emoji and other characters.
    caption : str, optional
        Secondary text displayed below the label in smaller font.
    children : list[TreeItem], optional
        List of child nodes.
    disabled : bool, default=False
        Whether the item is disabled (non-selectable).

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
    caption: str = ""
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

        # Validate caption
        if not isinstance(self.caption, str):
            raise ValueError("TreeItem caption must be a string")

        # Validate disabled
        if not isinstance(self.disabled, bool):
            raise ValueError("TreeItem disabled must be a boolean")

        # Validate children
        if not isinstance(self.children, list):
            raise ValueError("TreeItem children must be a list")

        for i, child in enumerate(self.children):
            if not isinstance(child, TreeItem):
                raise ValueError(f"TreeItem children[{i}] must be a TreeItem instance")

    def _to_dict(self) -> dict:
        """
        Serialize TreeItem for sending to server.

        Performance is optimized by dropping default values.

        Returns
        -------
        dict
            Dictionary representation of the tree item.
        """
        result = {"id": self.id, "label": self.label}

        if self.caption:
            result["caption"] = self.caption

        if self.disabled:
            result["disabled"] = True

        if self.children:
            result["children"] = [child._to_dict() for child in self.children]

        return result
