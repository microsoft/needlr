# Contributing

## Getting Started for Contributors
1. Create a new branch that branches off the `dev` branch with one of the following naming conventions: (1) <name>-<task>, (2) <name>-dev-<task>, etc.
2. In your branch, make the necessary changes.
3. Commit changes and push your branch.
4. Create a pull request (PR) on Friday.

## Building from source

1. Create your own virual environment `virtualenv .venv`
2. Install the `uv` package `pip install uv==0.5.13`
3. Build the wheel using `uv build`

## uv overview

This project uses `uv` to manage the build and publish. For those developing on the source code, you'll need to be familiar with this package.

To install the package in an editable way in your virtual environment, use the command `uv pip install -e .`

### Updating dependencies

If you're adding dependencies for development, please use the dependency groups feature by running the command `uv add --dev <package name>`.

If you're adding dependencies for the package's functionality, please use the command `uv add <package name>`.
