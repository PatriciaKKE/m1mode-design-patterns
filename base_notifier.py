from notifier_interface import INotifier
from config_singleton import NotificationConfig

class BaseNotifier(INotifier):
    def __init__(self):
        self.config = NotificationConfig()
    
    def validate(self, recipient: str, message: str) -> bool:
        return bool(recipient and message)