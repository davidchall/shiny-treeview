from shiny_treeview import TreeItem

tree_data = [
    TreeItem(
        id="groceries",
        label="🛒 Groceries",
        children=[
            TreeItem(
                id="produce",
                label="🥬 Produce",
                children=[
                    TreeItem(id="bananas", label="🍌 Bananas"),
                    TreeItem(id="spinach", label="🍃 Fresh Spinach"),
                    TreeItem(id="tomatoes", label="🍅 Cherry Tomatoes"),
                ],
            ),
            TreeItem(
                id="dairy",
                label="🥛 Dairy",
                children=[
                    TreeItem(id="milk", label="🥛 Whole Milk"),
                    TreeItem(id="cheese", label="🧀 Cheddar Cheese"),
                    TreeItem(id="yogurt", label="🥄 Greek Yogurt"),
                ],
            ),
        ],
    ),
    TreeItem(
        id="household",
        label="🏠 Household",
        children=[
            TreeItem(
                id="cleaning",
                label="🧽 Cleaning",
                children=[
                    TreeItem(id="detergent", label="🧴 Laundry Detergent"),
                    TreeItem(id="sponges", label="🧽 Kitchen Sponges"),
                ],
            ),
        ],
    ),
    TreeItem(id="batteries", label="🔋 AA Batteries"),
    TreeItem(id="gift", label="🎁 Birthday Gift Wrap"),
]
