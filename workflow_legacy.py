"""
Gestion de Workflow RH TechFlow Solutions - VERSION LEGACY
==========================================================

⚠️  CE CODE FONCTIONNE MAIS EST VOLONTAIREMENT MAL ÉCRIT !
    Votre mission : le refactorer avec State Pattern et Command Pattern.

Analysez-le avec :
    pylint workflow_legacy.py

Code Smells présents :
- Switch/If Statement Smell (gestion d'états avec if/elif)
- Open/Closed Violation (ajouter un état = modifier partout)
- Pas de pattern State (états gérés par strings)
- Pas de pattern Command (pas d'historique, pas d'Undo)
- Couplage fort (pas d'Observer pour les notifications)
"""


class LeaveRequest:
    """
    Demande de congés - Gestion d'états avec if/elif géants.

    États possibles :
    - draft : Brouillon
    - submitted : Soumise
    - manager_review : En validation manager
    - hr_review : En validation RH
    - approved : Approuvée
    - rejected : Refusée
    - cancelled : Annulée

    ❌ Problèmes :
    - États gérés par strings (pas de typage)
    - Transitions validées par if/elif géant
    - Pas d'historique des changements
    - Pas de possibilité d'Undo
    - Notifications mélangées avec la logique métier
    """

    VALID_STATES = ["draft", "submitted", "manager_review", "hr_review",
                    "approved", "rejected", "cancelled"]

    def __init__(self, employee_id, start_date, end_date, leave_type, reason=""):
        self.id = id(self)  # Génération ID simple
        self.employee_id = employee_id
        self.start_date = start_date
        self.end_date = end_date
        self.leave_type = leave_type  # "CP", "RTT", "maladie", "sans_solde"
        self.reason = reason

        # ❌ État géré par string
        self.status = "draft"

        # ❌ Pas d'historique propre
        self.history = []
        self._log_change("Création", "draft")

        # ❌ Commentaires mélangés avec les données
        self.manager_comment = ""
        self.hr_comment = ""

    def _log_change(self, action, new_status):
        """❌ Logging basique sans structure"""
        from datetime import datetime
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "status": new_status
        })

    def _notify(self, message, recipients):
        """
        ❌ Notifications mélangées avec la logique métier
        ❌ Couplage fort - pas d'Observer pattern
        """
        print(f"📧 NOTIFICATION: {message}")
        print(f"   Destinataires: {recipients}")

    def submit(self):
        """
        Soumettre la demande.
        ❌ Validation d'état par if/elif
        """
        if self.status != "draft":
            print(f"❌ Impossible de soumettre: état actuel = {self.status}")
            return False

        # ❌ Validation métier mélangée
        if not self.start_date or not self.end_date:
            print("❌ Dates manquantes")
            return False

        self.status = "submitted"
        self._log_change("Soumission", "submitted")
        self._notify(
            f"Nouvelle demande de congés de l'employé {self.employee_id}",
            ["manager@techflow.com"]
        )
        print(f"✓ Demande {self.id} soumise")
        return True

    def start_manager_review(self):
        """❌ Encore un if/elif pour la transition"""
        if self.status != "submitted":
            print(f"❌ Impossible: état actuel = {self.status}")
            return False

        self.status = "manager_review"
        self._log_change("Début validation manager", "manager_review")
        print(f"✓ Demande {self.id} en cours de validation manager")
        return True

    def manager_approve(self, comment=""):
        """❌ Validation manager avec if/elif"""
        if self.status != "manager_review":
            print(f"❌ Impossible: état actuel = {self.status}")
            return False

        self.manager_comment = comment
        self.status = "hr_review"
        self._log_change("Approuvé par manager", "hr_review")
        self._notify(
            f"Demande {self.id} approuvée par manager, en attente RH",
            ["rh@techflow.com"]
        )
        print(f"✓ Demande {self.id} approuvée par manager → validation RH")
        return True

    def manager_reject(self, comment=""):
        """❌ Rejet manager avec if/elif"""
        if self.status != "manager_review":
            print(f"❌ Impossible: état actuel = {self.status}")
            return False

        self.manager_comment = comment
        self.status = "rejected"
        self._log_change(f"Refusé par manager: {comment}", "rejected")
        self._notify(
            f"Votre demande de congés a été refusée: {comment}",
            [f"employee_{self.employee_id}@techflow.com"]
        )
        print(f"✓ Demande {self.id} refusée par manager")
        return True

    def hr_approve(self, comment=""):
        """❌ Validation RH avec if/elif"""
        if self.status != "hr_review":
            print(f"❌ Impossible: état actuel = {self.status}")
            return False

        self.hr_comment = comment
        self.status = "approved"
        self._log_change("Approuvé par RH", "approved")
        self._notify(
            f"Votre demande de congés du {self.start_date} au {self.end_date} est approuvée !",
            [f"employee_{self.employee_id}@techflow.com", "manager@techflow.com"]
        )
        print(f"✓ Demande {self.id} APPROUVÉE")
        return True

    def hr_reject(self, comment=""):
        """❌ Rejet RH avec if/elif"""
        if self.status != "hr_review":
            print(f"❌ Impossible: état actuel = {self.status}")
            return False

        self.hr_comment = comment
        self.status = "rejected"
        self._log_change(f"Refusé par RH: {comment}", "rejected")
        self._notify(
            f"Votre demande de congés a été refusée par les RH: {comment}",
            [f"employee_{self.employee_id}@techflow.com"]
        )
        print(f"✓ Demande {self.id} refusée par RH")
        return True

    def cancel(self):
        """❌ Annulation avec if/elif complexe"""
        # ❌ Logique complexe de qui peut annuler quand
        if self.status in ["approved", "rejected", "cancelled"]:
            print(f"❌ Impossible d'annuler: état actuel = {self.status}")
            return False

        self.status = "cancelled"
        self._log_change("Annulée", "cancelled")
        self._notify(
            f"Demande de congés {self.id} annulée",
            ["manager@techflow.com", "rh@techflow.com"]
        )
        print(f"✓ Demande {self.id} annulée")
        return True

    def get_available_actions(self):
        """
        ❌ ÉNORME if/elif pour déterminer les actions possibles
        ❌ Doit être modifié à chaque nouvel état
        """
        if self.status == "draft":
            return ["submit", "cancel"]
        elif self.status == "submitted":
            return ["start_manager_review", "cancel"]
        elif self.status == "manager_review":
            return ["manager_approve", "manager_reject"]
        elif self.status == "hr_review":
            return ["hr_approve", "hr_reject"]
        elif self.status == "approved":
            return []  # État final
        elif self.status == "rejected":
            return []  # État final
        elif self.status == "cancelled":
            return []  # État final
        else:
            return []

    def __str__(self):
        return (f"LeaveRequest(id={self.id}, employee={self.employee_id}, "
                f"type={self.leave_type}, status={self.status}, "
                f"dates={self.start_date} → {self.end_date})")


