import asyncio
from telethon import TelegramClient, events
import os, re, telethon, telethon.client
from telethon.tl import types


class TelegramClass:



    def __init__(self, api_id, api_hash, path) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.path = path
        self.client = TelegramClient('anon', api_id, api_hash)
        self.url = None  # To store the URL found in the message
        self.event_processed = asyncio.Event()  # Event to signal message processing is done
        self.client.add_event_handler(self.my_event_handler, events.NewMessage(incoming=True, outgoing=True))
        self.organizations = [
    "Centrul Municipal de Tineret Chișinău",
    "Oportunități",
    "TECHNOVATOR",
    "SIGMOID",
    "antreprenor.md",
    "Clubul Ingineresc Micro Lab",
    "Asociația Internațională a Tinerilor ✨",
    "Oportunități PNTP",
    "Startup Moldova",
    "YouthHub"
    ]        
            
    async def my_event_handler(self, event):
        self.chat = await event.get_chat()
        if isinstance(self.chat, types.Chat) or isinstance(self.chat, types.Channel): 
            for titlu in self.organizations:
                if titlu == self.chat.title:
                    self.message_text = event.message.message
                    self.photo = event.photo
                    print(self.message_text)
                    self.url = self.FindURLinTelegramMessage(self.message_text)
                    self.check_if_Folder_exists(self.path)
                    await self.download_media(event, self.path)
                    self.event_processed.set()  
                    await self.client.disconnect() 

    async def download_media(self, event, path: str):
        await event.message.download_media(path)    

    def check_if_Folder_exists(self, download_folder: str):
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)         
    
    def FindURLinTelegramMessage(self, message: str):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, message)
        return url[0] if url else None
    
    async def run_code(self):
        await self.client.start()
        await self.event_processed.wait()  
        return self.url 
