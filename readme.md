# Keysmith Bot

Keysmith Bot is a Telegram bot designed to generate and manage ciphers. It uses MD5 and PBKDF2 for hashing and allows users to create custom or random ciphers. The bot also supports multiple languages and automatically deletes messages after a specified delay.

## Features

- **Custom Cipher Generation**: Users can provide their own cipher and length to generate a custom hash.
- **Random Cipher Generation**: Users can request a random cipher to be generated.
- **Message Deletion**: Automatically deletes messages after a specified delay to maintain privacy.
- **Language Support**: Supports multiple languages (English, Italian, Portuguese).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Smiley-94/keysmithBot.git
    cd keysmithBot
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Prepare the image for the bot:
    ```bash
    docker build .
    ```
4. Run the bot as a Docker container:
    ```bash
    docker run -d --name "your_container_name" -e botToken="your_bot_token" your_image_name
    ```
remember to replace "your_bot_token" with your actual bot token and "your_container_name" with the desired container
name.

## Usage

1. Start the bot by sending `/start` to the bot in Telegram.
2. Choose between generating a custom cipher or a random cipher by clicking the respective button.
3. Follow the prompts to provide the necessary information.
4. The bot will generate and display the cipher, then delete the messages after the specified delay.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements.

## License

This project is licensed under the MIT License.
