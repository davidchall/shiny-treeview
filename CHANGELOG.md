# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-10-01

### Added
- New [Examples](https://davidchall.github.io/shiny-treeview/examples.html) page in the documentation website, featuring live demos of usage patterns.

## [0.1.0] - 2025-09-14

### Added
- Select from hierarchical data in your [Shiny for Python](https://shiny.posit.co/py/) apps via `input_treeview()`.
    - Parameters: `id`, `items`, `selected`, `expanded`, `multiple`, `checkbox`, `width`.
- Create hierarchical data with nested `TreeItem` objects.
    - Parameters: `id`, `label`, `caption`, `children`, `disabled`.
- Convert flat to hierarchical data with helper functions: `stratify_by_parent()`.

[unreleased]: https://github.com/davidchall/shiny-treeview/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/davidchall/shiny-treeview/releases/tag/v0.1.1
[0.1.0]: https://github.com/davidchall/shiny-treeview/releases/tag/v0.1.0