class LeaveCalculator:
    """
    Calcul des jours de congés.
    ❌ Pas de Strategy Pattern - if/elif selon le type de calcul
    """

    def calculate_days(self, start_date, end_date, leave_type, employee_seniority):
        """
        ❌ ÉNORME if/elif pour les règles de calcul
        ❌ Impossible d'ajouter une nouvelle règle sans modifier
        """
        from datetime import datetime

        # Parse des dates (simplifié)
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        total_days = (end - start).days + 1

        # ❌ if/elif géant pour les règles métier
        if leave_type == "CP":
            # Congés payés : selon ancienneté
            if employee_seniority < 1:
                # Moins d'1 an : prorata
                available = 25 * (employee_seniority / 1)
            elif employee_seniority < 5:
                available = 25
            elif employee_seniority < 10:
                available = 27  # +2 jours
            else:
                available = 30  # +5 jours

            if total_days > available:
                print(f"⚠️ Demande {total_days}j mais seulement {available}j disponibles")

        elif leave_type == "RTT":
            # RTT : fixe selon contrat
            if employee_seniority < 1:
                available = 0
            else:
                available = 12

            if total_days > available:
                print(f"⚠️ Demande {total_days}j RTT mais seulement {available}j disponibles")

        elif leave_type == "maladie":
            # Maladie : pas de limite mais règles spéciales
            if total_days > 3:
                print("⚠️ Arrêt > 3 jours : justificatif médical obligatoire")
            available = 365  # Pas de limite technique

        elif leave_type == "sans_solde":
            # Sans solde : selon politique
            if employee_seniority < 2:
                available = 0
                print("❌ Sans solde non autorisé avant 2 ans d'ancienneté")
            else:
                available = 30

        else:
            print(f"❌ Type de congé inconnu: {leave_type}")
            available = 0

        return {
            "requested_days": total_days,
            "available_days": available,
            "is_valid": total_days <= available
        }


# ============================================================
# UTILISATION - Démonstration du workflow legacy
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DÉMONSTRATION DU WORKFLOW LEGACY TECHFLOW")
    print("=" * 60)

    # Création d'une demande
    print("\n--- Création demande ---")
    request = LeaveRequest(
        employee_id="EMP001",
        start_date="2024-12-20",
        end_date="2024-12-25",
        leave_type="CP",
        reason="Vacances de Noël"
    )
    print(request)

    # Calcul des jours
    print("\n--- Calcul des jours ---")
    calculator = LeaveCalculator()
    result = calculator.calculate_days(
        "2024-12-20", "2024-12-25", "CP", employee_seniority=3
    )
    print(f"Résultat calcul: {result}")

    # Workflow normal
    print("\n--- Workflow normal ---")
    print(f"Actions disponibles: {request.get_available_actions()}")

    request.submit()
    print(f"Actions disponibles: {request.get_available_actions()}")

    request.start_manager_review()
    print(f"Actions disponibles: {request.get_available_actions()}")

    request.manager_approve("Bon pour accord")
    print(f"Actions disponibles: {request.get_available_actions()}")

    request.hr_approve("Validé, bon congés !")
    print(f"Actions disponibles: {request.get_available_actions()}")

    # Historique
    print("\n--- Historique ---")
    for entry in request.history:
        print(f"  {entry['timestamp']}: {entry['action']} → {entry['status']}")

    # ❌ Test transition invalide
    print("\n--- Test transition invalide ---")
    request.submit()  # Devrait échouer car déjà approved

    print("\n" + "=" * 60)
    print("FIN DE LA DÉMONSTRATION")
    print("=" * 60)
    print("\n💡 Refactorez ce code avec:")
    print("   - State Pattern (pour les états)")
    print("   - Command Pattern (pour l'historique et Undo)")
    print("   - Observer Pattern (pour les notifications)")
    print("   - Strategy Pattern (pour les calculs)")
