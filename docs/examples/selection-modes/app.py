from shiny.express import input, render, ui
from shiny_treeview import input_treeview
from data import tree_data

ui.h3("Single Selection (default)")
input_treeview(
    "single_tree",
    tree_data,
)

ui.h3("Multiple Selection")
ui.p("Hold Ctrl/Cmd or Shift while clicking to select multiple items.")
input_treeview(
    "multi_tree",
    tree_data,
    multiple=True,
)


@render.text
def single_value():
    return f"Single selection: {input.single_tree()}"


@render.text
def multi_value():
    selected = input.multi_tree()
    if selected:
        return f"Multiple selection: {', '.join(selected)}"
    else:
        return "Multiple selection: None"
