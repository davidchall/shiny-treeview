from shiny import App, Inputs, Outputs, Session, module, render, ui

from shiny_treeview import TreeItem, input_treeview


@module.ui
def file_browser_ui():
    """UI for a file browser module."""
    return ui.div(
        ui.h3("File Browser Module"),
        input_treeview(
            id="tree",
            items=[
                TreeItem(
                    id="documents",
                    label="Documents",
                    children=[
                        TreeItem(id="doc1.pdf", label="Document 1.pdf"),
                        TreeItem(id="doc2.docx", label="Document 2.docx"),
                        TreeItem(id="readme.txt", label="README.txt"),
                    ],
                ),
                TreeItem(
                    id="images",
                    label="Images",
                    children=[
                        TreeItem(id="photo1.jpg", label="Photo 1.jpg"),
                        TreeItem(id="photo2.png", label="Photo 2.png"),
                    ],
                ),
                TreeItem(
                    id="downloads",
                    label="Downloads",
                    children=[
                        TreeItem(id="file1.zip", label="Archive 1.zip"),
                        TreeItem(id="file2.tar", label="Archive 2.tar"),
                    ],
                ),
            ],
            selected="doc1.pdf",
            expanded=["documents", "images"],
        ),
        ui.output_text("selected_file"),
    )


@module.server
def file_browser_server(input: Inputs, output: Outputs, session: Session):
    """Server logic for file browser module."""

    @render.text
    def selected_file():
        selected = input.tree()
        if selected:
            return f"Selected file: {selected}"
        return "No file selected"


@module.ui
def settings_ui():
    """UI for a settings module with treeview."""
    return ui.div(
        ui.h3("Settings Module"),
        input_treeview(
            id="config_tree",
            items=[
                TreeItem(
                    id="general",
                    label="General Settings",
                    children=[
                        TreeItem(id="theme", label="Theme"),
                        TreeItem(id="language", label="Language"),
                        TreeItem(id="timezone", label="Timezone"),
                    ],
                ),
                TreeItem(
                    id="advanced",
                    label="Advanced Settings",
                    children=[
                        TreeItem(id="debug", label="Debug Mode"),
                        TreeItem(id="cache", label="Cache Settings"),
                        TreeItem(id="logging", label="Logging Level"),
                    ],
                ),
                TreeItem(
                    id="security",
                    label="Security",
                    children=[
                        TreeItem(id="auth", label="Authentication"),
                        TreeItem(id="encryption", label="Encryption"),
                    ],
                ),
            ],
            selected="theme",
            expanded=["general"],
            multiple=False,
        ),
        ui.output_text("selected_setting"),
    )


@module.server
def settings_server(input: Inputs, output: Outputs, session: Session):
    """Server logic for settings module."""

    @render.text
    def selected_setting():
        selected = input.config_tree()
        if selected:
            return f"Current setting: {selected}"
        return "No setting selected"


@module.ui
def navigation_ui():
    """UI for a navigation module with multiple selection."""
    return ui.div(
        ui.h3("Navigation Module"),
        input_treeview(
            id="nav_tree",
            items=[
                TreeItem(
                    id="dashboard",
                    label="Dashboard",
                    children=[
                        TreeItem(id="overview", label="Overview"),
                        TreeItem(id="analytics", label="Analytics"),
                    ],
                ),
                TreeItem(
                    id="admin",
                    label="Administration",
                    children=[
                        TreeItem(id="users", label="User Management"),
                        TreeItem(id="roles", label="Role Management"),
                        TreeItem(id="audit", label="Audit Logs"),
                    ],
                ),
            ],
            selected=["overview", "users"],
            expanded=["dashboard", "admin"],
            multiple=True,
        ),
        ui.output_text("selected_pages"),
    )


@module.server
def navigation_server(input: Inputs, output: Outputs, session: Session):
    """Server logic for navigation module."""

    @render.text
    def selected_pages():
        selected = input.nav_tree()
        if selected:
            pages = ", ".join(selected) if isinstance(selected, list) else selected
            return f"Active pages: {pages}"
        return "No pages selected"


# Main app UI combining multiple modules
app_ui = ui.page_fluid(
    ui.h1("Treeview Modules Test Application"),
    ui.p("This app demonstrates treeview components working inside Shiny modules."),
    ui.layout_columns(
        ui.card(
            ui.card_header("File Browser"),
            file_browser_ui("file_module"),
        ),
        ui.card(
            ui.card_header("Application Settings"),
            settings_ui("settings_module"),
        ),
        col_widths=[6, 6],
    ),
    ui.br(),
    ui.card(
        ui.card_header("Navigation"),
        navigation_ui("nav_module"),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    """Main server function that initializes all modules."""

    file_browser_server("file_module")
    settings_server("settings_module")
    navigation_server("nav_module")


app = App(app_ui, server)
