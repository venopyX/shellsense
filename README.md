# ShellSense

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![PyPI version](https://badge.fury.io/py/shellsense.svg)](https://badge.fury.io/py/shellsense)

A universal AI-powered terminal assistant for Linux

[Features](#features) •
[Installation](#installation) •
[Usage](#usage) •
[Development](#development) •
[Contributing](#contributing)

![ShellSense Demo](docs/images/shellsense-demo.gif)

</div>

## Features

- **AI Assistant**: Get expert help for any terminal task with multiple AI providers
- **Smart Search**: Integrated web search and Wikipedia lookup
- **Data Tools**: GitHub info, stock data, and product research
- **Translation**: Built-in support for multiple languages
- **Screenshots**: Capture webpage screenshots
- **Code Help**: Generate and explain code snippets
- **Rich Output**: Beautiful terminal formatting with loading animations
- **Universal**: Works with any Linux terminal (bash, zsh, fish, etc.)
- **Extensible**: Easy to add new tools and providers

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Chrome/Chromium (optional, for screenshots)

### Quick Install

```bash
pip install shellsense
```

That's it! ShellSense is now installed and ready to use.

### First-time Setup

Run the setup command to create your configuration:

```bash
shellsense --setup
```

This creates a configuration file at `~/.config/shellsense/config.env`. Edit this file with your API keys:

```env
# OpenAI API Keys (Optional)
OPENAI_API_KEY=your-openai-api-key

# Gemini API Keys (Optional)
GEMINI_API_KEY=your-gemini-api-key

# Cloudflare Environment Variables
CLOUDFLARE_ACCOUNT_ID=your-cloudflare-account-id
CLOUDFLARE_AUTH_TOKEN=your-cloudflare-auth-token
FUNCTION_CALL_MODEL=@hf/nousresearch/hermes-2-pro-mistral-7b
FRIENDLY_RESPONSE_MODEL=@hf/mistral/mistral-7b-instruct-v0.2
```

## Usage

### Basic Commands

```bash
# Show help and available commands
shellsense --help

# Use Specific AI Provider
shellsense -p gemini -q "What is the current weather in New York?"

# Default to Cloudflare AI
shellsense -q "Search Wikipedia for quantum computing"
```

### Available Tools

| Tool | Description |
|------|-------------|
| WebSearch | Search the web using Bing/DuckDuckGo |
| Wikipedia | Search and retrieve Wikipedia articles |
| Translator | Translate text between languages |
| Screenshot | Capture webpage screenshots |
| GitHub | Fetch GitHub user/repo information |
| Stock | Get real-time stock market data |
| ProductHunt | Discover trending tech products |
| Coder | Generate code snippets and explanations |

## Development

### Setup Development Environment

1. Clone and setup:
   ```bash
   git clone https://github.com/venopyX/shellsense.git
   cd shellsense

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate

   # Install in development mode with dev dependencies
   pip install -e ".[dev]"
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Build documentation:
   ```bash
   cd docs
   make html
   ```

4. Build and publish:
   ```bash
   python -m build
   twine upload dist/*
   ```

### Project Structure

```
shellsense/
├── shellsense/        # Main package
│   ├── ai/           # AI providers and models
│   │   └── providers/# AI provider implementations
│   ├── tools/        # Tool implementations
│   │   ├── coder/    # Code generation tools
│   │   ├── data/     # Data processing tools
│   │   ├── language/ # Language tools
│   │   ├── media/    # Media tools
│   │   ├── shell/    # Shell tools
│   │   └── web/      # Web tools
│   ├── config/       # Configuration management
│   ├── utils/        # Utility functions
│   └── __main__.py   # CLI entry point
├── tests/            # Test suite
├── docs/             # Documentation
│   ├── api/         # API reference
│   ├── guides/      # User guides
│   └── examples/    # Usage examples
└── pyproject.toml    # Project configuration
```

### Code Style

We use industry-standard Python tools:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all checks:
```bash
black .
isort .
flake8 .
mypy .
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## Documentation

For comprehensive documentation, visit our [Documentation](https://shellsense.readthedocs.io/en/latest/). Key sections include:

- [API Reference](https://shellsense.readthedocs.io/en/latest/api/index.html): Detailed API documentation
- [User Guides](https://shellsense.readthedocs.io/en/latest/guides/index.html): Step-by-step guides
- [Examples](https://shellsense.readthedocs.io/en/latest/examples/index.html): Usage examples
- [Contributing Guide](CONTRIBUTING.md): How to contribute

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [Documentation](docs/README.md)
- [Issue Tracker](https://github.com/venopyX/shellsense/issues)
- [Discussions](https://github.com/venopyX/shellsense/discussions)

---

<div align="center">
Made with ❤️ by the Gemechis Chala
</div>
