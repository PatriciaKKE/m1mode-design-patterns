"""
EmailNotifier - Envoi de notifications par email.
Implémentation concrète de INotifier.
"""

import sys
sys.path.append('..')
sys.path.append('../02-singleton')

from notifier_interface import INotifier
from config_singleton import NotificationConfig


class EmailNotifier(INotifier):
    """Notifier pour les emails."""
    
    def __init__(self):
        self.config = NotificationConfig()
        self.email_config = self.config.get_email_config()
    
    def get_channel_name(self) -> str:
        return "email"
    
    def validate(self, recipient: str, message: str) -> tuple[bool, str]:
        """Validation spécifique aux emails."""
        # Validation basique
        if not recipient or not recipient.strip():
            return False, "❌ Le destinataire est vide"
        
        if not message or not message.strip():
            return False, "❌ Le message est vide"
        
        # Validation du format email
        if "@" not in recipient or "." not in recipient:
            return False, f"❌ Format d'email invalide: '{recipient}'"
        
        return True, "✅ Validation réussie"
    
    def send(self, recipient: str, message: str, **kwargs) -> bool:
        """
        Envoie un email.
        
        Args:
            recipient: Adresse email du destinataire
            message: Contenu du message
            **kwargs: Options supplémentaires
                - priority: 'low', 'normal', 'high', 'urgent'
                - subject: Sujet personnalisé
                - attachments: Liste de fichiers joints
        
        Returns:
            bool: True si l'envoi a réussi
        """
        # Validation
        is_valid, error_message = self.validate(recipient, message)
        if not is_valid:
            print(error_message)
            return False
        
        # Récupération des options
        priority = kwargs.get('priority', 'normal')
        subject = kwargs.get('subject', message[:50] + "...")
        attachments = kwargs.get('attachments', [])
        
        # Formatage selon la priorité
        if priority == 'urgent':
            subject = f"🚨 URGENT: {subject}"
            priority_indicator = "🔴"
        elif priority == 'high':
            subject = f"⚠️ IMPORTANT: {subject}"
            priority_indicator = "🟡"
        elif priority == 'low':
            subject = f"📎 NOTE: {subject}"
            priority_indicator = "🟢"
        else:
            priority_indicator = "🔵"
        
        # Simulation d'envoi d'email
        print("\n" + "=" * 60)
        print("📧 EMAIL NOTIFICATION")
        print("=" * 60)
        print(f"{priority_indicator} Priorité: {priority}")
        print(f"📨 De: notifications@{self.email_config['host']}")
        print(f"📬 À: {recipient}")
        print(f"🏢 Serveur SMTP: {self.email_config['host']}:{self.email_config['port']}")
        print(f"📝 Sujet: {subject}")
        print(f"📄 Pièces jointes: {len(attachments)} fichier(s)")
        print("-" * 60)
        print(f"📋 Message:")
        print(f"{message}")
        print("=" * 60)
        print("✅ Email envoyé avec succès (simulation)")
        print("=" * 60 + "\n")
        
        return True
    
    def format_message(self, message: str, **kwargs) -> str:
        """Formate le message pour l'email."""
        signature = kwargs.get('signature', "\n\n--\nTechFlow Notifications")
        max_length = kwargs.get('max_length', 1000)
        
        # Tronquer si nécessaire
        if len(message) > max_length:
            message = message[:max_length] + "... [message tronqué]"
        
        return message + signature


# Tests unitaires
if __name__ == "__main__":
    print("🧪 TEST EMAIL NOTIFIER")
    print("=" * 60)
    
    # Création du notifier
    notifier = EmailNotifier()
    print(f"✅ Notifier créé: {notifier.get_channel_name()}")
    
    # Tests
    test_cases = [
        {
            "name": "Email normal",
            "recipient": "user@example.com",
            "message": "Bonjour,\n\nCeci est un email de test normal.\n\nCordialement.",
            "kwargs": {"priority": "normal", "subject": "Test Email"}
        },
        {
            "name": "Email urgent",
            "recipient": "admin@company.com",
            "message": "ALERTE CRITIQUE :\nLe serveur principal est hors ligne.\nIntervention immédiate requise.",
            "kwargs": {"priority": "urgent", "subject": "Alerte Serveur"}
        },
        {
            "name": "Email avec pièces jointes",
            "recipient": "hr@company.com",
            "message": "Veuillez trouver ci-joint le rapport mensuel.",
            "kwargs": {
                "priority": "high",
                "subject": "Rapport Mensuel",
                "attachments": ["rapport.pdf", "data.xlsx"]
            }
        },
        {
            "name": "Email invalide (format)",
            "recipient": "not-an-email",
            "message": "Ceci devrait échouer.",
            "kwargs": {}
        },
        {
            "name": "Destinataire vide",
            "recipient": "",
            "message": "Test",
            "kwargs": {}
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}:")
        print("-" * 40)
        
        success = notifier.send(
            recipient=test['recipient'],
            message=test['message'],
            **test['kwargs']
        )
        
        if success:
            print(f"   ✅ Succès")
        else:
            print(f"   ✅ Échec attendu")
    
    print("\n" + "=" * 60)
    print(f"📊 Résumé: EmailNotifier fonctionnel")
    print("=" * 60)