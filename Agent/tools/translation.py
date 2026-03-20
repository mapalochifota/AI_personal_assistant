import requests
from tools.base_tool import BaseTool

class TranslationTool(BaseTool):

    @property
    def name(self) -> str:
        return "translate_text"

    @property
    def description(self) -> str:
        return "Translates text from one language to another."

    def execute(self, args: dict) -> str:
        text        = args.get("text", "").strip()
        target_lang = args.get("target_language", "fr").strip()
        source_lang = args.get("source_language", "en").strip()

        if not text:
            return "Error: No text provided to translate."

        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q":        text,
                "langpair": f"{source_lang}|{target_lang}"
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()

            if data.get("responseStatus") == 200:
                translated = data["responseData"]["translatedText"]
                return (
                    f"Original  ({source_lang}): {text}\n"
                    f"Translated({target_lang}): {translated}"
                )
            else:
                return f"Translation failed: {data.get('responseDetails', 'Unknown error')}"

        except requests.exceptions.Timeout:
            return "Translation service timed out."
        except Exception as e:
            return f"Translation error: {str(e)}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to translate"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Target language code: fr French, es Spanish, de German, lv Latvian"
                    },
                    "source_language": {
                        "type": "string",
                        "description": "Source language code, default is en for English"
                    }
                },
                "required": ["text", "target_language"]
            }
        }