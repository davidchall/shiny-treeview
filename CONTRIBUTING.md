# Contributing to Shiny TreeView

Thank you for your interest in contributing to Shiny TreeView! This guide will help you get started with local development and submitting contributions.

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 16+** (only needed for JavaScript development)
- **Git**

### Local Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/shiny-treeview.git
   cd shiny-treeview
   ```

2. **Create a virtual environment**:
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the package in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install JavaScript dependencies** (if working on the React component):
   ```bash
   npm install
   ```

### Development Workflow

#### Python Development

1. **Make your changes** to the Python code in `shiny_treeview/`

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Format code**:
   ```bash
   black .
   isort .
   ```

#### JavaScript/TypeScript Development

1. **Make changes** to TypeScript code in `srcts/`

2. **Build the JavaScript bundle**:
   ```bash
   npm run build
   ```

3. **For continuous development** (auto-rebuild on changes):
   ```bash
   npm run watch
   ```

4. **Test the example app**:
   ```bash
   cd example-app
   python -m shiny run app.py --reload
   ```

#### Documentation Development

1. **Install Quarto**:
   - Download from [quarto.org](https://quarto.org/docs/get-started/)
   - Or on macOS: `brew install quarto`

2. **Build API documentation**:
   ```bash
   cd docs
   quartodoc build
   ```

3. **Render the documentation site**:
   ```bash
   quarto render
   ```

4. **Preview locally**:
   ```bash
   quarto preview
   ```

## Submitting a Pull Request

### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the development workflow above

3. **Add tests** for any new functionality

4. **Update documentation** if you're changing APIs

5. **Commit your changes** with descriptive commit messages:
   ```bash
   git commit -m "Add support for custom tree icons"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub with:
   - Clear description of what the PR does
   - Link to any related issues
   - Screenshots/examples if relevant
   - Notes about breaking changes (if any)

## Release Process

(For maintainers)

1. Update version in `package.json`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v0.1.1`
4. Push tag: `git push origin v0.1.1`
5. GitHub Actions will automatically build and publish to PyPI

## Getting Help

- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the [online documentation](https://davidchall.github.io/shiny-treeview)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Please be respectful and inclusive in all interactions.

## License

By contributing to Shiny TreeView, you agree that your contributions will be licensed under the MIT License.
