"""
Factory Method complète avec intégration EmailNotifier.
Version finale pour le TP.
"""

from enum import Enum
from typing import Dict, Type
import sys

# Chemins d'import
sys.path.append('..')
sys.path.append('../02-singleton')

# Imports de base
from notifier_interface import INotifier
from console_notifier import ConsoleNotifier

# Import conditionnel d'EmailNotifier
try:
    from email_notifier import EmailNotifier
    EMAIL_NOTIFIER_AVAILABLE = True
    print("✅ EmailNotifier importé avec succès")
except ImportError as e:
    print(f"⚠️ EmailNotifier non disponible: {e}")
    EMAIL_NOTIFIER_AVAILABLE = False
    
    # Classe stub pour permettre l'exécution
    class EmailNotifier(INotifier):
        def get_channel_name(self):
            return "email"
        def send(self, recipient, message, **kwargs):
            print(f"[EMAIL STUB] À {recipient}: {message[:50]}...")
            return True
        def validate(self, recipient, message):
            return True, ""


class ChannelType(Enum):
    """Types de canaux disponibles."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SLACK = "slack"
    CONSOLE = "console"


class NotificationFactory:
    """
    Factory avec registre - Pattern Factory Method.
    Permet d'ajouter de nouveaux canaux sans modifier le code existant.
    """
    
    _registry: Dict[ChannelType, Type[INotifier]] = {}
    
    @classmethod
    def register(cls, channel_type: ChannelType, notifier_class: Type[INotifier]):
        """Enregistre un nouveau type de notifier."""
        cls._registry[channel_type] = notifier_class
        print(f"📝 {channel_type.value} -> {notifier_class.__name__}")
    
    @classmethod
    def create(cls, channel_type: ChannelType) -> INotifier:
        """
        Crée une instance de notifier.
        
        Args:
            channel_type: Type de canal (EMAIL, SMS, etc.)
            
        Returns:
            Instance du notifier correspondant
            
        Raises:
            ValueError: Si le canal n'est pas enregistré
        """
        if channel_type not in cls._registry:
            available = [c.value for c in cls._registry.keys()]
            error_msg = (
                f"🚫 Erreur: Canal '{channel_type.value}' non disponible.\n"
                f"   Canaux disponibles: {available}\n"
                f"   Pour ajouter un canal: NotificationFactory.register(ChannelType.NOUVEAU, NouveauNotifier)"
            )
            raise ValueError(error_msg)
        
        notifier_class = cls._registry[channel_type]
        return notifier_class()
    
    @classmethod
    def available_channels(cls):
        """Retourne la liste des canaux disponibles."""
        return [c.value for c in cls._registry.keys()]
    
    @classmethod
    def print_registry(cls):
        """Affiche le registre complet."""
        print("\n📚 REGISTRE DE LA FACTORY:")
        print("-" * 40)
        for channel_type, notifier_class in cls._registry.items():
            print(f"   {channel_type.value:10} → {notifier_class.__name__}")
        print("-" * 40)


class SimpleNotificationFactory:
    """
    Factory simplifiée - Alternative plus simple.
    Utile pour les petits projets ou prototypes.
    """
    
    @staticmethod
    def create(channel_type: ChannelType) -> INotifier:
        """
        Crée un notifier (version simple).
        
        Args:
            channel_type: Type de canal
            
        Returns:
            Instance du notifier
        """
        if channel_type == ChannelType.CONSOLE:
            return ConsoleNotifier()
        elif channel_type == ChannelType.EMAIL:
            if EMAIL_NOTIFIER_AVAILABLE:
                return EmailNotifier()
            else:
                raise ValueError("EmailNotifier non disponible. Assurez-vous que email_notifier.py existe.")
        else:
            raise ValueError(f"🚫 Canal non supporté: {channel_type.value}")


def setup_factory():
    """
    Configure la factory avec tous les notifiers disponibles.
    Cette fonction suit le principe d'initialisation explicite.
    """
    print("\n🔧 Configuration de la Factory...")
    
    # Enregistrement des notifiers
    NotificationFactory.register(ChannelType.CONSOLE, ConsoleNotifier)
    
    if EMAIL_NOTIFIER_AVAILABLE:
        NotificationFactory.register(ChannelType.EMAIL, EmailNotifier)
    else:
        print("⚠️ EmailNotifier non enregistré (indisponible)")
    
    print("✅ Factory configurée avec succès!")


def demonstrate_legacy_vs_factory():
    """Montre la différence entre l'approche legacy et factory."""
    
    print("\n" + "=" * 70)
    print("🔄 COMPARAISON: LEGACY vs FACTORY")
    print("=" * 70)
    
    print("\nLEGACY APPROACH (mauvaise pratique):")
    print("-" * 40)
    legacy_code = '''
class NotificationService:
    def send_notification(self, recipient, message, channel):
        # CODE SMELL: if/elif géant
        if channel == "email":
            # 20+ lignes pour email...
            pass
        elif channel == "sms":
            # 15+ lignes pour sms...
            pass
        elif channel == "push":
            # 15+ lignes pour push...
            pass
        # Ajouter un canal = MODIFIER CETTE MÉTHODE
        # Risque de casser le code existant
    '''
    print(legacy_code)
    
    print("\nFACTORY APPROACH (bonne pratique):")
    print("-" * 40)
    factory_code = '''
# 1. Créer une nouvelle classe
class WhatsAppNotifier(INotifier):
    def send(self, recipient, message):
        # Implémentation spécifique à WhatsApp
        pass

# 2. L'enregistrer (UNE SEULE FOIS)
NotificationFactory.register(ChannelType.WHATSAPP, WhatsAppNotifier)

# 3. Utiliser
notifier = NotificationFactory.create(ChannelType.WHATSAPP)
notifier.send("+336...", "Hello!")
    '''
    print(factory_code)
    
    print("\n✅ AVANTAGES DE LA FACTORY:")
    print("   • Open/Closed Principle: Extension sans modification")
    print("   • Single Responsibility: Chaque classe fait une chose")
    print("   • Testabilité: Classes isolées, facile à mock")
    print("   • Maintenance: Ajout/suppression sans risque")


