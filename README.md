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

Create hierarchical data with `TreeItem`, add the treeview to your Shiny app UI, and use the selected IDs as needed in the rest of the app.

```python
from shiny import App, ui, render
from shiny_treeview import input_treeview, TreeItem

# Define your tree data using TreeItem objects
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

app_ui = ui.page_fluid(
    ui.h1("My Tree View App"),
    input_treeview("my_tree", tree_data),
    ui.output_text("selected_item")
)

def server(input, output, session):
    @render.text
    def selected_item():
        return f"Selected: {input.my_tree()}"

app = App(app_ui, server)
```
