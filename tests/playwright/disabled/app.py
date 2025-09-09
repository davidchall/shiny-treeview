from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

tree_data = [
    TreeItem(
        id="folder1",
        label="Folder 1",
        children=[
            TreeItem(id="file1", label="File 1"),
            TreeItem(id="file2", label="File 2", disabled=True),
        ],
    ),
    TreeItem(id="standalone", label="Standalone File", disabled=False),
]


app_ui = ui.page_fluid(
    ui.h1("Treeview Test App"),
    input_treeview(id="my_treeview", items=tree_data, selected="file1"),
)

app = App(app_ui, None)
