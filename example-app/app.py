# pyright: basic

from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

# Sample tree data using TreeItem objects
tree_data = [
    TreeItem(
        id="documents",
        label="📁 Documents",
        children=[
            TreeItem(id="doc1", label="📄 Report.pdf"),
            TreeItem(id="doc2", label="📄 Presentation.pptx"),
            TreeItem(
                id="subfolder1",
                label="📁 Archive",
                children=[
                    TreeItem(id="archive1", label="📄 Old_Report.pdf"),
                    TreeItem(id="archive2", label="📄 Budget_2023.xlsx"),
                ],
            ),
        ],
    ),
    TreeItem(
        id="downloads",
        label="📁 Downloads",
        children=[
            TreeItem(id="download1", label="📦 software.zip"),
            TreeItem(id="download2", label="🖼️ image.png"),
            TreeItem(
                id="download3", label="📄 manual.pdf", disabled=True
            ),  # Disabled item
        ],
    ),
    TreeItem(
        id="pictures",
        label="📁 Pictures",
        children=[
            TreeItem(
                id="vacation",
                label="📁 Vacation 2024",
                children=[
                    TreeItem(id="pic1", label="🖼️ beach.jpg"),
                    TreeItem(id="pic2", label="🖼️ sunset.jpg"),
                ],
            ),
            TreeItem(id="pic3", label="🖼️ profile.jpg"),
        ],
    ),
]

app_ui = ui.page_fluid(
    ui.h1("Shiny Tree View Demo"),
    ui.p(
        "This demo shows the MUI RichTreeView component integrated with Shiny for Python."
    ),
    ui.row(
        ui.column(
            6,
            ui.h3("Single Selection Tree"),
            input_treeview(
                id="single_tree",
                items=tree_data,
                multiple=False,
                selected="doc1",  # Pre-select an item
                expanded=["documents", "downloads"],  # Expand these folders initially
            ),
            ui.br(),
            ui.h4("Selected Item:"),
            ui.output_text("single_selection"),
        ),
        ui.column(
            6,
            ui.h3("Multiple Selection Tree"),
            input_treeview(
                id="multi_tree",
                items=tree_data,
                multiple=True,
                selected=["doc1", "download2"],  # Pre-select multiple items
                expanded="pictures",  # Expand just the pictures folder (single string)
            ),
            ui.br(),
            ui.h4("Selected Items:"),
            ui.output_text("multi_selection"),
        ),
    ),
    ui.hr(),
    ui.row(
        ui.column(
            6,
            ui.h3("Empty Single Selection Tree (starts with None)"),
            input_treeview(
                id="empty_single_tree",
                items=tree_data,
                multiple=False,
                expanded=["documents"],
            ),
            ui.br(),
            ui.h4("Selected Item:"),
            ui.output_text("empty_single_selection"),
        ),
        ui.column(
            6,
            ui.h3("Empty Multiple Selection Tree (starts with None)"),
            input_treeview(
                id="empty_multi_tree",
                items=tree_data,
                multiple=True,
                expanded=["documents"],
            ),
            ui.br(),
            ui.h4("Selected Items:"),
            ui.output_text("empty_multi_selection"),
        ),
    ),
    ui.hr(),
    ui.h3("All Input Values (for debugging):"),
    ui.output_text("debug_info"),
)


def server(input, output, session):
    @render.text
    def single_selection():
        selected = input.single_tree()
        # Single selection should return a string or None
        if selected:
            return f"Selected: {selected}"
        return "None selected"

    @render.text
    def multi_selection():
        selected = input.multi_tree()
        # Multiple selection should return a tuple/list or None
        if selected and isinstance(selected, (list, tuple)) and len(selected) > 0:
            return f"Selected: {', '.join(selected)}"
        return "None selected"

    @render.text
    def empty_single_selection():
        selected = input.empty_single_tree()
        # Single selection should return a string or None
        if selected:
            return f"Selected: {selected}"
        return "None selected"

    @render.text
    def empty_multi_selection():
        selected = input.empty_multi_tree()
        # Multiple selection should return a tuple/list or None
        if selected and isinstance(selected, (list, tuple)) and len(selected) > 0:
            return f"Selected: {', '.join(selected)}"
        return "None selected"

    @render.text
    def debug_info():
        single_val = input.single_tree()
        multi_val = input.multi_tree()
        empty_single_val = input.empty_single_tree()
        empty_multi_val = input.empty_multi_tree()
        return f"""
        Single tree value: {single_val} (type: {type(single_val)})
        Multi tree value: {multi_val} (type: {type(multi_val)})
        Empty single tree value: {empty_single_val} (type: {type(empty_single_val)})
        Empty multi tree value: {empty_multi_val} (type: {type(empty_multi_val)})
        """


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
