from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

# Software components tree with checkbox selection
tree_data = [
    TreeItem(
        id="frontend",
        label="🌐 Frontend Components",
        children=[
            TreeItem(id="react", label="⚛️ React Framework"),
            TreeItem(id="bootstrap", label="🎨 Bootstrap CSS"),
            TreeItem(id="icons", label="🎯 Icon Library"),
            TreeItem(
                id="charts",
                label="📊 Chart Libraries",
                children=[
                    TreeItem(id="plotly", label="📈 Plotly"),
                    TreeItem(id="d3", label="📉 D3.js"),
                ],
            ),
        ],
    ),
    TreeItem(
        id="backend",
        label="⚙️ Backend Services",
        children=[
            TreeItem(id="python", label="🐍 Python Runtime"),
            TreeItem(id="fastapi", label="🚀 FastAPI Framework"),
            TreeItem(id="database", label="🗃️ PostgreSQL Database"),
            TreeItem(id="redis", label="⚡ Redis Cache"),
        ],
    ),
    TreeItem(
        id="devtools",
        label="🛠️ Development Tools",
        children=[
            TreeItem(id="docker", label="🐳 Docker"),
            TreeItem(id="pytest", label="🧪 Pytest"),
            TreeItem(id="black", label="⚫ Black Formatter"),
        ],
    ),
]

app_ui = ui.page_fluid(
    ui.h2("Software Components Selection"),
    ui.p(
        "Use checkboxes to select the components you want to include in your project."
    ),
    ui.row(
        ui.column(
            6,
            ui.h4("Available Components"),
            input_treeview(
                id="components_tree",
                items=tree_data,
                multiple=True,
                checkbox=True,  # Enable checkbox selection
                expanded=["frontend", "backend", "devtools"],
                selected=[
                    "react",
                    "python",
                    "docker",
                ],  # Pre-select essential components
            ),
        ),
        ui.column(
            6,
            ui.h4("Selected Components:"),
            ui.output_text("selected_components"),
            ui.br(),
            ui.h4("Installation Commands:"),
            ui.output_ui("install_commands"),
            ui.br(),
            ui.h4("Project Summary:"),
            ui.output_text("project_summary"),
        ),
    ),
)


def server(input, output, session):
    @render.text
    def selected_components():
        selected = input.components_tree()
        if selected and len(selected) > 0:
            component_names = []
            for comp_id in selected:
                # Find component name from tree data
                for category in tree_data:
                    if category.id == comp_id:
                        component_names.append(category.label)
                    elif hasattr(category, "children") and category.children:
                        for comp in category.children:
                            if comp.id == comp_id:
                                component_names.append(comp.label)
                            elif hasattr(comp, "children") and comp.children:
                                for subcomp in comp.children:
                                    if subcomp.id == comp_id:
                                        component_names.append(subcomp.label)

            return f"Selected {len(selected)} components:\n" + "\n".join(
                f"• {name}" for name in component_names
            )
        return "No components selected"

    @render.ui
    def install_commands():
        selected = input.components_tree()
        if not selected or len(selected) == 0:
            return ui.p("Select components to see installation commands.")

        # Map component IDs to installation commands
        install_map = {
            "react": "npm install react react-dom",
            "bootstrap": "npm install bootstrap",
            "icons": "npm install react-icons",
            "plotly": "npm install plotly.js",
            "d3": "npm install d3",
            "python": "# Python runtime (already available)",
            "fastapi": "pip install fastapi uvicorn",
            "database": "pip install psycopg2-binary",
            "redis": "pip install redis",
            "docker": "# Install Docker Desktop",
            "pytest": "pip install pytest",
            "black": "pip install black",
        }

        commands = []
        for comp_id in selected:
            if comp_id in install_map:
                commands.append(install_map[comp_id])

        if commands:
            return ui.div(
                ui.tags.pre(
                    ui.tags.code("\n".join(commands)), class_="bg-light p-3 rounded"
                )
            )
        return ui.p("No installation commands available for selected items.")

    @render.text
    def project_summary():
        selected = input.components_tree()
        if not selected or len(selected) == 0:
            return "No components selected for project."

        # Categorize selected components
        frontend_count = len(
            [
                s
                for s in selected
                if s in ["react", "bootstrap", "icons", "plotly", "d3", "charts"]
            ]
        )
        backend_count = len(
            [s for s in selected if s in ["python", "fastapi", "database", "redis"]]
        )
        devtools_count = len(
            [s for s in selected if s in ["docker", "pytest", "black"]]
        )

        project_type = "Unknown"
        if frontend_count > 0 and backend_count > 0:
            project_type = "Full-Stack Application"
        elif frontend_count > 0:
            project_type = "Frontend Application"
        elif backend_count > 0:
            project_type = "Backend Service"

        return f"""Project Type: {project_type}
Frontend Components: {frontend_count}
Backend Components: {backend_count}
Development Tools: {devtools_count}

Total Selected: {len(selected)} components"""


app = App(app_ui, server)
