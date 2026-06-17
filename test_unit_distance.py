"""Tests unitaires des fonctions du controleur (logique isolee).

Mise en miroir du test unitaire vu en cours : on simule la requete Flask
(``request``) pour tester la fonction sans serveur.
"""

from datetime import datetime

import pytest

from app import Calculate, already_calculated, distances, index


class MockRequest:
    """Fausse requete Flask exposant un corps JSON et une methode."""

    def __init__(self, payload):
        self._payload = payload

    @property
    def json(self):
        return self._payload

    @property
    def method(self):
        return "POST"


payloads = [
    ({"start_point": "0,0", "end_point": "3,4"}, 5.0),   # triangle 3-4-5
    ({"start_point": "2,5", "end_point": "1,6"}, 2 ** 0.5),  # exemple du sujet
    ({"start_point": "1,1", "end_point": "1,1"}, 0.0),   # points identiques
]


@pytest.mark.parametrize("payload,expected", payloads)
def test_calculate(monkeypatch, payload, expected):
    monkeypatch.setattr("app.request", MockRequest(payload))
    result = Calculate()
    assert result["result_distance"] == pytest.approx(expected)


def test_calculate_points(monkeypatch):
    monkeypatch.setattr("app.request", MockRequest({"start_point": "0,0", "end_point": "3,4"}))
    result = Calculate()
    assert result["start_point"] == [0, 0]
    assert result["end_point"] == (3, 4)


def test_api_root_renvoie_objet_vide():
    assert index() == {}


def test_already_calculated_reprend_l_historique():
    distances.clear()
    distances.append({
        "requested_at": datetime.now(),
        "result_distance": 5.0,
        "start_point": [0, 0],
        "end_point": (3, 4),
    })
    result = already_calculated()
    assert len(result) == 1
    assert result[0]["result_distance"] == 5.0
    distances.clear()
