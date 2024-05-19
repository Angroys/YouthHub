from telethon import TelegramClient, events, sync
import telethon
import os, re
from groq_api import GroqAPI

api_id = 23396138
api_hash = '870bf37c60ef75fec3802a87c7e69937'
client = TelegramClient('anon', api_id, api_hash)
ai_summarizer = GroqAPI('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')
download_folder = 'donwload/'

if not os.path.exists(download_folder):
    os.makedirs(download_folder)

@client.on(events.NewMessage(incoming=True, outgoing=True))
async def my_event_handler(event):
    chat = await event.get_chat()
    
    message_text = event.message.message
    photo = event.photo
    file_path = await event.message.download_media(file=download_folder)
    url = FindURLinTelegramMessage(message_text)
    summary_of_the_news = ai_summarizer.get_summary_of_the_news(url)
    print(summary_of_the_news)
    
    
def FindURLinTelegramMessage(string):
    
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]
 

    

client.start()
client.run_until_disconnected()