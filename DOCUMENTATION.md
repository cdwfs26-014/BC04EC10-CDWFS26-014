# Documentation developpeur - my_distance

Documentation succincte pour comprendre et utiliser l'application.

## 1. Role de l'application

`my_distance` calcule la **distance entre deux points** d'un plan a 2 dimensions
a partir du **theoreme de Pythagore** :

```
distance(AB) = racine( (Bx - Ax)^2 + (By - Ay)^2 )
```

Exemple : pour A(2,5) et B(1,6), la distance vaut racine(2) ~ 1.414.

## 2. Installation et lancement

```bash
uv sync                              # installe les dependances (pyproject/uv.lock)
uv run flask --app app run           # http://127.0.0.1:5000
```

## 3. Interface web

Ouvrir `http://127.0.0.1:5000/` :
1. saisir le point A (champ `apoint`) au format `x,y` avec des entiers (ex. `2,5`) ;
2. saisir le point B (champ `bpoint`) au format `x,y` (ex. `1,6`) ;
3. cliquer sur **soumettre**.

Le resultat du calcul s'affiche en haut de la page.

## 4. API JSON

| Methode          | Route             | Description                            | Code |
|------------------|-------------------|----------------------------------------|------|
| GET              | `/api`            | Point d'entree (objet vide)            | 200  |
| POST (GET/PUT*)  | `/api/distance`   | Calcule la distance entre deux points  | 200  |
| GET              | `/api/distances`  | Historique de tous les calculs         | 200  |

(*) La route `/api/distance` est declaree pour POST, GET et PUT mais attend un
corps JSON ; POST est la methode a utiliser.

```bash
curl -X POST http://127.0.0.1:5000/api/distance \
     -H "Content-Type: application/json" \
     -d '{"start_point": "2,5", "end_point": "1,6"}'
```

La specification complete est fournie dans `openapi.yaml`.

## 5. Organisation du code

| Fichier                | Role                                                  |
|------------------------|-------------------------------------------------------|
| `app.py`               | Application Flask : vues web (`/`) et API (`/api...`)  |
| `templates/index.html` | Formulaire de saisie et affichage du resultat         |

Fonctions de `app.py` :
- `html_calculate` : formulaire (GET) et calcul (POST) cote web ;
- `index` : point d'entree `/api` ;
- `already_calculated` : historique `/api/distances` ;
- `Calculate` : calcul via l'API `/api/distance`.

> L'historique (`distances`) est stocke **en memoire** : il est perdu au
> redemarrage. Une base de donnees serait necessaire en production.

## 6. Tests

| Fichier                          | Type         | Outil                    |
|----------------------------------|--------------|--------------------------|
| `test_unit_distance.py`          | unitaire     | pytest                   |
| `test_integration_distance.py`   | integration  | pytest + client Flask    |
| `test_func_distance.py`          | fonctionnel  | Selenium (grid)          |
| `test_performance_distance.py`   | performance  | Locust + testcontainers  |

Les commandes d'execution, de couverture et d'analyse SonarQube sont dans le
`README.md`.

## 7. Evolution prevue

Pour les distances a l'echelle planetaire, le calcul de Pythagore sera complete
par la **formule de Haversine** (distance sur une sphere).
