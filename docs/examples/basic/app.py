from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

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

app_ui = ui.page_fluid(
    ui.h1("My Tree View App"),
    input_treeview("my_tree", tree_data),
    ui.output_text("selected_item"),
)


def server(input, output, session):
    @render.text
    def selected_item():
        return f"Selected: {input.my_tree()}"


app = App(app_ui, server)
