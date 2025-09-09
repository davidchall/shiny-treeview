from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

tree_data = [
    TreeItem(
        id="folder1",
        label="Folder 1",
        caption="This is a very long caption that should demonstrate how the treeview handles extensive descriptive text that might wrap to multiple lines or overflow the container width",
        children=[
            TreeItem(id="file1", label="File 1", caption="Short caption"),
            TreeItem(id="file2", label="File 2"),
        ],
    ),
    TreeItem(
        id="standalone",
        label="Standalone File",
    ),
]


app_ui = ui.page_fluid(
    ui.h1("Treeview Test App"),
    input_treeview(id="my_treeview", items=tree_data, selected="file1", width="400px"),
)

app = App(app_ui, None)
