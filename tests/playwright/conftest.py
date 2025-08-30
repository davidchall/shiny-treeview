"""Pytest configuration and fixtures for shiny-treeview tests."""

from shiny.pytest import create_app_fixture

# Create the app fixture using Shiny's testing infrastructure
# This points to the app.py file in the same directory
local_app = create_app_fixture("app.py")
