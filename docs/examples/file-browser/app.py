from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

# Sample file system tree data
tree_data = [
    TreeItem(
        id="documents",
        label="📁 Documents",
        children=[
            TreeItem(id="report", label="📄 Report.pdf"),
            TreeItem(id="presentation", label="📄 Presentation.pptx"),
            TreeItem(
                id="archive",
                label="📁 Archive",
                children=[
                    TreeItem(id="old_report", label="📄 Old_Report.pdf"),
                    TreeItem(id="budget", label="📄 Budget_2023.xlsx"),
                ],
            ),
        ],
    ),
    TreeItem(
        id="downloads",
        label="📁 Downloads",
        children=[
            TreeItem(id="software", label="📦 software.zip"),
            TreeItem(id="image", label="🖼️ image.png"),
            TreeItem(id="manual", label="📄 manual.pdf"),
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
                    TreeItem(id="beach", label="🖼️ beach.jpg"),
                    TreeItem(id="sunset", label="🖼️ sunset.jpg"),
                ],
            ),
            TreeItem(id="profile", label="🖼️ profile.jpg"),
        ],
    ),
]

app_ui = ui.page_fluid(
    ui.h2("File Browser Example"),
    ui.p("Select files and folders to see their paths below."),
    ui.row(
        ui.column(
            6,
            ui.h4("Single Selection"),
            input_treeview(
                id="file_tree",
                items=tree_data,
                multiple=False,
                expanded=["documents", "downloads"],
            ),
        ),
        ui.column(
            6,
            ui.h4("Selected File:"),
            ui.output_text("selected_file"),
            ui.br(),
            ui.h4("File Actions:"),
            ui.p(
                "Based on the selected file type, different actions could be available."
            ),
            ui.output_ui("file_actions"),
        ),
    ),
)


def server(input, output, session):
    @render.text
    def selected_file():
        selected = input.file_tree()
        if selected:
            return f"📂 Path: /{selected.replace('_', '/')}"
        return "No file selected"

    @render.ui
    def file_actions():
        selected = input.file_tree()
        if not selected:
            return ui.p("Select a file to see available actions.")

        # Simple file type detection based on the selected item
        if selected in ["documents", "downloads", "pictures", "archive", "vacation"]:
            return ui.div(
                ui.p("📁 Folder Actions:"),
                ui.actionButton(
                    "open_folder", "Open Folder", class_="btn-primary btn-sm me-2"
                ),
                ui.actionButton(
                    "share_folder", "Share", class_="btn-outline-secondary btn-sm"
                ),
            )
        elif selected.endswith(("report", "presentation", "manual")):
            return ui.div(
                ui.p("📄 Document Actions:"),
                ui.actionButton("open_doc", "Open", class_="btn-primary btn-sm me-2"),
                ui.actionButton(
                    "edit_doc", "Edit", class_="btn-outline-primary btn-sm me-2"
                ),
                ui.actionButton(
                    "share_doc", "Share", class_="btn-outline-secondary btn-sm"
                ),
            )
        elif selected in ["software"]:
            return ui.div(
                ui.p("📦 Archive Actions:"),
                ui.actionButton("extract", "Extract", class_="btn-warning btn-sm me-2"),
                ui.actionButton(
                    "scan", "Virus Scan", class_="btn-outline-danger btn-sm"
                ),
            )
        else:  # Images
            return ui.div(
                ui.p("🖼️ Image Actions:"),
                ui.actionButton("view_img", "View", class_="btn-primary btn-sm me-2"),
                ui.actionButton(
                    "edit_img", "Edit", class_="btn-outline-primary btn-sm me-2"
                ),
                ui.actionButton(
                    "download_img", "Download", class_="btn-outline-secondary btn-sm"
                ),
            )


app = App(app_ui, server)
