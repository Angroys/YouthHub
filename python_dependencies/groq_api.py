import os
import re
import time
from groq import Groq
import logging
from difflib import SequenceMatcher

class GroqAPI():
    def __init__(self, user_api_key: str):
        self.client = Groq(api_key=user_api_key)
        self.message_cache = []

    def get_summary_of_the_news(self, text: str):
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        urls = re.findall(url_pattern, text)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": """ 
                                Scrie un text în limba română și nu adăuga comentarii adiționale pe care le scrii la început. În plus extrage linkul din mesajul primit și punel la sfârșit
                                Scrie textul strict după acest script:
                                [rocket emoji]Titlu de 10 cuvinte

                                [emoji]O descriere de două propoziții care începe cu un emoji

                                [emoji cu calendar][extrage data din link oferit sau pune deadline de aplicare din articol]{}
                                {}""".format(urls[0] ,text)      
                }
            ],
            model="llama-3.1-70b-versatile"
        )
        return chat_completion.choices[0].message.content

    def is_similar_message(self, message: str, threshold: float = 0.3):
        for cached_message in self.message_cache:
            similarity = SequenceMatcher(None, message, cached_message).ratio()
            if similarity >= threshold:
                return True
        return False

    def messageIsAnOpportunity(self, telegram_message: str):
        if self.is_similar_message(telegram_message):
            return "False"

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": """You will receive a message from telegram below. You don't have to comment. 
                    You just have to say 'True' or 'False' if its an volunteering opportunity or participation in an event or something for work, but mostly volunteering, events, hackathons, camps & bootcamps, or some courses sau concursuri cu premii.: 
                    Evenimentele trebuie în perioada 1 august 2024 - 31 decembrie 2024. Intră pe linkuri și citește informația de pe ele{}""".format(telegram_message) ,
                }
            ],
            model="llama-3.1-70b-versatile"
        )

        result = chat_completion.choices[0].message.content
        print(result)

        # Add the message to the cache if it's a new opportunity
        if result.strip().lower() == 'true':
            self.message_cache.append(telegram_message)

        return result

# API KEY = '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'