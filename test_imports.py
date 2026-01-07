
import sys
import os

print("=" * 50)
print("🧪 TEST DES IMPORTS")
print("=" * 50)

# 1. Affiche le dossier courant
print(f"\n1. 📁 Dossier courant: {os.getcwd()}")

# 2. Ajoute les chemins pour les imports
print("\n2. 📍 Ajout des chemins d'import:")
sys.path.append('..')  # Remonter d'un dossier
sys.path.append('../02-singleton')  # Aller dans singleton

print(f"   - Chemin ajouté: '..'")
print(f"   - Chemin ajouté: '../02-singleton'")

# 3. Liste les fichiers dans 02-singleton
print("\n3. 📋 Fichiers dans 02-singleton:")
try:
    singleton_path = os.path.join('..', '02-singleton')
    if os.path.exists(singleton_path):
        files = os.listdir(singleton_path)
        for file in files:
            if file.endswith('.py'):
                print(f"   - {file}")
    else:
        print(f"   ❌ Dossier non trouvé: {singleton_path}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 4. Test des imports
print("\n4. 🚀 Test des imports:")

# Test INotifier
try:
    from notifier_interface import INotifier
    print("   ✅ INotifier importé avec succès")
except ImportError as e:
    print(f"   ❌ Erreur INotifier: {e}")

# Test ConsoleNotifier
try:
    from console_notifier import ConsoleNotifier
    print("   ✅ ConsoleNotifier importé avec succès")
except ImportError as e:
    print(f"   ❌ Erreur ConsoleNotifier: {e}")

# Test Config Singleton
try:
    from config_singleton import NotificationConfig
    print("   ✅ NotificationConfig importé avec succès")
except ImportError as e:
    print(f"   ❌ Erreur NotificationConfig: {e}")

# 5. Test d'instanciation
print("\n5. 🔧 Test d'instanciation:")

try:
    # Test Singleton
    config1 = NotificationConfig()
    config2 = NotificationConfig()
    is_singleton = config1 is config2
    print(f"   ✅ Singleton test: {is_singleton}")
except Exception as e:
    print(f"   ❌ Erreur Singleton: {e}")

try:
    # Test ConsoleNotifier
    notifier = ConsoleNotifier()
    channel_name = notifier.get_channel_name()
    print(f"   ✅ ConsoleNotifier créé: {channel_name}")
    
    # Test envoi
    success = notifier.send("test@import.com", "Test d'import")
    print(f"   ✅ Envoi test: {success}")
except Exception as e:
    print(f"   ❌ Erreur ConsoleNotifier: {e}")

print("\n" + "=" * 50)
print("✅ TEST TERMINÉ")
print("=" * 50)