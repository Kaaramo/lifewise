"""
LIFEWISE — Moteur de Décision (Decision Engine)
Partie 4 — Mission 1, Sprint S1

Ce module implémente les règles métier permettant de déterminer
quand et quel type d'alerte envoyer à l'utilisateur.

PRINCIPE FONDAMENTAL :
    La caméra ne peut que constater l'ABSENCE VISUELLE d'un objet.
    Elle ne peut PAS affirmer qu'un objet est réellement oublié.
    Toutes les alertes sont des VÉRIFICATIONS SUGGÉRÉES.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums & Structures de données
# ---------------------------------------------------------------------------

class AlertType(Enum):
    """Types d'alertes possibles, par ordre de priorité croissante."""
    NONE = 0          # Pas d'alerte
    DOUCE = 1         # Vérification légère (téléphone visible)
    GENERALE = 2      # Vérification générale (champ vide)
    VERIFICATION = 3  # Vérification d'un objet spécifique manquant
    CONTEXTUELLE = 4  # Alerte liée à un rendez-vous important


@dataclass
class CalendarEvent:
    """Représente un événement du calendrier de l'utilisateur."""
    title: str
    start_time: datetime
    importance: str  # "basse", "normale", "haute"


@dataclass
class SystemState:
    """
    État du système fourni au moteur de décision.
    
    Attributes:
        departure_detected: True si un départ de l'utilisateur est détecté.
        objects_in_frame:   Liste des objets visibles dans le champ de la caméra.
        expected_objects:   Liste des objets que l'utilisateur doit normalement emporter.
        calendar_events:    Événements du calendrier pour la journée.
        current_time:       Heure actuelle (par défaut : maintenant).
    """
    departure_detected: bool
    objects_in_frame: list[str]
    expected_objects: list[str]
    calendar_events: list[CalendarEvent] = field(default_factory=list)
    current_time: datetime = field(default_factory=datetime.now)


@dataclass
class DecisionResult:
    """
    Résultat produit par le moteur de décision.
    
    Attributes:
        alert_type:      Type d'alerte à envoyer.
        message:         Message à afficher à l'utilisateur.
        missing_objects: Objets absents du champ de la caméra.
        triggered_rule:  Numéro de la règle qui a déclenché l'alerte.
    """
    alert_type: AlertType
    message: str
    missing_objects: list[str] = field(default_factory=list)
    triggered_rule: int = 0

    def __str__(self) -> str:
        return (
            f"[Règle {self.triggered_rule}] "
            f"{self.alert_type.name} — {self.message}"
        )


# ---------------------------------------------------------------------------
# Moteur de décision
# ---------------------------------------------------------------------------

