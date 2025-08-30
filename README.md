# Shiny TreeView

A Shiny for Python extension that provides a tree view component using Material-UI's RichTreeView component.

![Tree View Demo](https://via.placeholder.com/600x400/e0e0e0/333333?text=Tree+View+Demo)

## Features

- 🌳 **Hierarchical Data Display**: Display nested data structures in an intuitive tree format
- 🎯 **Single and Multiple Selection**: Support for both single and multiple item selection modes
- 🎨 **Material Design**: Built with Material-UI components for a modern, professional look
- ⚡ **Reactive**: Real-time updates when selections change
- 🐍 **Python-First**: Designed specifically for Shiny for Python applications
- 📱 **Responsive**: Works well on desktop and mobile devices

## Installation

```bash
pip install shiny-treeview
```

## Quick Start

```python
from shiny import App, ui, render
from shiny_treeview import input_treeview

# Define your tree data
tree_data = [
    {
        "id": "documents",
        "label": "📁 Documents",
        "children": [
            {"id": "doc1", "label": "📄 Report.pdf"},
            {"id": "doc2", "label": "📄 Presentation.pptx"},
        ]
    },
    {
        "id": "downloads",
        "label": "📁 Downloads",
        "children": [
            {"id": "download1", "label": "📦 software.zip"},
            {"id": "download2", "label": "🖼️ image.png"},
        ]
    }
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
        return f"Selected: {', '.join(selected) if selected else 'None'}"

app = App(app_ui, server)
```

## API Reference

### `input_treeview(id, items, multiple=False, selected=None)`

Create a tree view input component.

#### Parameters

- **`id`** (str): The input ID for the component
- **`items`** (List[Dict]): Tree data structure. Each item should have:
  - `id` (str): Unique identifier for the item
  - `label` (str): Display text for the item
  - `children` (List[Dict], optional): Child items
- **`multiple`** (bool, optional): Enable multiple selection. Default: `False`
- **`selected`** (Union[str, List[str]], optional): Initially selected item ID(s)

#### Tree Data Structure

```python
[
    {
        "id": "parent1",
        "label": "Parent Item 1",
        "children": [
            {
                "id": "child1",
                "label": "Child Item 1",
                "children": [
                    {"id": "grandchild1", "label": "Grandchild Item 1"}
                ]
            },
            {"id": "child2", "label": "Child Item 2"}
        ]
    },
    {
        "id": "parent2",
        "label": "Parent Item 2"
    }
]
```

## Examples

### Single Selection Tree

```python
input_treeview(
    id="single_tree",
    items=tree_data,
    multiple=False,
    selected="specific_id"
)
```

### Multiple Selection Tree

```python
input_treeview(
    id="multi_tree",
    items=tree_data,
    multiple=True,
    selected=["id1", "id2", "id3"]
)
```

### File System Browser

```python
file_tree = [
    {
        "id": "home",
        "label": "🏠 Home",
        "children": [
            {
                "id": "documents",
                "label": "📁 Documents",
                "children": [
                    {"id": "resume.pdf", "label": "📄 Resume.pdf"},
                    {"id": "cover_letter.doc", "label": "📄 Cover Letter.doc"}
                ]
            },
            {
                "id": "pictures",
                "label": "📁 Pictures",
                "children": [
                    {"id": "vacation.jpg", "label": "🖼️ Vacation.jpg"},
                    {"id": "family.png", "label": "🖼️ Family.png"}
                ]
            }
        ]
    }
]

input_treeview(
    id="file_browser",
    items=file_tree,
    multiple=True
)
```

## Requirements

- Python 3.10+
- shiny >= 0.6.0
- htmltools >= 0.6.0

This package ships with a prebuilt JavaScript bundle, so end users do not need Node.js or npm to install or use it.

## Technical Details

This package uses:

- **React & ReactDOM**: For rendering the MUI component
- **Material-UI RichTreeView**: The core tree component
- **Shiny React Bindings**: For seamless Shiny integration

The component works by:
1. Creating a React component that renders the MUI RichTreeView
2. Using Shiny's React input binding system to communicate with Python
3. Serializing tree data as JSON between Python and JavaScript
4. Providing a clean Python API that feels native to Shiny
