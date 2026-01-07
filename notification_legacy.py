"""
Module de notification TechFlow Solutions - VERSION LEGACY
==========================================================

⚠️  CE CODE FONCTIONNE MAIS EST VOLONTAIREMENT MAL ÉCRIT !
    Votre mission : le refactorer avec les Design Patterns.

Analysez-le avec :
    pylint notification_legacy.py

Score attendu : ~3/10 (normal, c'est fait exprès !)

Code Smells présents :
- God Class (une classe fait tout)
- Switch/If Statement Smell (if/elif géant)
- Duplicate Code (validation répétée)
- Open/Closed Violation (modifier pour ajouter un canal)
- Configuration Smell (variables globales)
- Magic Strings ("email", "sms", "push")
"""

# ❌ Configuration dupliquée partout (pas de Singleton)
EMAIL_HOST = "smtp.techflow.com"
EMAIL_PORT = 587
EMAIL_USER = "notifications@techflow.com"
EMAIL_PASSWORD = "super_secret_password"  # ❌ Credentials en dur !

SMS_API_KEY = "sk_live_xxxxxxxxxxxxx"
SMS_API_URL = "https://api.sms-provider.com/send"

PUSH_API_KEY = "pk_xxxxxxxxxxxxx"
PUSH_API_URL = "https://api.push-provider.com/notify"

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/xxx/yyy/zzz"


