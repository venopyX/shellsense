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

- **Chat with OpenAI GPT Model**:
  ```bash
  shellsense -c "Your query here"
  ```

- **Chat with Cloudflare AI Model**:
  ```bash
  shellsense -cf "Your query here"
  ```

- **Process a Query with CopiloHero Tools**:
  ```bash
  shellsense -q "Your query here"
  ```

### Aliases

- **shellsense**: Main command to interact with the plugin.
- **sschat**: Alias for `shellsense -c`.
- **sscfchat**: Alias for `shellsense -cf`.
- **ssai**: Alias for `shellsense -q`.

## Configuration

Configure your environment variables in the `config/example.env` file:

```env
CLOUDFLARE_ACCOUNT_ID=your-cloudflare-account-id
CLOUDFLARE_AUTH_TOKEN=your-cloudflare-auth-token
OPENAI_API_KEY=your-openai-api-key-here-you-can-skip-this
FUNCTION_CALL_MODEL=@hf/nousresearch/hermes-2-pro-mistral-7b
FRIENDLY_RESPONSE_MODEL=@hf/mistral/mistral-7b-instruct-v0.2
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Open a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please open an issue on the GitHub repository or contact the maintainers directly.

---

![ShellSense UI Example](shellsense-home-screenshot.png)

Experience the future of terminal interaction with ShellSense. Enhance your productivity and unlock new capabilities with intelligent AI integration.