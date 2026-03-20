import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from memory import MemoryManager
from tool_registry import ToolRegistry

load_dotenv()

class Agent:

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY not set. Run: set GEMINI_API_KEY=AIzaSyCaYPWiqW7IU_JkxB3MTQNYHW9EpzT45-I"
            )

        self.client   = genai.Client(api_key=api_key)
        self.memory   = MemoryManager()
        self.registry = ToolRegistry()

        # Build tools config from registry
        declarations = self.registry.get_declarations()
        self.tools = [
            types.Tool(function_declarations=[
                types.FunctionDeclaration(
                    name=d["name"],
                    description=d["description"],
                    parameters=d["parameters"]
                )
                for d in declarations
            ])
        ]

        self.system_instruction = (
            "You are a helpful personal assistant. "
            "Use tools whenever they would give a better answer for "
            "weather, calculations, time, translation, or file reading. "
            "Always be concise and friendly."
        )

    def chat(self, user_input: str) -> str:
        self.memory.add_user_message(user_input)

        try:
            contents = self.memory.get_history()

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    tools=self.tools
                )
            )

            while True:
                part = response.candidates[0].content.parts[0]

                if hasattr(part, "function_call") and part.function_call:
                    tool_name = part.function_call.name
                    tool_args = dict(part.function_call.args)

                    print(f"\n  [Agent] Calling tool: '{tool_name}'")

                    tool_result = self.registry.execute(tool_name, tool_args)

                    print(f"  [Agent] Tool result: {tool_result}\n")

                    self.memory.add_model_message(f"[Tool: {tool_name}] {tool_result}")

                    # Send tool result back to Gemini
                    function_response_content = {
                        "role": "user",
                        "parts": [{
                            "function_response": {
                                "name": tool_name,
                                "response": {"result": tool_result}
                            }
                        }]
                    }

                    response = self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=contents + [function_response_content],
                        config=types.GenerateContentConfig(
                            system_instruction=self.system_instruction,
                            tools=self.tools
                        )
                    )

                else:
                    final_text = part.text
                    self.memory.add_model_message(final_text)
                    return final_text

        except Exception as e:
            error_msg = f"Agent error: {str(e)}"
            self.memory.add_model_message(error_msg)
            return error_msg