def demo_complete_factory():
    """Démonstration complète de la Factory en action."""
    
    print("\n" + "=" * 70)
    print("🏭 FACTORY METHOD - DÉMONSTRATION COMPLÈTE")
    print("=" * 70)
    
    # 1. Configuration initiale
    setup_factory()
    NotificationFactory.print_registry()
    
    # 2. Test ConsoleNotifier via Factory
    print("\n1. 🖥️ TEST CONSOLENOTIFIER")
    print("-" * 40)
    try:
        console_notifier = NotificationFactory.create(ChannelType.CONSOLE)
        print(f"   ✅ Créé: {console_notifier.get_channel_name()}")
        
        # Envoi d'une notification
        success = console_notifier.send(
            recipient="dev@techflow.com",
            message="Notification console de test"
        )
        print(f"   📤 Résultat: {'✅ Réussi' if success else '❌ Échec'}")
    except ValueError as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Test EmailNotifier via Factory
    print("\n2. 📧 TEST EMAILNOTIFIER")
    print("-" * 40)
    try:
        email_notifier = NotificationFactory.create(ChannelType.EMAIL)
        print(f"   ✅ Créé: {email_notifier.get_channel_name()}")
        
        # Envoi d'un email de test
        success = email_notifier.send(
            recipient="client@entreprise.com",
            message="""Cher client,

Nous vous confirmons la création de votre compte.
Vos identifiants vous seront envoyés séparément.

Cordialement,
L'équipe TechFlow""",
            priority="normal",
            subject="Création de compte"
        )
        print(f"   📤 Résultat: {'✅ Réussi' if success else '❌ Échec'}")
    except ValueError as e:
        print(f"   ❌ Erreur: {e}")
    
    # 4. Test Simple Factory
    print("\n3. ⚡ TEST SIMPLE FACTORY")
    print("-" * 40)
    try:
        simple_factory = SimpleNotificationFactory()
        email_notifier2 = simple_factory.create(ChannelType.EMAIL)
        print(f"   ✅ Créé via SimpleFactory: {email_notifier2.get_channel_name()}")
    except ValueError as e:
        print(f"   ❌ Erreur: {e}")
    
    # 5. Test d'erreur (canal non existant)
    print("\n4. 🧪 TEST D'ERREUR (canal SMS non implémenté)")
    print("-" * 40)
    try:
        NotificationFactory.create(ChannelType.SMS)
        print("   ❌ DEVRAIT ÉCHOUER!")
    except ValueError as e:
        print(f"   ✅ Erreur attendue:\n   {e}")
    
    # 6. Démonstration d'extensibilité
    print("\n5. 🚀 DÉMONSTRATION D'EXTENSIBILITÉ")
    print("-" * 40)
    print("   Pour ajouter un canal SMS:")
    print("   1. Créer SMSNotifier(INotifier)")
    print("   2. NotificationFactory.register(ChannelType.SMS, SMSNotifier)")
    print("   3. Utiliser: factory.create(ChannelType.SMS)")
    print("   → AUCUNE modification du code existant!")
    
    # 7. Comparaison avec legacy
    demonstrate_legacy_vs_factory()
    
    print("\n" + "=" * 70)
    print("✅ DÉMONSTRATION TERMINÉE - FACTORY OPÉRATIONNELLE")
    print("=" * 70)


