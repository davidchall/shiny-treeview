from shiny.express import input, render
from shiny_treeview import input_treeview
from data1 import tree_data

input_treeview("my_tree", tree_data)


@render.text
def value():
    return f"Selected: {input.my_tree()}"
