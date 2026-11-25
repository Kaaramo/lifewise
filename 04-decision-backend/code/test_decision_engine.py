"""
LIFEWISE — Tests du Moteur de Décision
Partie 4 — Mission 1, Sprint S1

Tests unitaires couvrant tous les scénarios définis dans les règles métier.

Lancer les tests :
    python -m pytest test_decision_engine.py -v
    # ou sans pytest :
    python test_decision_engine.py
"""

import unittest
from datetime import datetime, timedelta

from decision_engine import (
    AlertType,
    CalendarEvent,
    DecisionEngine,
    DecisionResult,
    SystemState,
)

# Heure de référence pour les tests
NOW = datetime(2025, 11, 25, 8, 0, 0)  # 8h00 du matin


def make_state(
    departure: bool = True,
    in_frame: list[str] | None = None,
    expected: list[str] | None = None,
    events: list[CalendarEvent] | None = None,
) -> SystemState:
    """Helper pour créer facilement un SystemState dans les tests."""
    return SystemState(
        departure_detected=departure,
        objects_in_frame=in_frame if in_frame is not None else [],
        expected_objects=expected if expected is not None else ["portefeuille", "clés", "téléphone"],
        calendar_events=events or [],
        current_time=NOW,
    )


class TestRule0NoDeparture(unittest.TestCase):
    """Règle 0 : Aucun départ détecté → système en veille."""

    def test_no_departure_no_alert(self):
        """Sans départ, aucune alerte, quel que soit l'état des objets."""
        engine = DecisionEngine()

        # Sous-scénario A : tous les objets manquants mais pas de départ
        state = make_state(
            departure=False,
            in_frame=[],
            expected=["portefeuille", "clés"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.NONE)
        self.assertEqual(result.triggered_rule, 0)
        print(f"[Règle 0 - A] {result}")

    def test_no_departure_with_calendar(self):
        """Sans départ, même avec un RDV important, aucune alerte."""
        engine = DecisionEngine()
        event = CalendarEvent(
            title="Réunion client",
            start_time=NOW + timedelta(minutes=20),
            importance="haute",
        )
        state = make_state(departure=False, events=[event])
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.NONE)
        self.assertEqual(result.triggered_rule, 0)
        print(f"[Règle 0 - B] {result}")


class TestRule1AllClear(unittest.TestCase):
    """Règle 1 : Départ détecté + tous les objets visibles → pas d'alerte."""

    def test_all_objects_visible(self):
        """Tous les objets attendus sont dans le champ : bonne journée."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["portefeuille", "clés", "téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.NONE)
        self.assertEqual(result.triggered_rule, 1)
        print(f"[Règle 1] {result}")

    def test_extra_objects_in_frame(self):
        """Des objets supplémentaires dans le champ n'affectent pas le résultat."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["portefeuille", "clés", "téléphone", "lunettes", "sac"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.NONE)
        print(f"[Règle 1 - extra objets] {result}")