def run_tests():
    """Exécute des tests automatisés sur la factory."""
    
    print("\n" + "=" * 70)
    print("🧪 TESTS AUTOMATISÉS")
    print("=" * 70)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Singleton de configuration
    print("\n1. Test Singleton Configuration:")
    try:
        from config_singleton import NotificationConfig
        config1 = NotificationConfig()
        config2 = NotificationConfig()
        assert config1 is config2, "Devrait être le même instance"
        print("   ✅ Singleton vérifié")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Échec: {e}")
    tests_total += 1
    
    # Test 2: Factory création
    print("\n2. Test Factory Création:")
    try:
        setup_factory()
        notifier = NotificationFactory.create(ChannelType.CONSOLE)
        assert notifier.get_channel_name() == "console"
        print("   ✅ Factory création vérifiée")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Échec: {e}")
    tests_total += 1
    
    # Test 3: Envoi de notification
    print("\n3. Test Envoi Notification:")
    try:
        notifier = NotificationFactory.create(ChannelType.CONSOLE)
        success = notifier.send("test@example.com", "Message test")
        assert success == True
        print("   ✅ Envoi vérifié")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Échec: {e}")
    tests_total += 1
    
    # Résumé
    print("\n" + "=" * 70)
    print(f"📊 RÉSULTAT DES TESTS: {tests_passed}/{tests_total} réussis")
    if tests_passed == tests_total:
        print("🎉 TOUS LES TESTS ONT RÉUSSI!")
    else:
        print(f"⚠️ {tests_total - tests_passed} test(s) ont échoué")
    print("=" * 70)


if __name__ == "__main__":
    print("🔧 INITIALISATION DU SYSTÈME DE NOTIFICATION")
    print("=" * 70)
    
    # Choix du mode
    print("\nSélectionnez le mode:")
    print("1. 🏭 Démonstration Factory")
    print("2. 🧪 Tests automatisés")
    print("3. 📊 Les deux")
    
    try:
        choice = input("\nVotre choix (1-3): ").strip()
        
        if choice == "1":
            demo_complete_factory()
        elif choice == "2":
            run_tests()
        elif choice == "3":
            demo_complete_factory()
            run_tests()
        else:
            print("Choix invalide, exécution de la démonstration par défaut...")
            demo_complete_factory()
            
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
    
    print("\n" + "=" * 70)
    print("🚀 TP DESIGN PATTERNS - FACTORY METHOD COMPLÉTÉ")
    print("=" * 70)

if __name__ == "__main__":
    demo_complete()