from apiclient.discovery import build
from html2text import HTML2Text

API_KEY = "AIzaSyByE2b7ouR-io5CVLGAGNDjVYSfQs_Q74U"
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

# t = Translate()

# print (t.translate("两年前发生的制衣厂大楼坍塌事故造成逾千人死亡。孟加拉国警方日前正式以故意杀人罪指控涉案41人。这是制衣业历史上死亡人数最高的一场灾难。"))