from shiny_treeview import TreeItem

tree_data = [
    TreeItem(
        id="docs",
        label="📁 Documents",
        children=[
            TreeItem(id="report", label="📄 Report.pdf"),
            TreeItem(id="slides", label="📄 Slides.pptx"),
        ],
    ),
    TreeItem(id="readme", label="📄 README.md"),
]
