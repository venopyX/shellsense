# ShellSense Plugin

## Overview

ShellSense is an advanced, futuristic Zsh terminal plugin designed to integrate intelligent AI capabilities directly into your command-line interface. This plugin leverages state-of-the-art AI models and a suite of powerful tools to provide expert assistance for a wide range of tasks, from Linux terminal mastery to programming support and beyond.

## Features

- **Linux Terminal Mastery**: Solve zsh issues, recommend commands, scripts, and shortcuts, and assist with zsh configuration and optimization.
- **Programming Support**: Debug code, solve programming challenges, and provide optimized code snippets and best practices.
- **Cybersecurity Guidance**: Advise on ethical hacking, penetration testing, and system hardening.
- **Tech Knowledge**: Explain concepts, tools, and techniques across AI, science, and technology.
- **Integrated Tools**: Utilize a variety of tools for web searches, stock analysis, GitHub user info, product trends, and more.

## Installation

### Prerequisites

- Python 3.8 or higher
- Zsh shell

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

#### Example:
- Using `ssai` instead of `shellsense -q`
  ```sh
  ssai "Who is venopyx on github"
  ```

## Tools

ShellSense comes with a variety of integrated tools to enhance your terminal experience:

- **StockTool**: Fetch current stock prices, company profiles, and analyst recommendations.
- **WebSearchTool**: Perform Google searches and retrieve top results.
- **CrawlerTool**: Scrape visible text and metadata from webpages.
- **ProductHuntTool**: Retrieve top trending products from Product Hunt.
- **ScreenshotTool**: Capture screenshots of webpages.
- **TranslatorTool**: Translate text between different languages.
- **WikipediaSearchTool**: Perform Wikipedia searches and return relevant pages.
- **CoderTool**: Generate concise, well-structured code snippets.
- **GitHubTool**: Fetch publicly available information about GitHub users.
- **CommandExecutionTool**: Execute shell commands and handle file/folder operations.

## Configuration

Configure your environment variables in the `config/example.env` file:

```env
CLOUDFLARE_ACCOUNT_ID=your-cloudflare-account-id
CLOUDFLARE_AUTH_TOKEN=your-cloudflare-auth-token
OPENAI_API_KEY=your-openai-api-key [OPTIONAL]
FUNCTION_CALL_MODEL=@hf/nousresearch/hermes-2-pro-mistral-7b [OPTIONAL]
FRIENDLY_RESPONSE_MODEL=@hf/mistral/mistral-7b-instruct-v0.2 [OPTIONAL]
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
