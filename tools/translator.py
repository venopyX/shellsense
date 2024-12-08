# tools/translator.py

from deep_translator import GoogleTranslator
from tools.base_tool import BaseTool

class TranslatorTool(BaseTool):
    """
    Translates a given text from a source language to a target language. 
    This tool allows users to easily convert text between different languages, 
    making it ideal for communication, localization, and content understanding across language barriers.
    Simply provide the source language, target language, and the text to be translated.
    """

    def invoke(self, input: dict) -> dict:
        from_lang = input.get("from_lang")
        to_lang = input.get("to_lang")
        text = input.get("text")

        if not from_lang or not to_lang or not text:
            return {"error": "Parameters 'from_lang', 'to_lang', and 'text' are required."}

        try:
            # Initialize Google Translator
            translator = GoogleTranslator(source=from_lang, target=to_lang)
            # Perform translation
            translated_text = translator.translate(text)

            return {
                "original_text": text,
                "translated_text": translated_text,
                "from_lang": from_lang,
                "to_lang": to_lang
            }

        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Returns the JSON schema for the translator tool's input parameters.
        """
        return {
            "type": "object",
            "properties": {
                "from_lang": {
                    "type": "string",
                    "description": "The language code of the source text (e.g., 'en' for English)."
                },
                "to_lang": {
                    "type": "string",
                    "description": "The language code to translate the text into (e.g., 'am' for Amharic, 'om' for Oromic, etc)."
                },
                "text": {
                    "type": "string",
                    "description": "The text to be translated."
                }
            },
            "required": ["from_lang", "to_lang", "text"]
        }
