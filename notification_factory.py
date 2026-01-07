"""
Factory Method pour créer des notifiers.
Remplace le if/elif géant du code legacy.
"""

from enum import Enum
from typing import Dict, Type
import sys
import os

# CORRECTION : Deux points, pas trois
sys.path.append('..')  # Remonter d'un dossier
sys.path.append('../02-singleton')  # Aller dans singleton

try:
    from notifier_interface import INotifier
    from console_notifier import ConsoleNotifier
    print("✅ Imports depuis 02-singleton réussis")
except ImportError as e:
    print(f"⚠️ Erreur d'import: {e}")
    print("Création de classes minimales pour continuer...")
    
    # Définitions minimales
    class INotifier:
        def send(self, recipient, message):
            pass
        def get_channel_name(self):
            pass
    
    class ConsoleNotifier(INotifier):
        def get_channel_name(self):
            return "console"
        def send(self, recipient, message):
            print(f"[CONSOLE] À {recipient}: {message}")
            return True


class ChannelType(Enum):
    """Types de canaux disponibles."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SLACK = "slack"
    CONSOLE = "console"


class NotificationFactory:
    """
    Factory pour créer des instances de notifiers.
    """
    
    _registry: Dict[ChannelType, Type[INotifier]] = {}
    
    @classmethod
    def register(cls, channel_type: ChannelType, notifier_class: Type[INotifier]):
        """Enregistre un nouveau type de notifier."""
        cls._registry[channel_type] = notifier_class
        print(f"✅ Enregistré: {channel_type.value} -> {notifier_class.__name__}")
    
    @classmethod
    def create(cls, channel_type: ChannelType) -> INotifier:
        """Crée une instance de notifier."""
        if channel_type not in cls._registry:
            available = [c.value for c in cls._registry.keys()]
            raise ValueError(
                f"Canal '{channel_type.value}' non supporté. "
                f"Canaux disponibles: {available}"
            )
        
        return cls._registry[channel_type]()
    
    @classmethod
    def get_available_channels(cls):
        """Retourne les canaux disponibles."""
        return [c.value for c in cls._registry.keys()]


class SimpleNotificationFactory:
    """Factory simple."""
    
    @staticmethod
    def create_notifier(channel_type: ChannelType) -> INotifier:
        if channel_type == ChannelType.CONSOLE:
            return ConsoleNotifier()
        else:
            raise ValueError(f"Canal non implémenté: {channel_type.value}")


def setup_factory():
    """Configure la factory."""
    NotificationFactory.register(ChannelType.CONSOLE, ConsoleNotifier)
    print("✅ Factory configurée avec ConsoleNotifier")


# Test
if __name__ == "__main__":
    print("🧪 TEST FACTORY")
    print("=" * 50)
    
    # Test simple factory
    print("\n1. Test Simple Factory:")
    factory = SimpleNotificationFactory()
    
    try:
        notifier = factory.create_notifier(ChannelType.CONSOLE)
        print(f"   ✅ Notifier créé: {notifier.get_channel_name()}")
        
        # Test envoi
        success = notifier.send("test@example.com", "Test factory")
        print(f"   📤 Envoi: {'✅ Réussi' if success else '❌ Échec'}")
        
    except ValueError as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test factory avec registre
    print("\n2. Test Factory avec registre:")
    setup_factory()
    
    try:
        notifier2 = NotificationFactory.create(ChannelType.CONSOLE)
        print(f"   ✅ Notifier depuis registre: {type(notifier2).__name__}")
    except ValueError as e:
        print(f"   ❌ Erreur: {e}")
    
    print(f"\n3. Canaux disponibles: {NotificationFactory.get_available_channels()}")