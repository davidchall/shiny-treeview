# Shiny TreeView

A TreeView UI component for [Shiny for Python](https://shiny.posit.co/py/), backed by [Material UI](https://mui.com/x/react-tree-view/).

## Installation

```sh
pip install shiny-treeview
```

To install the latest development version:

```sh
pip install git+https://github.com/davidchall/shiny-treeview.git#egg=shiny_treeview
```

## Quick Start

Try this quick start live and explore more examples [here](https://davidchall.github.io/shiny-treeview/examples).

```python
from shiny.express import input, render
from shiny_treeview import input_treeview, TreeItem

tree_data = [
    TreeItem(
        "docs",
        "📁 Documents",
        children=[
            TreeItem("report", "📄 Report.pdf"),
            TreeItem("slides", "📄 Slides.pptx"),
        ]
    ),
    TreeItem("readme", "ℹ️ README.md")
]

input_treeview("my_tree", tree_data)

@render.text
def value():
    return f"Selected: {input.my_tree()}"
```
