from abc import ABC, abstractmethod

class BaseTool(ABC):
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, args: dict) -> str:
        pass

    @abstractmethod
    def get_declaration(self) -> dict:
        pass