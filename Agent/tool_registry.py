from tools.base_tool import BaseTool
from tools.calculator import CalculatorTool
from tools.weather import WeatherTool
from tools.time_tool import TimeTool
from tools.translation import TranslationTool
from tools.file_reader import FileReaderTool

class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        self._register_all()

    def _register_all(self):
        tools = [
            CalculatorTool(),
            WeatherTool(),
            TimeTool(),
            TranslationTool(),
            FileReaderTool(),
        ]
        for tool in tools:
            self._tools[tool.name] = tool
            print(f"  [Registry] Registered tool: '{tool.name}'")

    def execute(self, tool_name: str, args: dict) -> str:
        if tool_name not in self._tools:
            return f"Error: Unknown tool '{tool_name}'."

        try:
            return self._tools[tool_name].execute(args)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"

    def get_declarations(self) -> list:
        return [tool.get_declaration() for tool in self._tools.values()]