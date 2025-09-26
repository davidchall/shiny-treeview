from shiny_treeview import TreeItem

tree_data = [
    TreeItem(
        id="movies",
        label="🎬 Movies",
        children=[
            TreeItem(
                id="action",
                label="💥 Action",
                children=[
                    TreeItem(id="diehard", label="Die Hard"),
                    TreeItem(id="madmax", label="Mad Max: Fury Road"),
                ],
            ),
            TreeItem(
                id="comedy",
                label="😂 Comedy",
                children=[
                    TreeItem(id="groundhog", label="Groundhog Day"),
                    TreeItem(id="princess", label="The Princess Bride"),
                ],
            ),
        ],
    ),
    TreeItem(
        id="music",
        label="🎵 Music",
        children=[
            TreeItem(
                id="rock",
                label="🎸 Rock",
                children=[
                    TreeItem(id="queen", label="Queen - Bohemian Rhapsody"),
                    TreeItem(id="beatles", label="The Beatles - Hey Jude"),
                ],
            ),
            TreeItem(
                id="jazz",
                label="🎺 Jazz",
                children=[
                    TreeItem(id="miles", label="Miles Davis - Kind of Blue"),
                    TreeItem(id="coltrane", label="John Coltrane - A Love Supreme"),
                ],
            ),
        ],
    ),
    TreeItem(
        id="podcasts",
        label="🎙️ Podcasts",
        children=[
            TreeItem(id="tech-podcast", label="Tech Talk Weekly"),
        ],
    ),
    TreeItem(id="home-video", label="📹 Family Vacation 2023"),
]
