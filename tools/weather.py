import requests
from tools.base_tool import BaseTool

class WeatherTool(BaseTool):

    @property
    def name(self) -> str:
        return "get_weather"

    @property
    def description(self) -> str:
        return "Gets the current weather for a given city."

    def execute(self, args: dict) -> str:
        city = args.get("city", "").strip()

        if not city:
            return "Error: No city provided."

        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response.text.strip()
            else:
                return f"Could not get weather for '{city}'."

        except requests.exceptions.Timeout:
            return "Weather service timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "No internet connection available."
        except Exception as e:
            return f"Weather error: {str(e)}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city e.g. London or Riga"
                    }
                },
                "required": ["city"]
            }
        }