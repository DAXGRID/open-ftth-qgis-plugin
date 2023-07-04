import os
import json


class Translation:
    def __init__(self):
        file_name = os.path.dirname(__file__) + '/translations.json'
        with open(file_name, 'r') as file:
            self.translations = json.loads(file.read())

    def translate(self, text):
        translation = self.translations["DK"].get(text, None);
        if translation is None:
            # Get a default error message in case it has not been translated.
            translation = self.translations["DK"]["DEFAULT_ERROR"]

        return translation
