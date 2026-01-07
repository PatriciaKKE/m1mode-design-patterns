from abc import ABC, abstractmethod

class INotifier(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass
    
    @abstractmethod
    def get_channel_name(self) -> str:
        pass