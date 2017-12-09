from apiclient.discovery import build
from html2text import HTML2Text

API_KEY = "INSERT_YOUR_API_KEY"
VERSION = "v2"
SERVICE = "translate"

class Translate:
    
    def __init__(self):
        services = build(SERVICE, VERSION, developerKey=API_KEY)
        self.translator = services.translations()
        self.cleaner = HTML2Text()

    def translate(self, query, target_lang="en"):
        """
        Call the Google Translate API to translate the given sentence to English
        """

        try:
            # set the query text and target language
            request = self.translator.list(
                q=query,
                target=target_lang
            )

            # response object from google api
            obj = request.execute()
            translated_text = obj["translations"][0]["translatedText"]

            # remove HTML tags
            translated_text = self.cleaner.handle(translated_text).replace("\n", " ")

        except:
            raise ValueError("Invalid input")

        return translated_text