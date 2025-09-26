from shiny.express import input, render
from shiny_treeview import input_treeview
from data2 import tree_data

input_treeview(
    "my_tree",
    tree_data,
    multiple=True,
)


@render.text
def multi_value():
    selected = input.my_tree()
    if isinstance(selected, tuple):
        return f"Selected: {', '.join(selected)}"
    else:
        return f"Selected: {selected}"
