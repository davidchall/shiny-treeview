from shiny import App, render, ui

from shiny_treeview import TreeItem, input_treeview

# Task/project management tree data
tree_data = [
    TreeItem(
        id="project_a",
        label="🚀 Project Alpha",
        children=[
            TreeItem(id="task_a1", label="✅ Setup development environment"),
            TreeItem(id="task_a2", label="⏳ Design user interface"),
            TreeItem(id="task_a3", label="❌ Implement backend API"),
            TreeItem(id="task_a4", label="⏳ Write documentation"),
        ],
    ),
    TreeItem(
        id="project_b",
        label="🎯 Project Beta",
        children=[
            TreeItem(id="task_b1", label="✅ Requirements gathering"),
            TreeItem(id="task_b2", label="⏳ Database design"),
            TreeItem(id="task_b3", label="❌ Frontend development"),
        ],
    ),
    TreeItem(
        id="maintenance",
        label="🔧 Maintenance Tasks",
        children=[
            TreeItem(id="task_m1", label="⏳ Update dependencies"),
            TreeItem(id="task_m2", label="❌ Security audit"),
            TreeItem(id="task_m3", label="✅ Backup verification"),
        ],
    ),
]

app_ui = ui.page_fluid(
    ui.h2("Task Selection Example"),
    ui.p("Select multiple tasks to perform batch operations."),
    ui.row(
        ui.column(
            6,
            ui.h4("Project Tasks"),
            input_treeview(
                id="task_tree",
                items=tree_data,
                multiple=True,
                expanded=["project_a", "project_b", "maintenance"],
                selected=["task_a1", "task_b1"],  # Pre-select completed tasks
            ),
        ),
        ui.column(
            6,
            ui.h4("Selected Tasks:"),
            ui.output_text("selected_tasks"),
            ui.br(),
            ui.h4("Batch Actions:"),
            ui.div(
                ui.actionButton(
                    "mark_complete", "Mark Complete", class_="btn-success btn-sm me-2"
                ),
                ui.actionButton(
                    "mark_progress",
                    "Mark In Progress",
                    class_="btn-warning btn-sm me-2",
                ),
                ui.actionButton(
                    "mark_todo", "Mark To Do", class_="btn-secondary btn-sm"
                ),
            ),
            ui.br(),
            ui.br(),
            ui.h4("Task Summary:"),
            ui.output_text("task_summary"),
        ),
    ),
)


def server(input, output, session):
    @render.text
    def selected_tasks():
        selected = input.task_tree()
        if selected and len(selected) > 0:
            task_names = []
            for task_id in selected:
                # Extract task name from the tree data
                for project in tree_data:
                    if project.id == task_id:
                        task_names.append(project.label)
                    elif hasattr(project, "children") and project.children:
                        for task in project.children:
                            if task.id == task_id:
                                task_names.append(task.label)
            return f"Selected {len(selected)} tasks:\n" + "\n".join(
                f"• {name}" for name in task_names
            )
        return "No tasks selected"

    @render.text
    def task_summary():
        # Count tasks by status based on emoji
        all_tasks = []
        for project in tree_data:
            if hasattr(project, "children") and project.children:
                all_tasks.extend(project.children)

        completed = len([t for t in all_tasks if "✅" in t.label])
        in_progress = len([t for t in all_tasks if "⏳" in t.label])
        todo = len([t for t in all_tasks if "❌" in t.label])

        return f"""Total Tasks: {len(all_tasks)}
Completed: {completed} ✅
In Progress: {in_progress} ⏳
To Do: {todo} ❌

Progress: {completed}/{len(all_tasks)} ({completed/len(all_tasks)*100:.0f}%)"""


app = App(app_ui, server)
