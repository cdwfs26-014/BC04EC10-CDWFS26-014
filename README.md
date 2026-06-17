# my_distance - Historique des commandes

Application de calcul de distance entre deux points d'un plan 2D (Flask).
Ce fichier rassemble les commandes utiles : execution, tests, couverture,
analyse de dette technique (SonarQube), Selenium et performance.

## Initialisation (uv)

```bash
uv sync
```

## Demarrage du serveur de developpement

```bash
uv run flask --app app run --debug        # http://127.0.0.1:5000
```

## Tests

```bash
# Tests unitaires et d'integration (sans dependance externe)
uv run pytest test_unit_distance.py test_integration_distance.py

# Tests fonctionnels Selenium (necessite le grid, voir plus bas)
uv run pytest test_func_distance.py

# Test de performance (necessite Docker)
uv run pytest test_performance_distance.py
```

## Couverture de tests (coverage.py)

```bash
uv run pytest test_unit_distance.py test_integration_distance.py --cov=app
uv run coverage xml          # genere coverage.xml (lu par sonar-scanner)
```

## SAST - Dette technique avec SonarQube

`sonar-project.properties` declare la cle de projet, le fichier analyse
(`sonar.inclusions=app.py`) et le rapport de couverture (`coverage.xml`).

```bash
# Demarrer une instance SonarQube locale (base h2)
docker run --name sonarqube -d -p 9000:9000 sonarqube:latest

# Reseau pour relier le scanner au serveur
docker network create sonar_network
docker network connect sonar_network sonarqube --alias sonarqube

# Analyse avec le sonar-scanner CLI (remplacer le token)
docker run --network sonar_network --rm \
  -e SONAR_HOST_URL="http://sonarqube:9000" \
  -e SONAR_TOKEN="<token_a_changer>" \
  -v "${PWD}:/usr/src" sonarsource/sonar-scanner-cli
```

## Tests fonctionnels Selenium (interaction utilisateur)

```bash
# Lancer le grid Selenium (hub + chrome + firefox) + l'application
docker compose -f grid/compose.yaml up -d --build

# Copier .env.example en .env puis lancer les tests fonctionnels
cp .env.example .env
uv run pytest test_func_distance.py
```

## Conteneurisation / execution

```bash
docker build -t my_distance:latest .
docker compose -f system/compose.yaml up -d --build
```

## Test de performance (Locust)

```bash
# Via testcontainers (image construite automatiquement)
uv run pytest test_performance_distance.py

# Ou en mode interactif avec l'interface Locust
uv run locust -f locustfile.py --host http://127.0.0.1:5000
```
