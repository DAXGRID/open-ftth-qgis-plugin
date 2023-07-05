from ..application_settings import ApplicationSettings
import os
import json


class Translation:
    def __init__(self):
        fallback_language = "EN"
        language = ApplicationSettings().get_translation_language()
        file_name = os.path.dirname(__file__) + '/translations.json'
        with open(file_name, 'r') as file:
            self.translations = json.loads(file.read()).get(language, fallback_language)

    def translate(self, text):
        translation = self.translations.get(text, None);
        if translation is None:
            # Get a default error message in case it has not been translated.
            translation = self.translations['DEFAULT_ERROR']

        return translation
