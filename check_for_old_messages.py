import asyncio, os, sys, logging, time

sys.path.append(os.path.abspath(os.path.dirname('python_dependencies\groq_api.py')))

from jinja2 import Environment, FileSystemLoader
from python_dependencies.telegram_api_code import TelegramClass
from python_dependencies.groq_api import GroqAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
grok_api_key = ''
api_id = 
api_hash = ''
download_path = 'download/'

# Initialize Telegram and Groq clients
telegram_client = TelegramClass(api_id, api_hash, download_path, groq_api_key=grok_api_key)
groq_client = GroqAPI(grok_api_key)

# List of organizations (chat IDs or usernames)
organizations = [
    "sigmo_ai"



]

async def fetch_past_messages(chat_id, limit=100):
    messages = []
    try:
        # Fetch past messages from the chat
        async for message in telegram_client.client.iter_messages(chat_id, limit=limit):
            messages.append(message)
            logger.info(f"Message ID: {message.id}, Sender ID: {message.sender_id}, Text: {message.text}")
    except Exception as e:
        logger.error(f"Error fetching messages from {chat_id}: {e}")
    return messages

async def run_bot():
    try:
        await telegram_client.connect()  # Ensure connection
        logger.info("Bot is running and listening for messages...")

        for chat in organizations:
            messages = await fetch_past_messages(chat, 25)
            for message in messages:
                try:
                    if groq_client.messageIsAnOpportunity(message.message) == 'True':
                        summary = groq_client.get_summary_of_the_news(message.message)
                        await telegram_client.send_mess(summary, chat_id="youthubmdtest")
                except Exception as e:
                    logger.error(f"Error processing message in chat {chat}: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await telegram_client.disconnect()  # Disconnect after all tasks are complete


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except asyncio.CancelledError:
        logger.error("The main task was cancelled.")
    except Exception as e:
        logger.error(f"An error occurred in the main execution: {e}")
