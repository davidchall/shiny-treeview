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

```python
from shiny import App, ui, render
from shiny_treeview import input_treeview, TreeItem

# Define your tree data using TreeItem objects
tree_data = [
    TreeItem(
        id="documents",
        label="📁 Documents",
        children=[
            TreeItem(id="doc1", label="📄 Report.pdf"),
            TreeItem(id="doc2", label="📄 Presentation.pptx"),
        ]
    ),
    TreeItem(
        id="downloads",
        label="📁 Downloads",
        children=[
            TreeItem(id="download1", label="📦 software.zip"),
            TreeItem(id="download2", label="🖼️ image.png"),
        ]
    )
]

app_ui = ui.page_fluid(
    ui.h1("My Tree View App"),
    input_treeview(
        id="my_tree",
        items=tree_data,
        multiple=False,
        selected="doc1"
    ),
    ui.output_text("selected_items")
)

def server(input, output, session):
    @render.text
    def selected_items():
        selected = input.my_tree()
        return f"Selected: {selected}"

app = App(app_ui, server)
```
