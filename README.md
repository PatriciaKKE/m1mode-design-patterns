# 03 - Pattern Factory Method 🟡

> **ÉTAPE 2** : Éliminer les if/elif avec Factory Method

## 🎯 Objectif

Remplacer le **if/elif géant** de `send_notification()` par une **Factory** qui crée le bon type de notifier.

## 📝 Le Problème dans le Code Legacy

```python
# ❌ AVANT : if/elif géant - viole Open/Closed Principle
def send_notification(self, recipient, message, channel):
    if channel == "email":
        # ... 20 lignes de code email
    elif channel == "sms":
        # ... 20 lignes de code SMS
    elif channel == "push":
        # ... 20 lignes de code push
    # Ajouter un canal = modifier cette méthode !
```

## ✅ La Solution : Factory Method

```python
# ✅ APRÈS : Factory crée le bon notifier
notifier = NotifierFactory.create("email")
notifier.send(recipient, message)

# Ajouter un canal = créer une nouvelle classe (Open/Closed ✓)
```

## 📁 Fichiers à Créer

### 1. `notifier_interface.py` - Interface commune

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    """Interface pour tous les types de notification"""

    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Envoie une notification"""
        pass

    @abstractmethod
    def get_channel_name(self) -> str:
        """Retourne le nom du canal"""
        pass
```

### 2. `notifiers.py` - Implémentations concrètes

```python
from notifier_interface import Notifier

class EmailNotifier(Notifier):
    def send(self, recipient: str, message: str) -> bool:
        # Logique email
        pass

    def get_channel_name(self) -> str:
        return "email"

class SMSNotifier(Notifier):
    # TODO: Implémenter

class PushNotifier(Notifier):
    # TODO: Implémenter
```

### 3. `notifier_factory.py` - La Factory

```python
from notifiers import EmailNotifier, SMSNotifier, PushNotifier

class NotifierFactory:
    """Factory pour créer des notifiers"""

    _notifiers = {
        "email": EmailNotifier,
        "sms": SMSNotifier,
        "push": PushNotifier,
    }

    @classmethod
    def create(cls, channel: str) -> Notifier:
        """Crée et retourne le notifier approprié"""
        # TODO: Implémenter
        pass

    @classmethod
    def register(cls, channel: str, notifier_class):
        """Enregistre un nouveau type de notifier"""
        # Permet d'ajouter des canaux sans modifier la Factory !
        pass
```

## ✅ Critères de Validation

1. **Plus de if/elif** dans le code principal :
```python
# Ce code doit fonctionner sans if/elif
notifier = NotifierFactory.create(channel)
notifier.send(recipient, message)
```

2. **Ajout d'un canal sans modifier le code existant** :
```python
# Créer WhatsAppNotifier
class WhatsAppNotifier(Notifier):
    # ...

# L'enregistrer
NotifierFactory.register("whatsapp", WhatsAppNotifier)

# L'utiliser
notifier = NotifierFactory.create("whatsapp")
```

3. **Score Pylint** : > 7/10 pour chaque fichier

4. **Diagramme UML** : Interface + 3+ classes concrètes + Factory

## 📊 Commandes de Validation

```bash
# Tests
pytest tests/test_03_factory.py -v

# Pylint
pylint notifier_interface.py notifiers.py notifier_factory.py

# UML
pyreverse -o png -p Factory .
```

## 💡 Indices

<details>
<summary>Indice 1 : Le dictionnaire comme registre</summary>

Le dictionnaire `_notifiers` mappe des strings vers des **classes** (pas des instances).
Pour créer une instance, il faut appeler la classe : `ma_classe()`.

Utilisez `dict.get(key)` pour récupérer une classe, et pensez à gérer le cas où la clé n'existe pas.
</details>

<details>
<summary>Indice 2 : La méthode `register`</summary>

Pour permettre l'ajout dynamique de nouveaux types, il suffit d'ajouter une entrée au dictionnaire :
```python
cls._notifiers[channel] = notifier_class
```
</details>

<details>
<summary>Indice 3 : Injection de dépendances</summary>

Les notifiers peuvent recevoir la Config (Singleton) dans leur constructeur pour accéder aux paramètres de connexion (host, port, API keys...).
</details>

## ➡️ Prochaine Étape

Une fois la Factory validée, passez à **04-strategy-observer** pour les patterns comportementaux.