class DecisionEngine:
    """
    Moteur de décision LIFEWISE.

    Évalue l'état du système selon les règles métier et retourne
    une décision d'alerte.

    Usage:
        engine = DecisionEngine()
        result = engine.evaluate(state)
        print(result)
    """

    # Délai en minutes avant un rendez-vous pour qu'il soit "imminent"
    IMMINENCE_THRESHOLD_MINUTES: int = 60

    def evaluate(self, state: SystemState) -> DecisionResult:
        """
        Point d'entrée principal. Évalue l'état et retourne une décision.

        Les règles sont évaluées dans l'ordre. En cas de conditions multiples,
        la priorité la plus haute (AlertType avec valeur plus grande) gagne.
        """
        # --- Règle 0 : Aucun départ détecté ---
        if not state.departure_detected:
            return self._rule_0_no_departure()

        missing = self._get_missing_objects(state)
        imminent_event = self._get_imminent_event(state)

        # Collecte toutes les décisions candidates et retourne la prioritaire
        candidates: list[DecisionResult] = []

        # --- Règle 3 : Rendez-vous important imminent ---
        if imminent_event and missing:
            candidates.append(self._rule_3_important_event(imminent_event, missing))

        # --- Règle 4 : Téléphone visible + objets manquants ---
        if "téléphone" in state.objects_in_frame and missing:
            candidates.append(self._rule_4_phone_visible(missing))

        # --- Règle 5 : Aucun objet visible du tout ---
        if not state.objects_in_frame:
            candidates.append(self._rule_5_empty_frame())

        # --- Règle 2 : Objets spécifiques manquants ---
        if missing:
            candidates.append(self._rule_2_missing_objects(missing))

        # --- Règle 1 : Tout est visible ---
        if not missing:
            candidates.append(self._rule_1_all_clear())

        # Priorité : on choisit l'alerte avec la valeur AlertType la plus haute
        if candidates:
            return max(candidates, key=lambda r: r.alert_type.value)

        # Fallback (ne devrait pas arriver)
        return self._rule_1_all_clear()

    # -----------------------------------------------------------------------
    # Règles individuelles
    # -----------------------------------------------------------------------

    def _rule_0_no_departure(self) -> DecisionResult:
        """Règle 0 : Pas de départ → système en veille."""
        return DecisionResult(
            alert_type=AlertType.NONE,
            message="Système en veille. Aucun départ détecté.",
            triggered_rule=0,
        )

    def _rule_1_all_clear(self) -> DecisionResult:
        """Règle 1 : Tous les objets attendus sont visibles."""
        return DecisionResult(
            alert_type=AlertType.NONE,
            message="Tout semble en ordre. Bonne journée !",
            triggered_rule=1,
        )

    def _rule_2_missing_objects(self, missing: list[str]) -> DecisionResult:
        """Règle 2 : Objets absents du champ de la caméra."""
        items = ", ".join(missing)
        if len(missing) == 1:
            message = f"Pensez à vérifier votre {missing[0]}."
        else:
            message = f"Pensez à vérifier : {items}."
        return DecisionResult(
            alert_type=AlertType.VERIFICATION,
            message=message,
            missing_objects=missing,
            triggered_rule=2,
        )

    def _rule_3_important_event(
        self,
        event: CalendarEvent,
        missing: list[str],
    ) -> DecisionResult:
        """Règle 3 : Rendez-vous important imminent + objets manquants."""
        now = datetime.now()
        minutes_left = int((event.start_time - now).total_seconds() / 60)
        items = ", ".join(missing) if missing else "vos affaires"
        message = (
            f"Vous avez « {event.title} » dans environ {minutes_left} minute(s). "
            f"Pensez à vérifier : {items}."
        )
        return DecisionResult(
            alert_type=AlertType.CONTEXTUELLE,
            message=message,
            missing_objects=missing,
            triggered_rule=3,
        )

    def _rule_4_phone_visible(self, missing: list[str]) -> DecisionResult:
        """Règle 4 : Téléphone visible → alerte douce sur les autres objets."""
        items = ", ".join(missing)
        message = (
            f"Avant de partir, pensez à vérifier : {items}."
        )
        return DecisionResult(
            alert_type=AlertType.DOUCE,
            message=message,
            missing_objects=missing,
            triggered_rule=4,
        )

    def _rule_5_empty_frame(self) -> DecisionResult:
        """Règle 5 : Aucun objet visible dans le champ de la caméra."""
        return DecisionResult(
            alert_type=AlertType.GENERALE,
            message="Pensez à vérifier vos affaires avant de partir.",
            triggered_rule=5,
        )

    # -----------------------------------------------------------------------
    # Méthodes utilitaires
    # -----------------------------------------------------------------------

    def _get_missing_objects(self, state: SystemState) -> list[str]:
        """
        Retourne les objets attendus qui ne sont PAS visibles dans le champ
        de la caméra.

        Note : Absent du champ ≠ oublié. L'objet peut être dans une poche ou
        hors champ.
        """
        return [
            obj for obj in state.expected_objects
            if obj not in state.objects_in_frame
        ]

    def _get_imminent_event(self, state: SystemState) -> Optional[CalendarEvent]:
        """
        Retourne le prochain événement important dans les
        IMMINENCE_THRESHOLD_MINUTES prochaines minutes, ou None.
        """
        threshold_seconds = self.IMMINENCE_THRESHOLD_MINUTES * 60
        for event in state.calendar_events:
            if event.importance != "haute":
                continue
            delta = (event.start_time - state.current_time).total_seconds()
            if 0 <= delta <= threshold_seconds:
                return event
        return None
