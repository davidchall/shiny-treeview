from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

tree_data = [
    TreeItem(
        id="folder1",
        label="Folder 1",
        children=[
            TreeItem(id="file1", label="File 1"),
            TreeItem(id="file2", label="File 2"),
            TreeItem(
                id="subfolder1",
                label="Subfolder 1",
                children=[
                    TreeItem(id="subfile1", label="Subfile 1"),
                    TreeItem(id="subfile2", label="Subfile 2"),
                ],
            ),
        ],
    ),
    TreeItem(
        id="folder2",
        label="Folder 2",
        children=[
            TreeItem(id="file3", label="File 3"),
            TreeItem(id="file4", label="File 4"),
        ],
    ),
    TreeItem(id="standalone", label="Standalone File"),
]


app_ui = ui.page_fluid(
    ui.h1("Treeview Test App"),
    ui.card(
        ui.card_header("Single selection: default"),
        input_treeview(id="single_default", items=tree_data, checkbox=True),
        ui.output_code("single_default_txt"),
    ),
    ui.card(
        ui.card_header("Multiple selection: default"),
        input_treeview(
            id="multi_default", items=tree_data, multiple=True, checkbox=True
        ),
        ui.output_code("multi_default_txt"),
    ),
    ui.card(
        ui.card_header("Single selection: with initial value"),
        input_treeview(
            id="single_with_selected",
            items=tree_data,
            selected="file1",
            multiple=False,
            checkbox=True,
        ),
        ui.output_code("single_with_selected_txt"),
    ),
    ui.card(
        ui.card_header("Multiple selection: with initial values"),
        input_treeview(
            id="multi_with_selected",
            items=tree_data,
            selected=["file1", "file3"],
            multiple=True,
            checkbox=True,
        ),
        ui.output_code("multi_with_selected_txt"),
    ),
)


def server(input, output, session):
    """Server logic to display the current values of each treeview input."""

    @render.code
    def single_default_txt():
        return str(input.single_default())

    @render.code
    def multi_default_txt():
        return str(input.multi_default())

    @render.code
    def single_with_selected_txt():
        return str(input.single_with_selected())

    @render.code
    def multi_with_selected_txt():
        return str(input.multi_with_selected())


app = App(app_ui, server)