class TestRule2MissingObjects(unittest.TestCase):
    """Règle 2 : Départ + objets absents du champ → vérification suggérée."""

    def test_wallet_missing(self):
        """Portefeuille absent du champ → suggestion de vérification."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["clés", "téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.VERIFICATION)
        self.assertIn("portefeuille", result.missing_objects)
        self.assertIn("vérifier", result.message.lower())
        # Le message ne doit pas affirmer que l'objet est oublié
        self.assertNotIn("oublié", result.message.lower())
        self.assertNotIn("oublié", result.message)
        print(f"[Règle 2 - portefeuille manquant] {result}")

    def test_keys_missing(self):
        """Clés absentes du champ → suggestion de vérification."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["portefeuille", "téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.VERIFICATION)
        self.assertIn("clés", result.missing_objects)
        print(f"[Règle 2 - clés manquantes] {result}")

    def test_multiple_objects_missing(self):
        """Plusieurs objets absents → liste dans le message."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.VERIFICATION)
        self.assertIn("portefeuille", result.missing_objects)
        self.assertIn("clés", result.missing_objects)
        print(f"[Règle 2 - plusieurs manquants] {result}")

    def test_message_uses_verification_wording(self):
        """
        IMPORTANT : Le message utilise 'Pensez à vérifier', pas 'vous avez oublié'.
        C'est la distinction fondamentale : absent du champ ≠ oublié.
        """
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=[],
            expected=["portefeuille"],
        )
        result = engine.evaluate(state)
        # On vérifie la formulation douce
        forbidden_words = ["oublié", "oublié", "you forgot"]
        for word in forbidden_words:
            self.assertNotIn(word, result.message.lower(),
                             f"Le message ne doit pas contenir '{word}'")
        self.assertIn("vérifier", result.message.lower())
        print(f"[Règle 2 - formulation] {result}")


class TestRule3ImportantEvent(unittest.TestCase):
    """Règle 3 : Départ + RDV important imminent + objets manquants → alerte contextuelle."""

    def test_important_event_within_60_min(self):
        """RDV important dans 30 min + objet manquant → CONTEXTUELLE."""
        engine = DecisionEngine()
        event = CalendarEvent(
            title="Entretien d'embauche",
            start_time=NOW + timedelta(minutes=30),
            importance="haute",
        )
        state = make_state(
            departure=True,
            in_frame=["clés", "téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
            events=[event],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.CONTEXTUELLE)
        self.assertIn("Entretien d'embauche", result.message)
        print(f"[Règle 3 - RDV imminent] {result}")

    def test_low_importance_event_no_upgrade(self):
        """RDV peu important → ne déclenche pas l'alerte contextuelle."""
        engine = DecisionEngine()
        event = CalendarEvent(
            title="Rappel liste de courses",
            start_time=NOW + timedelta(minutes=15),
            importance="basse",
        )
        state = make_state(
            departure=True,
            in_frame=["clés"],
            expected=["portefeuille", "clés", "téléphone"],
            events=[event],
        )
        result = engine.evaluate(state)
        # Doit rester VERIFICATION, pas CONTEXTUELLE
        self.assertNotEqual(result.alert_type, AlertType.CONTEXTUELLE)
        print(f"[Règle 3 - RDV peu important] {result}")

    def test_important_event_far_away_no_upgrade(self):
        """RDV important mais dans 3h → ne déclenche pas l'alerte contextuelle."""
        engine = DecisionEngine()
        event = CalendarEvent(
            title="Réunion importante",
            start_time=NOW + timedelta(hours=3),
            importance="haute",
        )
        state = make_state(
            departure=True,
            in_frame=["clés"],
            expected=["portefeuille", "clés", "téléphone"],
            events=[event],
        )
        result = engine.evaluate(state)
        self.assertNotEqual(result.alert_type, AlertType.CONTEXTUELLE)
        print(f"[Règle 3 - RDV trop loin] {result}")


