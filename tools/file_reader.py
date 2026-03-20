import os
from tools.base_tool import BaseTool

class FileReaderTool(BaseTool):

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Reads and returns the contents of a local .txt file."

    def execute(self, args: dict) -> str:
        filename = args.get("filename", "").strip()

        if not filename:
            return "Error: No filename provided."

        if not filename.endswith(".txt"):
            return "Error: Only .txt files are supported."

        if os.path.sep in filename or ".." in filename:
            return "Error: Invalid filename."

        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                return f"The file '{filename}' is empty."

            return f"Contents of '{filename}':\n\n{content}"

        except FileNotFoundError:
            return f"File '{filename}' not found."
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The name of the .txt file to read e.g. notes.txt"
                    }
                },
                "required": ["filename"]
            }
        }