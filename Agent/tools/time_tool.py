from datetime import datetime
from tools.base_tool import BaseTool

class TimeTool(BaseTool):

    @property
    def name(self) -> str:
        return "get_current_time"

    @property
    def description(self) -> str:
        return "Returns the current date and time."

    def execute(self, args: dict) -> str:
        now = datetime.now()
        return now.strftime("Current date: %A, %d %B %Y | Time: %H:%M:%S")

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }