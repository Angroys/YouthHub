import os
from groq import Groq


class GroqAPI():
    def __init__(self, user_api_key : str):
        self.client = Groq(api_key=user_api_key)


    def get_summary_of_the_news(self, link: str):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Give a summary on the information given on this link {}".format(link) ,
            }
        ],
        model="llama3-8b-8192"
        )
        return chat_completion.choices[0].message.content

    