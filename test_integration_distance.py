"""Tests d'integration : routes web et API via le client de test Flask.

Deux clients sont utilises :
  * ``client``      : TESTING=True (cas nominaux) ;
  * ``client_brut`` : renvoie le vrai code HTTP, y compris 500, pour documenter
                      le comportement de l'application transmise (cassee).
"""

import pytest

from app import app as flask_app
from app import distances


@pytest.fixture()
def client():
    flask_app.config.update({"TESTING": True})
    distances.clear()
    with flask_app.test_client() as test_client:
        yield test_client
    distances.clear()


@pytest.fixture()
def client_brut():
    """Client qui renvoie le vrai code HTTP : une exception non geree -> 500."""
    flask_app.config.update({"TESTING": False, "PROPAGATE_EXCEPTIONS": False})
    distances.clear()
    with flask_app.test_client() as test_client:
        yield test_client
    distances.clear()
    flask_app.config.update({"TESTING": True, "PROPAGATE_EXCEPTIONS": None})


# === Cas nominaux (interaction utilisateur) ===============================

def test_get_affiche_le_formulaire(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"apoint" in response.data
    assert b"bpoint" in response.data


def test_post_calcule_et_affiche_le_resultat(client):
    response = client.post("/", data={"apoint": "2,5", "bpoint": "1,6"})
    assert response.status_code == 200
    assert b"Votre resultat est" in response.data
    assert len(distances) == 1


def test_api_root(client):
    response = client.get("/api")
    assert response.status_code == 200
    assert response.get_json() == {}


def test_api_distance_calcule(client):
    response = client.post("/api/distance", json={"start_point": "0,0", "end_point": "3,4"})
    assert response.status_code == 200
    assert response.get_json()["result_distance"] == 5.0


def test_api_distances_historique(client):
    assert client.get("/api/distances").get_json() == []
    client.post("/", data={"apoint": "0,0", "bpoint": "3,4"})
    historique = client.get("/api/distances").get_json()
    assert len(historique) == 1
    assert historique[0]["result_distance"] == 5.0


# === Tests de caracterisation : comportement de l'appli CASSEE =============
# Ces tests documentent les defauts de l'application transmise SANS les corriger.
# L'application ne valide aucune entree : toute entree invalide provoque une
# erreur serveur (500) ou une erreur HTTP (400 / 415).

class TestComportementCasse:

    def test_web_lettres_renvoie_500(self, client_brut):
        # int('abc') -> ValueError non geree -> 500
        assert client_brut.post("/", data={"apoint": "abc", "bpoint": "1,6"}).status_code == 500

    def test_web_coordonnee_incomplete_renvoie_500(self, client_brut):
        # une seule coordonnee -> IndexError non geree -> 500
        assert client_brut.post("/", data={"apoint": "2", "bpoint": "1,6"}).status_code == 500

    def test_web_champ_manquant_renvoie_400(self, client_brut):
        # champ 'bpoint' absent du formulaire -> 400 Bad Request
        assert client_brut.post("/", data={"apoint": "2,5"}).status_code == 400

    def test_api_sans_corps_json_renvoie_415(self, client_brut):
        # corps JSON requis (Content-Type) -> 415 Unsupported Media Type
        assert client_brut.post("/api/distance").status_code == 415

    @pytest.mark.parametrize("verbe", ["get", "put"])
    def test_api_methodes_declarees_sans_body_renvoient_415(self, client_brut, verbe):
        # /api/distance declare GET/POST/PUT mais exige toujours un corps JSON
        assert getattr(client_brut, verbe)("/api/distance").status_code == 415

    def test_api_lettres_renvoie_500(self, client_brut):
        # int('a') -> ValueError non geree -> 500
        assert client_brut.post(
            "/api/distance", json={"start_point": "a,b", "end_point": "1,6"}
        ).status_code == 500

    def test_api_cle_manquante_renvoie_500(self, client_brut):
        # cle 'end_point' absente -> KeyError non geree -> 500
        assert client_brut.post(
            "/api/distance", json={"start_point": "2,5"}
        ).status_code == 500
