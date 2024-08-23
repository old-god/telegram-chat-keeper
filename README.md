# telegram-chat-keeper

Telegram-chat-keeper is a Telegram bot designed for automatic group management, including removing system messages, deleting messages with specific stop words, and automatically banning users.

## Features

- **System Message Removal**: The bot automatically removes system messages about users joining and leaving.
- **Stop Word Message Deletion**: The bot deletes messages containing specific stop words and bans the senders of such messages.
- **User Banning**: Users who send messages containing banned words are automatically banned.

## Requirements

- Python 3.7+ (if running without Docker)
- Docker (optional, for containerized deployment)

## Installation

### Using Python (without Docker)

1. Clone the repository:

    ```bash
    git clone https://github.com/old-god/telegram-chat-keeper.git
    cd telegram-chat-keeper
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your Telegram API token:

    ```bash
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ```

4. Run the bot:

    ```bash
    python main.py
    ```

### Using Docker

1. Clone the repository:

    ```bash
    git clone https://github.com/old-god/telegram-chat-keeper.git
    cd telegram-chat-keeper
    ```

2. Create a `.env` file in the root directory of the project and add your Telegram API token:

    ```bash
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ```

3. Build the Docker image:

    ```bash
    docker build -t telegram-chat-keeper .
    ```

4. Run the Docker container:

    ```bash
    docker run -d --name telegram-chat-keeper --env-file .env telegram-chat-keeper
    ```

## Configuration

### Stop Words

You can configure the stop words in the code to make the bot delete messages containing these words and ban the senders. To do this, edit the `STOP_WORDS` list in the `main.py` file:

```python
STOP_WORDS = ['@OrOpremkabot']
```

### Logging

The bot uses the standard `logging` module for logging. You can configure the logging level at the beginning of the `main.py` file:

```python
logging.basicConfig(level=logging.INFO)
```

### Environment Variables

Ensure that the `TELEGRAM_BOT_TOKEN` environment variable is set in your system or specified in the `.env` file. This is necessary for the bot to work.

## Usage

Once the bot is running, it will automatically monitor events in the groups it has joined. The bot will:

- Remove system messages about users joining and leaving.
- Delete messages containing prohibited words and ban the senders.

## Notes

- Ensure the bot has sufficient permissions in the group to delete messages and ban users.
- The bot can be deployed on a server, cloud infrastructure, or using Docker for continuous use.

## Support

If you have any questions or issues with using telegram-chat-keeper, please create an issue in the repository or contact the author.

## License

This project is licensed under the MIT License. See the LICENSE file for details.