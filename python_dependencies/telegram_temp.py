import asyncio, logging

from telethon import TelegramClient, events
from telethon.tl import types
from groq_api import GroqAPI

class TelegramClass:
    def __init__(self, api_id, api_hash, path, groq_api_key):
        self.api_id = api_id
        self.api_hash = api_hash
        self.path = path
        self.client = TelegramClient('anon', api_id, api_hash, timeout=30)
        self.event_processed = asyncio.Event()
        self.message_text = None
        self.groq_client = GroqAPI(groq_api_key)
        self.client.add_event_handler(self.my_event_handler, events.NewMessage(incoming=True, outgoing=True))
        self.organizations = []

        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    async def connect(self):
        try:
            await self.client.start()
            self.logger.info("Connected to Telegram.")
        except Exception as e:
            self.logger.error(f"Failed to connect to Telegram: {e}")
            raise

    async def disconnect(self):
        try:
            await self.client.disconnect()
            self.logger.info("Disconnected from Telegram.")
        except Exception as e:
            self.logger.error(f"Failed to disconnect from Telegram: {e}")

    async def my_event_handler(self, event):
        try:
            self.chat = await event.get_chat()
            if isinstance(self.chat, (types.Chat, types.Channel)) and any(titlu in self.chat.title for titlu in self.organizations):
                self.message_text = event.message.message
                self.logger.info(f"Message processed: {self.message_text}")
                if(self.groq_clinet.messageIsAnOpportunity(self.message_text) == 'True'):
                    await self.send_mess(self.groq_clinet.get_summary_of_the_news(self.message_text))
                self.event_processed.set()
                for chat in self.organizations:
                    messages = self.fetch_past_messages(chat)
                    for message in messages[::-1]:
                        if(self.groq_clinet.messageIsAnOpportunity(message) == 'True'):
                            await self.send_mess(self.groq_clinet.get_summary_of_the_news(message))

        except Exception as e:
            self.logger.error(f"Error in event handler: {e}")
            self.event_processed.set()  # Avoid deadlock in case of errors

    async def send_mess(self, message, chat_id="youthubmd", max_retries=3):
        for attempt in range(max_retries):
            try:
                await self.client.send_message(entity=chat_id, message=message)
                self.logger.info("Message sent successfully.")
                return
            except asyncio.CancelledError:
                self.logger.warning("Message sending was cancelled.")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                self.logger.error(f"Failed to send message (attempt {attempt + 1}): {e}")
                if attempt + 1 == max_retries:
                    raise
    
    async def fetch_past_messages(self, chat_id, limit=10):
        try:
            # Connect to theself.client
            await self.client.start()

            # Fetch past messages from the chat
            messages = []
            async for message in self.client.iter_messages(chats, limit=limit):
                messages.append(message)
                print(f"Message ID: {message.id}, Sender ID: {message.sender_id}, Text: {message.text}")

            return messages
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await self.client.disconnect()

