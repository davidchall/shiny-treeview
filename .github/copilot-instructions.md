# GitHub Copilot Instructions for Shiny TreeView

## Project Overview
This is a Shiny for Python extension that provides a tree view component using Material-UI's RichTreeView. The package creates React-based tree components that integrate seamlessly with Shiny applications.

## Project Structure
```
shiny_treeview/
├── __init__.py          # Package exports
├── ui.py                # Main input_treeview component
├── tree.py              # Tree data structures
├── stratify.py          # Flat-to-nested conversion functions
├── utils.py             # Helper functions
└── distjs/index.js      # Prebuilt JavaScript bundle

srcts/                   # TypeScript source (builds to distjs/)
├── index.ts             # Main entry point
└── treeview.ts          # React component implementation

tests/                   # Test suite
├── test_*.py            # Unit tests
└── playwright/          # End-to-end browser tests

docs/                    # Quartodoc documentation
```

## Code Style and Conventions

### Python Code
- **Style**: Use Black formatting (line length 88) and avoid trailing whitespace
- **Imports**: Use isort for import organization
- **Type hints**: Always include type hints for public APIs
- **Docstrings**: Use NumPy-style docstrings for all public functions

## Key Patterns

### Data Structures
- `TreeItem`: Core data structure with `id`, `label`, and optional `children`
- Always validate tree data structure integrity
- Support both flat data (via stratify functions) and hierarchical data

### Component API Design
- Follow Shiny input component conventions
- Return `Tag` objects from component functions
- Use descriptive parameter names with sensible defaults
- Support both single and multiple selection modes

### Testing
- **Unit tests**: For data structures and utilities
- **Integration tests**: For component behavior
- **Browser tests**: Using Playwright for end-to-end testing
- Always test edge cases (empty trees, malformed data, etc.)

## Dependencies and Environment

### Production Dependencies
- `shiny >= 0.6.0` - Core Shiny framework
- `htmltools >= 0.6.0` - HTML generation utilities

### Development Dependencies
- `pytest` - Testing framework
- `playwright` - Browser testing
- `black` - Code formatting
- `isort` - Import sorting
- `quartodoc` - Documentation generation

### JavaScript Build
- Package ships with prebuilt JavaScript bundle
- End users don't need Node.js/npm
- Developers need Node.js only for JS development

## Documentation

### API Documentation
- Generated automatically with Quartodoc
- Deployed to GitHub Pages
- Include practical examples in docstrings

### Examples
- Provide complete, runnable examples
- Cover basic usage, file browser patterns, multiple selection
- Examples should be copy-pasteable

## Error Handling
- Validate tree data structure on input
- Provide helpful error messages for malformed data
- Handle edge cases gracefully (empty selections, missing IDs)

## Performance Considerations
- Tree components should handle reasonably large datasets (1000+ items)
- Use efficient data structures for tree operations
- Minimize re-renders in React components

## When Contributing
- Run tests before submitting: `pytest`
- Format code: `black .` and `isort .`
- Update documentation if changing APIs
- Add tests for new functionality
- Follow semantic versioning for releases

## Specific to This Project
- This is a **UI component library**, not an application
- Focus on **developer experience** - easy to use, well-documented
- **React/MUI integration** is handled internally - users just work with Python
- **Backwards compatibility** is important once released
- **Examples** should be practical and demonstrate real-world usage patterns
