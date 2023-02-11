import requests
import re
import os

from google_images_search import GoogleImagesSearch

GIS = GoogleImagesSearch(os.environ['GOOGLE_API_KEY'], os.environ['GOOGLE_SEARCH_ENGINE_ID'])

class Card:
    def __init__(self, word, origin, target):
        self.origin = word
        self.target, self.pronounciation = self.get_word_data(word) 
        self.image_url = self.get_image(self.target)
        self.lang = f"{origin}-{target}"

    # String representation of the object for debugging
    def __str__(self):
        return f"Card: {self.origin} -> {self.target} [{self.pronounciation}] ({self.image_url}))"

    # TODO: Currently only supports Spanish
    @staticmethod
    def get_word_data(word):
        url = 'https://www.dictionaryapi.com/api/v3/references/spanish/json/{}'
        params = {'key': 'abd3154d-1e08-4d44-b220-b4f2bc6a7a6b'}
        response = requests.get(url.format(word), params=params)
        translation = response.json()[0]['shortdef'][0]
        audio_code = response.json()[0]['hwi']['prs'][0]['sound']['audio']
        subfolder = re.match(r"^(bix|gg|[^a-zA-Z]+|.)", audio_code).group(1)
        pronounciation = f"https://media.merriam-webster.com/audio/prons/es/me/mp3/{subfolder}/{audio_code}.mp3"
        return translation, pronounciation
    
    @staticmethod
    def get_image(word):
        _search_params = {
            'q': word, 'num':1, 'safe': 'high',
            'fileType': 'jpg|png', 'imgType': 'photo',
            'rights': 'cc_publicdomain,cc_noncommercial',
        }
        # Get the url of the image from the first result
        GIS.search(search_params=_search_params)
        return GIS.results()[0].url


if __name__ == '__main__':
    print(Card('aburrido', 'es', 'en'))
    print(Card('comer', 'es', 'en'))
