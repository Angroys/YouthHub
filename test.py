import asyncio
from telethon import TelegramClient, events

# Your Telegram API credentials
api_id = 
api_hash = ''

# Chat IDs or usernames
source_chat_id = 'youthubmd'  # The chat from which you want to forward messages
destination_chat_id = 'youthubnews'  # The chat to which you want to forward messages

async def main():
    async with TelegramClient('forward_bot', api_id, api_hash) as client:
        # Fetch the entire message history from the source chat
        async for message in client.iter_messages(source_chat_id):
            # Forward the message to the destination chat
            await client.send_message(destination_chat_id, message)
            print(f"Message sent from {source_chat_id} to {destination_chat_id}")

        print("All messages have been forwarded.")

# Run the main function
asyncio.run(main())