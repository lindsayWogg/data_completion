import requests
import os
from dotenv import load_dotenv

load_dotenv()

def search_pixabay_images(key_words):
    url=os.getenv('url_img_search').format(api_key=os.getenv('pixabay_key'),query=key_words)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if 'hits' in data:
            image_links = [item['largeImageURL'] for item in data['hits']]
            return image_links
    return None
