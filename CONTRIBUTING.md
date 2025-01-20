# Contributing to ShellSense

We love your input! We want to make contributing to ShellSense as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/venopyx/shellsense.git
   cd shellsense
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

We use several tools to maintain code quality:

- `black` for code formatting
- `isort` for import sorting
- `mypy` for type checking
- `flake8` for style guide enforcement

Before submitting a PR, please run:
```bash
black .
isort .
mypy shellsense
flake8
```

## Testing

We use pytest for testing. To run tests:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=shellsense
```

## Adding New Tools

1. Create a new tool class in the appropriate category directory under `shellsense/tools/`
2. Inherit from `BaseTool`
3. Implement the required methods
4. Add tests
5. Update documentation

Example:
```python
from shellsense.tools.base import BaseTool

class MyNewTool(BaseTool):
    """
    Description of what your tool does.
    """
    def invoke(self, input: dict) -> dict:
        # Implementation
        pass

    def get_schema(self) -> dict:
        # Schema definition
        pass
```

## Documentation

- Use docstrings for all public classes and methods
- Follow Google style docstrings
- Keep README.md updated
- Add examples for new features

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the docs with details of any new tools or features
3. The PR will be merged once you have the sign-off of at least one maintainer

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/venopyX/shellsense/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/venopyX/shellsense/issues/new).

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
