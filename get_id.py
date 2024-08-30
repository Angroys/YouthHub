import asyncio
from telethon import TelegramClient

# Your Telegram API credentials
api_id = 23396138
api_hash = '870bf37c60ef75fec3802a87c7e69937'

# List of usernames for which you want to extract chat_ids
usernames = [
    "portalcivic"
]

async def main():
    # Create the Telegram client
    async with TelegramClient('anon', api_id, api_hash) as client:
        for username in usernames:
            try:
                entity = await client.get_entity(username)
                chat_id = entity.id
                print(f"{chat_id}")
            except Exception as e:
                print(f"Failed to get chat_id for {username}: {e}")

# Run the main function
asyncio.run(main())
