from notifier_interface import INotifier

class ConsoleNotifier(INotifier):
    def get_channel_name(self):
        return "console"
    
    def send(self, recipient, message):
        print(f"[CONSOLE] À {recipient}: {message}")
        return True