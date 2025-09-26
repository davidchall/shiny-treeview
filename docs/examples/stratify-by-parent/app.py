from shiny.express import input, render
from shiny_treeview import input_treeview, stratify_by_parent, TreeItem
from data4 import read_data


employees_db = read_data()

employees, manager_ids = [], []
for row in employees_db.values():
    label = "{icon} {name} ({title})".format(**row)
    employees.append(TreeItem(id=row["employee_id"], label=label))
    manager_ids.append(row["manager_id"] if row["manager_id"] else None)

# Convert flat data into hierarchical tree
tree_data = stratify_by_parent(employees, manager_ids)
input_treeview("org_tree", tree_data, selected="7")


@render.text
def selected_employee():
    selected = input.org_tree()
    if not selected:
        return "No employee selected"
    return employees_db[selected]["name"]
