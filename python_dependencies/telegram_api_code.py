import asyncio
import logging
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
        self.client.add_event_handler(self.my_event_handler, events.NewMessage())
        self.organizations = [
    "1452970035",
    "1190874605",
    "1704244304",
    "2018595248",
    "1640771696",
    "1572721193",
    "1458904601",
    "1209366368",
    "1918262723",
    "1445720900",
    "1276209494",
    "2060715853",
    "1727255311",
    "1695314357",
    "1155841239",
    "2102711645",
    "1632951890",
    "1718986183",
    "5522937027",
    "2209469557",
    "1718986183",
    "1155841239"
]


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
            self.logger.info("New message event detected.")
            self.chat = await event.get_chat()
            chat_id_str = str(self.chat.id)

            if isinstance(self.chat, (types.Chat, types.Channel)) and chat_id_str in str(self.organizations):   
                self.logger.info("It worked")
                self.message_text = event.message.message
                self.logger.info(f"Message processed: {self.message_text}")

                if(self.groq_client.messageIsAnOpportunity(self.message_text) == 'True'):
                    self.logger.info("Yes, it does")
                    await self.send_mess(self.groq_client.get_summary_of_the_news(self.message_text))
                self.event_processed.set()
        except Exception as e:
            self.logger.error(f"Error in event handler: {e}")
            self.event_processed.set()  # Avoid deadlock in case of errors

    async def send_mess(self, message, chat_id="youthubmdtest", max_retries=3):
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