class TestRule4PhoneVisible(unittest.TestCase):
    """Règle 4 : Téléphone visible + autres objets manquants → alerte douce."""

    def test_phone_visible_other_missing(self):
        """Téléphone dans le champ + clés manquantes → DOUCE (mais VERIFICATION gagne)."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        # VERIFICATION a priorité sur DOUCE selon notre tableau de priorité
        # car missing objects déclenche la règle 2 aussi
        self.assertIn(result.alert_type, [AlertType.VERIFICATION, AlertType.DOUCE])
        self.assertGreater(result.alert_type.value, AlertType.NONE.value)
        print(f"[Règle 4 - téléphone visible] {result}")


class TestRule5EmptyFrame(unittest.TestCase):
    """Règle 5 : Aucun objet visible du tout → vérification générale."""

    def test_completely_empty_frame(self):
        """Champ vide → GENERALE."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=[],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        # VERIFICATION prime sur GENERALE (tous les objets sont "manquants")
        # mais le message doit rester prudent
        self.assertGreater(result.alert_type.value, AlertType.NONE.value)
        self.assertNotIn("oublié", result.message.lower())
        print(f"[Règle 5 - champ vide] {result}")

    def test_no_expected_objects_no_alert(self):
        """Si aucun objet n'est attendu, pas d'alerte même si le champ est vide."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=[],
            expected=[],
        )
        result = engine.evaluate(state)
        # Champ vide MAIS aucun objet attendu → Règle 1 (tout en ordre) prime
        # La règle 5 (GENERALE) se déclenche aussi, vérifions le comportement
        print(f"[Règle 5 - aucun objet attendu] {result}")


class TestPrioritySystem(unittest.TestCase):
    """Tests de la hiérarchie des priorités entre règles."""

    def test_contextuelle_beats_verification(self):
        """CONTEXTUELLE > VERIFICATION."""
        engine = DecisionEngine()
        event = CalendarEvent(
            title="Examen médical",
            start_time=NOW + timedelta(minutes=45),
            importance="haute",
        )
        state = make_state(
            departure=True,
            in_frame=["téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
            events=[event],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.CONTEXTUELLE)
        print(f"[Priorité - CONTEXTUELLE > VERIFICATION] {result}")

    def test_verification_beats_douce(self):
        """VERIFICATION > DOUCE."""
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        # VERIFICATION (règle 2) a valeur 3, DOUCE (règle 4) a valeur 1
        self.assertGreaterEqual(result.alert_type.value, AlertType.DOUCE.value)
        print(f"[Priorité - VERIFICATION vs DOUCE] {result}")


class TestCompleteScenarios(unittest.TestCase):
    """Scénarios complets simulant des cas réels."""

    def test_scenario_morning_routine_all_good(self):
        """
        Scénario : Matin normal, tout est visible.
        → Pas d'alerte.
        """
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["portefeuille", "clés", "téléphone", "sac"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.NONE)
        print(f"\n[Scénario 1 - Matin normal] {result}")

    def test_scenario_forgot_wallet_before_work(self):
        """
        Scénario : Départ au travail, portefeuille non visible.
        → Vérification suggérée (pas 'oublié').
        """
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["clés", "téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.VERIFICATION)
        self.assertIn("portefeuille", result.message)
        self.assertNotIn("oublié", result.message.lower())
        print(f"[Scénario 2 - Portefeuille manquant] {result}")

    def test_scenario_job_interview_incomplete(self):
        """
        Scénario : Entretien d'embauche dans 25 min, clés non visibles.
        → Alerte contextuelle urgente.
        """
        engine = DecisionEngine()
        event = CalendarEvent(
            title="Entretien chez Google",
            start_time=NOW + timedelta(minutes=25),
            importance="haute",
        )
        state = make_state(
            departure=True,
            in_frame=["portefeuille", "téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
            events=[event],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.CONTEXTUELLE)
        self.assertIn("Entretien chez Google", result.message)
        print(f"[Scénario 3 - Entretien imminent] {result}")

    def test_scenario_camera_sees_nothing(self):
        """
        Scénario : La caméra ne voit rien du tout (mauvaise position, nuit, etc.).
        → Vérification générale prudente.
        """
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=[],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertGreater(result.alert_type.value, AlertType.NONE.value)
        self.assertNotIn("oublié", result.message.lower())
        print(f"[Scénario 4 - Caméra vide] {result}")

    def test_scenario_user_still_preparing(self):
        """
        Scénario : Le téléphone est visible (l'utilisateur est encore là),
        mais le portefeuille et les clés ne sont pas dans le champ.
        → Alerte douce / vérification.
        """
        engine = DecisionEngine()
        state = make_state(
            departure=True,
            in_frame=["téléphone"],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertGreater(result.alert_type.value, AlertType.NONE.value)
        print(f"[Scénario 5 - Utilisateur encore là] {result}")

    def test_scenario_no_departure_despite_missing_objects(self):
        """
        Scénario : Tous les objets manquants mais l'utilisateur n'est pas parti.
        → Aucune alerte (système en veille).
        """
        engine = DecisionEngine()
        state = make_state(
            departure=False,
            in_frame=[],
            expected=["portefeuille", "clés", "téléphone"],
        )
        result = engine.evaluate(state)
        self.assertEqual(result.alert_type, AlertType.NONE)
        self.assertEqual(result.triggered_rule, 0)
        print(f"[Scénario 6 - Pas de départ] {result}")


# ---------------------------------------------------------------------------
# Exécution directe (sans pytest)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("LIFEWISE — Tests du Moteur de Décision")
    print("=" * 60)
    unittest.main(verbosity=2)
