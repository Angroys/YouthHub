import asyncio, os, sys, logging

sys.path.append(os.path.abspath(os.path.dirname('python_dependencies\groq_api.py')))

from jinja2 import Environment, FileSystemLoader
from python_dependencies.telegram_api_code import TelegramClass
from python_dependencies.groq_api import GroqAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
grok_api_key = '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'
api_id = 23396138
api_hash = '870bf37c60ef75fec3802a87c7e69937'
download_path = 'download/'

telegram_client = TelegramClass(api_id, api_hash, download_path, grok_api_key)

async def run_bot():
    try:
        await telegram_client.connect()
        logger.info("Bot is running and listening for messages...")
        await telegram_client.client.run_until_disconnected()  # Run the client
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await telegram_client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except asyncio.CancelledError:
        logger.error("The main task was cancelled.")
    except Exception as e:
        logger.error(f"An error occurred in the main execution: {e}")   