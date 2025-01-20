# ShellSense Plugin

## Overview

ShellSense is an advanced, futuristic Zsh terminal plugin designed to integrate intelligent AI capabilities directly into your command-line interface. This plugin leverages state-of-the-art AI models and a suite of powerful tools to provide expert assistance for a wide range of tasks.

## Key Features

- **AI Assistant in the Terminal**: Get expert assistance directly in your Zsh terminal for various tasks.
- **Integrated Tools**:
  - **WebSearchTool**: Perform web searches.
  - **CrawlerTool**: Scrape webpage content.
  - **ProductHuntTool**: Get trending products.
  - **ScreenshotTool**: Capture webpage screenshots.
  - **TranslatorTool**: Translate text.
  - **WikipediaSearchTool**: Search Wikipedia.
  - **CoderTool**: Generate code snippets.
  - **GitHubTool**: Fetch GitHub user info.
  - **CommandExecutionTool**: Execute shell commands.
  - **StockTool**: Fetch stock data.

## Installation

### Prerequisites

- Python 3.8 or higher
- Zsh shell
- ChromeDriver installed and path set up for the **ScreenshotTool** to function properly.

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/shellsense.git
   cd shellsense
   ```

2. **Install Dependencies**:
   ```bash
   ./setup.sh
   ```

3. **Add ShellSense to Your Zsh Configuration**:
   The setup script will automatically add the necessary configurations to your `.zshrc` file. Restart your terminal or run `source ~/.zshrc` to activate ShellSense.

## Usage

### Commands

- **Setup**
  ```bash
  shellsense --setup
  ```

- **Ask ShellSense a Question**
  ```bash
  shellsense -q "Your question here"
  ```

- **Choose an AI Provider**
  ```bash
  shellsense -p gemini -q "Your question here"
  ```

## Configuration

Configure your environment variables in the `config/example.env` file:

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

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Open a pull request with a clear description of your changes.

## Documentation

For comprehensive documentation, please visit the [ShellSense Documentation](https://github.com/venopyX/shellsense/tree/main/docs).

# ShellSense Documentation

## Overview

Welcome to the ShellSense documentation! This directory contains comprehensive documentation for ShellSense, a universal AI-powered terminal assistant for Linux.

## Documentation Structure

```
docs/
├── api/            # API Reference documentation
│   ├── providers/  # AI provider documentation
│   ├── tools/      # Tool documentation
│   └── utils/      # Utility documentation
├── guides/         # User guides and tutorials
├── examples/       # Usage examples
└── images/         # Documentation images
```

## Building the Documentation

### Prerequisites

- Python 3.8 or higher
- Sphinx documentation generator

### Build Steps

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Build the documentation:
   ```bash
   cd docs
   make html
   ```

3. View the documentation:
   ```bash
   # On Linux with xdg-open
   xdg-open build/html/index.html
   ```

## Documentation Sections

### API Reference

Detailed documentation of ShellSense's internal APIs:

- **AI Providers**: Documentation for Cloudflare, OpenAI, and Gemini providers
- **Tools**: Documentation for all available tools
- **Utilities**: Documentation for utility functions and classes

### User Guides

Step-by-step guides for using ShellSense:

- **Quickstart Guide**: Get up and running quickly
- **Configuration Guide**: Detailed configuration options
- **Provider Guide**: Information about different AI providers
- **Tool Guide**: Details about available tools and their usage

### Examples

Real-world examples of using ShellSense:

- **Basic Usage**: Common use cases
- **Advanced Usage**: Complex scenarios
- **Custom Tools**: Creating custom tools

## Contributing to Documentation

We welcome documentation improvements! Here's how you can help:

1. Fork the repository
2. Make your documentation changes
3. Build and test locally
4. Submit a pull request

### Documentation Style Guide

- Use clear, concise language
- Include code examples where relevant
- Follow RST/Sphinx formatting guidelines
- Add docstrings to all Python code
- Keep examples up-to-date

## Getting Help

If you find any issues or have suggestions for improving the documentation:

- [Open an Issue](https://github.com/venopyX/shellsense/issues)
- [Join Discussions](https://github.com/venopyX/shellsense/discussions)
- [Contributing Guide](../CONTRIBUTING.md)

---

<div align="center">
Made with ❤️ by the Gemechis Chala
</div>
