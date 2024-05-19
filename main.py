import re, io, requests, os, hashlib, asyncio, time
from PIL import Image
from python_dependencies.telegram_api_code import TelegramClass
from python_dependencies.groq_api import GroqAPI
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


donwload_path = 'download/'
grok_api_key = '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'
api_id = 23396138
api_hash = '870bf37c60ef75fec3802a87c7e69937'
telegram_client = TelegramClass(api_id, api_hash, donwload_path)
ai_summarizer = GroqAPI(grok_api_key)

def extractImageFromArticle(url:str):
    image_content = requests.get(url[0]).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)
    return image
    
    
async def get_a_Summarizer_and_the_Image():
    link =  await telegram_client.run_code()
    if link:
        title = ai_summarizer.write_a_article_title(link)
        summary_of_the_news = ai_summarizer.get_summary_of_the_news(link)
        makeHTMLfile(title, summary_of_the_news, link)
    else:
        print("No URL found in the message.")

def makeHTMLfile(title, text, link):
    
    env = Environment(loader=FileSystemLoader('templates'))  

    template = env.get_template('article_template.html')


    article_data = {
        'article_title': title,
        'article_date': time.time(),
        'article_image': 'download\image.png',
        'paragraph_1': text
        
    }

    rendered_template = template.render(article_data)

    
    output_folder = 'articles'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file_path = os.path.join(output_folder, 'new_article.html')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(rendered_template)

asyncio.run(get_a_Summarizer_and_the_Image())