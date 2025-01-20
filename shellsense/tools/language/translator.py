from deep_translator import GoogleTranslator

from shellsense.tools.base_tool import BaseTool


class TranslatorTool(BaseTool):
    """
    Translates text from a source language to a target language.

    Args (for `invoke` method):
        from_lang (str): Language code of the source text (e.g., 'en' for English).
        to_lang (str): Language code to translate into (e.g., 'am' for Amharic, 'om' for Oromic).
        text (str): The text to be translated.
    """

    def invoke(self, input: dict) -> dict:
        from_lang = input.get("from_lang")
        to_lang = input.get("to_lang")
        text = input.get("text")

        if not from_lang or not to_lang or not text:
            return {
                "error": "Parameters 'from_lang', 'to_lang', and 'text' are required."
            }

        try:
            translator = GoogleTranslator(source=from_lang, target=to_lang)
            translated_text = translator.translate(text)

            return {
                "original_text": text,
                "translated_text": translated_text,
                "from_lang": from_lang,
                "to_lang": to_lang,
            }

        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}

    def get_schema(self) -> dict:
        """
        Provides the input schema for the translator tool.

        Returns:
            dict: JSON schema specifying required parameters and their descriptions.
        """
        return {
            "type": "object",
            "properties": {
                "from_lang": {
                    "type": "string",
                    "description": "Language code of the source text (e.g., 'en' for English).",
                },
                "to_lang": {
                    "type": "string",
                    "description": "Language code to translate into (e.g., 'am' for Amharic, 'om' for Oromic).",
                },
                "text": {"type": "string", "description": "Text to be translated."},
            },
            "required": ["from_lang", "to_lang", "text"],
        }
