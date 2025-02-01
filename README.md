# marzban-broadcast
Broadcast a message to all marzban users


## Quickstart

1. Create .env file
    ```
    TG_BOT_TOKEN=XXXXXXX
    API_BASE_URL=base URL of your marzban panel
    ADMIN_TOKEN=admin token for marzban panel
    ```
2. Create `message` file with your message. [Example](https://github.com/kutovoys/marzban-torrent-blocker/blob/715cae4f043633971ed37488b0221b1fba7b9ce9/config/config.go#L13)
3. `poetry self add poetry-plugin-dotenv`
4. `poetry run python broadcast.py`