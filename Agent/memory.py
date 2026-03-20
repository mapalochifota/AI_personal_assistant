class MemoryManager:

    def __init__(self):
        self._history: list[dict] = []

    def add_user_message(self, text: str):
        self._history.append({"role": "user", "parts": [{"text": text}]})

    def add_model_message(self, text: str):
        self._history.append({"role": "model", "parts": [{"text": text}]})

    def get_history(self) -> list:
        return self._history

    def clear(self):
        self._history = []

    def summary(self) -> str:
        return f"[Memory] {len(self._history)} turns in conversation history."