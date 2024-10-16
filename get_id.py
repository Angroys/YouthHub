import asyncio
from telethon import TelegramClient

# Your Telegram API credentials
api_id = 
api_hash = ''

# List of usernames for which you want to extract chat_ids
username = input("Write the channel name:")

async def main():
    # Create the Telegram client
    async with TelegramClient('anon', api_id, api_hash) as client:
        try:
            entity = await client.get_entity(username)
            chat_id = entity.id
            print(f"{chat_id}")
        except Exception as e:
            print(f"Failed to get chat_id for {username}: {e}")

# Run the main function
asyncio.run(main())
