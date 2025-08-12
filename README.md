# Bluesky Crowdin Turkish Translation Reporter

This scraper is generated for the Bluesky Turkish translation team. It monitors the translation progress and sends notifications via Discord when updates occur.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/mertssmnoglu/mertssmnoglu/bluesky-crowdin-turkish-translation-reporter.git
   cd mertssmnoglu/bluesky-crowdin-turkish-translation-reporter
   ```

2. Prepare the environment:

    ```bash
    uv venv --python 3.12
    ```

3. Install the required dependencies:

   ```bash
   uv sync
   ```

4. Create a `.env` file in the root directory and add your Discord webhook URL:

   ```env
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
   ```

5. Run the application:

   ```bash
   uv run main.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
