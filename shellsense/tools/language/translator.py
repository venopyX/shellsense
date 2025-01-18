import logging
from typing import Dict, Any, List, Optional
from googletrans import Translator as GoogleTranslator, LANGUAGES
from shellsense.tools.base import BaseTool

logger = logging.getLogger(__name__)

class TranslatorTool(BaseTool):
    """
    A tool for translating text between languages using Google Translate.
    Supports auto-detection of source language and translation to multiple target languages.
    """

    def __init__(self):
        self.translator = GoogleTranslator()
        self.supported_languages = LANGUAGES

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Translate text between languages.

        Args:
            input_data (Dict[str, Any]): Input containing:
                - text (str): Text to translate
                - target_lang (str): Target language code (e.g., 'en', 'es')
                - source_lang (str, optional): Source language code (default: auto-detect)

        Returns:
            Dict[str, Any]: Translation results or error message

        Raises:
            ValueError: If text or target language is missing or invalid
            TranslationError: If translation fails
        """
        try:
            self.validate_input(input_data)
            
            text = input_data["text"]
            target_lang = input_data["target_lang"]
            source_lang = input_data.get("source_lang", "auto")
            
            logger.info(f"Translating text to {target_lang}")
            return self._translate_text(text, target_lang, source_lang)
            
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return {"error": f"Invalid input: {str(e)}"}
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return {"error": f"Translation failed: {str(e)}"}

    def _translate_text(self, text: str, target_lang: str, source_lang: str = "auto") -> Dict[str, Any]:
        """
        Perform the actual translation.

        Args:
            text (str): Text to translate
            target_lang (str): Target language code
            source_lang (str): Source language code

        Returns:
            Dict[str, Any]: Translation results
        """
        try:
            # Validate language codes
            if target_lang not in self.supported_languages:
                raise ValueError(f"Unsupported target language: {target_lang}")
            if source_lang != "auto" and source_lang not in self.supported_languages:
                raise ValueError(f"Unsupported source language: {source_lang}")

            # Perform translation
            translation = self.translator.translate(
                text,
                dest=target_lang,
                src=source_lang
            )
            
            logger.debug(f"Translation successful: {translation.text}")
            return {
                "translated_text": translation.text,
                "source_lang": translation.src,
                "target_lang": translation.dest,
                "confidence": translation.extra_data.get("confidence", None)
            }
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise

    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get a list of supported languages.

        Returns:
            Dict[str, str]: Dictionary of language codes and names
        """
        return self.supported_languages

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of a text.

        Args:
            text (str): Text to analyze

        Returns:
            Dict[str, Any]: Detected language info
        """
        try:
            detection = self.translator.detect(text)
            return {
                "language": detection.lang,
                "confidence": detection.confidence,
                "language_name": self.supported_languages.get(detection.lang, "Unknown")
            }
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return {"error": f"Language detection failed: {str(e)}"}

    def get_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the translator tool's input parameters.

        Returns:
            Dict[str, Any]: JSON schema for validation and documentation.

        Example:
            {
                "text": "Hello, world!",
                "target_lang": "es",
                "source_lang": "en"
            }
        """
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to translate"
                },
                "target_lang": {
                    "type": "string",
                    "description": "Target language code (e.g., 'en', 'es')",
                    "enum": list(self.supported_languages.keys())
                },
                "source_lang": {
                    "type": "string",
                    "description": "Source language code (default: auto-detect)",
                    "enum": ["auto"] + list(self.supported_languages.keys())
                }
            },
            "required": ["text", "target_lang"]
        }

    def validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate the input data.

        Args:
            input_data (Dict[str, Any]): Input data to validate

        Raises:
            ValueError: If input data is invalid
        """
        if not input_data.get("text"):
            raise ValueError("Text is required")
        if not input_data.get("target_lang"):
            raise ValueError("Target language is required")