class NotificationService:
    """
    Service de notification - TOUT est dans une seule classe !

    Problèmes :
    - God Class : trop de responsabilités
    - if/elif géant dans send_notification
    - Duplication de code (validation, logging)
    - Impossible à tester unitairement
    - Ajouter un canal = modifier cette classe
    """

    def __init__(self):
        # ❌ Configuration dupliquée depuis les variables globales
        self.email_host = EMAIL_HOST
        self.email_port = EMAIL_PORT
        self.email_user = EMAIL_USER
        self.email_password = EMAIL_PASSWORD
        self.sms_key = SMS_API_KEY
        self.sms_url = SMS_API_URL
        self.push_key = PUSH_API_KEY
        self.push_url = PUSH_API_URL
        self.slack_url = SLACK_WEBHOOK_URL

        # Compteurs (mélangés avec la logique métier)
        self.sent_count = 0
        self.failed_count = 0
        self.email_count = 0
        self.sms_count = 0
        self.push_count = 0
        self.slack_count = 0

    def send_notification(self, recipient, message, channel, priority="normal",
                          attachments=None, retry_count=3):
        """
        Envoie une notification via le canal spécifié.

        ❌ ÉNORME if/elif - viole Open/Closed Principle
        ❌ Chaque nouveau canal = modifier cette méthode
        ❌ Logique de chaque canal mélangée ici
        """
        # ❌ Validation dupliquée pour chaque appel
        if not recipient:
            print("ERREUR: Destinataire manquant")
            self.failed_count += 1
            return False

        if not message:
            print("ERREUR: Message manquant")
            self.failed_count += 1
            return False

        if len(message) > 5000:
            print("ERREUR: Message trop long (max 5000 caractères)")
            self.failed_count += 1
            return False

        # ❌ PROBLÈME MAJEUR : if/elif géant
        if channel == "email":
            return self._send_email(recipient, message, priority, attachments)

        elif channel == "sms":
            return self._send_sms(recipient, message, priority)

        elif channel == "push":
            return self._send_push(recipient, message, priority)

        elif channel == "slack":
            return self._send_slack(recipient, message, priority)

        elif channel == "teams":
            # ❌ Ajouté plus tard - le if/elif grandit...
            return self._send_teams(recipient, message, priority)

        elif channel == "whatsapp":
            # ❌ Encore un canal ajouté...
            return self._send_whatsapp(recipient, message, priority)

        else:
            # ❌ Si on se trompe de canal, erreur silencieuse
            print(f"ERREUR: Canal inconnu '{channel}'")
            self.failed_count += 1
            return False

    def _send_email(self, recipient, message, priority, attachments):
        """❌ Logique email mélangée dans la God Class"""
        try:
            # Construction du sujet selon priorité
            if priority == "urgent":
                subject = "[URGENT] " + message[:50]
            elif priority == "high":
                subject = "[IMPORTANT] " + message[:50]
            else:
                subject = message[:50]

            # ❌ Simulation connexion SMTP (en vrai, ça serait smtplib)
            print(f"📧 Connexion SMTP à {self.email_host}:{self.email_port}")
            print(f"📧 Authentification: {self.email_user}")
            print(f"📧 Envoi à: {recipient}")
            print(f"📧 Sujet: {subject}")
            print(f"📧 Corps: {message[:100]}...")

            if attachments:
                for att in attachments:
                    print(f"📧 Pièce jointe: {att}")

            self.sent_count += 1
            self.email_count += 1
            print("📧 Email envoyé avec succès ✓")
            return True

        except Exception as e:
            print(f"📧 ERREUR envoi email: {e}")
            self.failed_count += 1
            return False

    def _send_sms(self, recipient, message, priority):
        """❌ Logique SMS mélangée dans la God Class"""
        try:
            # ❌ Validation spécifique SMS dupliquée
            if not recipient.startswith("+"):
                print("⚠️ Numéro doit commencer par + (format international)")
                recipient = "+33" + recipient.lstrip("0")

            # ❌ Troncature message SMS
            if len(message) > 160:
                print(f"⚠️ Message tronqué (160 car. max pour SMS)")
                message = message[:157] + "..."

            # Ajout préfixe urgence
            if priority == "urgent":
                message = "🚨 URGENT: " + message

            print(f"📱 Appel API SMS: {self.sms_url}")
            print(f"📱 Clé API: {self.sms_key[:10]}...")
            print(f"📱 Destinataire: {recipient}")
            print(f"📱 Message: {message}")

            self.sent_count += 1
            self.sms_count += 1
            print("📱 SMS envoyé avec succès ✓")
            return True

        except Exception as e:
            print(f"📱 ERREUR envoi SMS: {e}")
            self.failed_count += 1
            return False

    def _send_push(self, recipient, message, priority):
        """❌ Logique Push mélangée dans la God Class"""
        try:
            # Construction payload
            payload = {
                "to": recipient,
                "title": "TechFlow Notification",
                "body": message,
                "priority": priority
            }

            if priority == "urgent":
                payload["sound"] = "alarm"
                payload["badge"] = 1

            print(f"🔔 Appel API Push: {self.push_url}")
            print(f"🔔 Clé API: {self.push_key[:10]}...")
            print(f"🔔 Payload: {payload}")

            self.sent_count += 1
            self.push_count += 1
            print("🔔 Push envoyé avec succès ✓")
            return True

        except Exception as e:
            print(f"🔔 ERREUR envoi Push: {e}")
            self.failed_count += 1
            return False

    def _send_slack(self, recipient, message, priority):
        """❌ Logique Slack mélangée dans la God Class"""
        try:
            # Construction message Slack
            if priority == "urgent":
                slack_message = f"🚨 *URGENT* 🚨\n{message}"
            elif priority == "high":
                slack_message = f"⚠️ *Important*\n{message}"
            else:
                slack_message = message

            print(f"💬 Envoi Slack webhook")
            print(f"💬 Canal/User: {recipient}")
            print(f"💬 Message: {slack_message}")

            self.sent_count += 1
            self.slack_count += 1
            print("💬 Slack envoyé avec succès ✓")
            return True

        except Exception as e:
            print(f"💬 ERREUR envoi Slack: {e}")
            self.failed_count += 1
            return False

    def _send_teams(self, recipient, message, priority):
        """❌ Ajouté plus tard - code dupliqué de Slack"""
        try:
            if priority == "urgent":
                teams_message = f"🚨 **URGENT** 🚨\n\n{message}"
            elif priority == "high":
                teams_message = f"⚠️ **Important**\n\n{message}"
            else:
                teams_message = message

            print(f"👥 Envoi Teams webhook")
            print(f"👥 Canal: {recipient}")
            print(f"👥 Message: {teams_message}")

            self.sent_count += 1
            print("👥 Teams envoyé avec succès ✓")
            return True

        except Exception as e:
            print(f"👥 ERREUR envoi Teams: {e}")
            self.failed_count += 1
            return False

    def _send_whatsapp(self, recipient, message, priority):
        """❌ Encore un canal ajouté - le code grandit..."""
        try:
            if not recipient.startswith("+"):
                recipient = "+33" + recipient.lstrip("0")

            if priority == "urgent":
                message = "🚨 " + message

            print(f"📲 Envoi WhatsApp")
            print(f"📲 Numéro: {recipient}")
            print(f"📲 Message: {message}")

            self.sent_count += 1
            print("📲 WhatsApp envoyé avec succès ✓")
            return True

        except Exception as e:
            print(f"📲 ERREUR envoi WhatsApp: {e}")
            self.failed_count += 1
            return False

    def send_bulk(self, recipients, message, channel, priority="normal"):
        """
        Envoi en masse.
        ❌ Logique dupliquée, pas de gestion d'erreurs propre
        """
        success = 0
        failed = 0

        for recipient in recipients:
            if self.send_notification(recipient, message, channel, priority):
                success += 1
            else:
                failed += 1

        print(f"\n📊 Résultat bulk: {success} succès, {failed} échecs")
        return {"success": success, "failed": failed}

    def send_multi_channel(self, recipient, message, channels, priority="normal"):
        """
        Envoi sur plusieurs canaux.
        ❌ Encore de la duplication
        """
        results = {}
        for channel in channels:
            results[channel] = self.send_notification(recipient, message, channel, priority)
        return results

    def get_stats(self):
        """Statistiques d'envoi"""
        return {
            "total_sent": self.sent_count,
            "total_failed": self.failed_count,
            "by_channel": {
                "email": self.email_count,
                "sms": self.sms_count,
                "push": self.push_count,
                "slack": self.slack_count
            }
        }

    def reset_stats(self):
        """Reset des compteurs"""
        self.sent_count = 0
        self.failed_count = 0
        self.email_count = 0
        self.sms_count = 0
        self.push_count = 0
        self.slack_count = 0


