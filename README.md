# ShellSense: AI-Powered Zsh Plugin

ShellSense is an intelligent Zsh plugin designed to enhance your terminal experience with powerful features and AI-powered capabilities. Developed using Python, ShellSense offers a streamlined workflow for various tasks, making your terminal more efficient and user-friendly.

## Features

- **AI-Powered Copilot**: Utilize AI models to assist with coding, debugging, and various terminal tasks.
- **Integrates Python with Zsh**: Seamlessly blend the power of Python with Zsh for enhanced functionality.
- **Modular and Scalable Design**: Easily extend and customize the plugin to fit your needs.
- **Secure Environment Variable Management**: Safely manage and use environment variables.
- **Chat with AI Models**: Interact with OpenAI and Cloudflare AI models directly from your terminal.
- **Dynamic Tool Aggregator**: Utilize Cloudflare's AI Function Calling to provide various functionalities like GitHub user info retrieval, stock analysis, web scraping, and more.
- **GitHub User Info**: Fetch public details of GitHub users.
- **Stock Analysis**: Retrieve real-time stock data, company profiles, and analyst recommendations.
- **Web Scraping**: Extract visible text and metadata from webpages.
- **Product Hunt Leaderboard**: Get the latest trending products on Product Hunt.
- **Web Search**: Perform Google search and retrieve top results.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/zsh-python-plugin.git
    cd zsh-python-plugin
    ```

2. **Run the Setup Script**:
    ```bash
    ./setup.sh
    ```

3. **Add Your `.env` Configurations**:
    ```bash
    cp config/example.env .env
    ```

    ### `.env` Variables:

    | Variable                | Description                                  |
    |-------------------------|----------------------------------------------|
    | `OPENAI_API_KEY`        | OpenAI API key                               |
    | `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID                         |
    | `CLOUDFLARE_AUTH_TOKEN` | Cloudflare authentication token               |
    | `ACCOUNT_ID`            | Cloudflare's unique account ID                |
    | `API_TOKEN`             | Authentication token for tools                |
    | `MODEL_NAME`            | Name of the AI model used in tools            |

4. **Restart Your Terminal or Use**:
    ```bash
    source ~/.zshrc
    ```

## Usage

- **Chat with OpenAI Models**:
    ```bash
    shellsense -c "Your query here"
    ```

- **Chat with Cloudflare's Models**:
    ```bash
    shellsense -cf "Your query here"
    ```

- **Process a Query with CopiloHero Tools**:
    ```bash
    shellsense -q "Your query here"
    ```

## Example Queries

- **Retrieve GitHub User Info**:
    ```bash
    shellsense -q "Get information about the GitHub user 'octocat'."
    ```

- **Get Current Stock Price**:
    ```bash
    shellsense -q "Get the current stock price of 'AAPL'."
    ```

- **Capture a Screenshot of a Webpage**:
    ```bash
    shellsense -q "Capture a screenshot of 'https://example.com'."
    ```

- **Fetch Trending Products from Product Hunt**:
    ```bash
    shellsense -q "Fetch trending products from Product Hunt."
    ```

- **Perform a Google Search**:
    ```bash
    shellsense -q "Perform a Google search for 'latest tech news'."
    ```

## Contributing

Feel free to fork this project, open issues, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries, please contact: [your-email@example.com](mailto:your-email@example.com)

## Future Features

ShellSense is continuously evolving with many more features in development. Stay tuned for updates!
