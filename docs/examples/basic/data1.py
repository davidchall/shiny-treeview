from shiny_treeview import TreeItem

tree_data = [
    TreeItem(
        "docs",
        "📁 Documents",
        children=[
            TreeItem("report", "📄 Report.pdf"),
            TreeItem("slides", "📄 Slides.pptx"),
        ],
    ),
    TreeItem("readme", "ℹ️ README.md"),
]
