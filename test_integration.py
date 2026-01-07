from config_singleton import NotificationConfig
from console_notifier import ConsoleNotifier

def test_singleton():
    print("=== Test Singleton ===")
    config1 = NotificationConfig()
    config2 = NotificationConfig()
    
    if config1 is config2:
        print("✅ Singleton vérifié : même instance")
    else:
        print("❌ ERREUR : pas un Singleton")
        return False
    return True

def test_notifier():
    print("\n=== Test Notifier ===")
    notifier = ConsoleNotifier()
    
    # Test 1 : Envoi normal
    print("\nTest 1 - Notification normale :")
    success1 = notifier.send("test@example.com", "Bonjour !")
    print(f"Résultat : {'✅ Succès' if success1 else '❌ Échec'}")
    
    # Test 2 : Destinataire vide
    print("\nTest 2 - Destinataire vide :")
    success2 = notifier.send("", "Message sans destinataire")
    print(f"Résultat : {'✅ Échec attendu' if not success2 else '❌ DEVRAIT ÉCHOUER'}")
    
    # Test 3 : Message vide
    print("\nTest 3 - Message vide :")
    success3 = notifier.send("admin@example.com", "")
    print(f"Résultat : {'✅ Échec attendu' if not success3 else '❌ DEVRAIT ÉCHOUER'}")
    
    return success1 and not success2 and not success3

def test_channel_name():
    print("\n=== Test Channel Name ===")
    notifier = ConsoleNotifier()
    name = notifier.get_channel_name()
    print(f"Nom du canal : {name}")
    return name == "console"

if __name__ == "__main__":
    print("🧪 Début des tests d'intégration...\n")
    
    results = []
    
    results.append(test_singleton())
    results.append(test_notifier())
    results.append(test_channel_name())
    
    print("\n" + "="*50)
    if all(results):
        print("🎉 TOUS LES TESTS ONT RÉUSSI !")
    else:
        print("❌ Certains tests ont échoué")
    print("="*50)