# ============================================================
# UTILISATION - Démonstration du code legacy
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DÉMONSTRATION DU CODE LEGACY TECHFLOW")
    print("=" * 60)

    # Création du service (God Class)
    service = NotificationService()

    # Test envoi email
    print("\n--- Test Email ---")
    service.send_notification(
        recipient="marie.dupont@techflow.com",
        message="Votre demande de congés a été approuvée pour la période du 20 au 25 décembre.",
        channel="email",
        priority="normal"
    )

    # Test envoi SMS
    print("\n--- Test SMS ---")
    service.send_notification(
        recipient="0612345678",
        message="Code de vérification TechFlow: 847291",
        channel="sms",
        priority="urgent"
    )

    # Test envoi Push
    print("\n--- Test Push ---")
    service.send_notification(
        recipient="user_token_abc123",
        message="Nouvelle demande de congés à valider",
        channel="push",
        priority="high"
    )

    # Test envoi Slack
    print("\n--- Test Slack ---")
    service.send_notification(
        recipient="#rh-notifications",
        message="Thomas Chen a soumis une demande de congés",
        channel="slack"
    )

    # ❌ Test canal avec typo - erreur silencieuse !
    print("\n--- Test Canal Invalide (typo) ---")
    service.send_notification(
        recipient="user@example.com",
        message="Test",
        channel="emal"  # ❌ Typo ! Pas d'erreur de compilation
    )

    # Statistiques
    print("\n--- Statistiques ---")
    stats = service.get_stats()
    print(f"Total envoyés: {stats['total_sent']}")
    print(f"Total échecs: {stats['total_failed']}")
    print(f"Par canal: {stats['by_channel']}")

    print("\n" + "=" * 60)
    print("FIN DE LA DÉMONSTRATION")
    print("=" * 60)
    print("\n💡 Maintenant, analysez ce code avec:")
    print("   pylint notification_legacy.py")
    print("   pyreverse -o png -p Legacy notification_legacy.py")
