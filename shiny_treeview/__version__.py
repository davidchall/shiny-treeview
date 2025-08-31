"""Version information for shiny-treeview."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("shiny-treeview")
except PackageNotFoundError:
    # Package not installed, fall back to a default
    __version__ = "0.0.0+unknown"
