import requests
from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.environ['api_key']
api_secret = os.environ['api_secret']


def object_classifier(image_url):
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
        auth=(api_key, api_secret))
    

    return response.json()    