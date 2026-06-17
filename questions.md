# Réponses au questionnaire

Projet : **my_distance** — calcul de distance entre deux points d'un plan 2D (Flask).
Auteur (identifiant anonymisé) : `cdwfs26-014`.

Outils utilisés (ceux vus en cours) : **uv**, **pytest** / **pytest-cov**, **SonarQube**
(dette technique + couverture), **Selenium** (interaction utilisateur), **Locust** +
**testcontainers** (performance), **Docker**.

---

## 1. Quelle était la dette technique en début de projet ? Comment l'avez-vous mesurée ?

Mesurée par **analyse statique SonarQube** (scanner `sonar-scanner-cli` configuré par
`sonar-project.properties` ; commandes dans le `README.md`). SonarQube exprime la dette comme
un **effort de remédiation** (temps) associé à une **note de maintenabilité** (A→E) et à un
inventaire de **code smells**, **bugs**, **vulnérabilités**, **duplications** et **couverture**.

Sur `app.py`, les principaux problèmes relevés :
- **code mort** : un `print` placé après un `return` dans `already_calculated` (jamais exécuté) ;
- **duplication** : le même dictionnaire de résultat construit deux fois dans `html_calculate` ;
- **nommage** trompeur et incohérent (`eNd`, `start`, `startPoint`, `EndPoint`) ;
- **structure** : un second `if request.method == 'POST'` au lieu d'un `else` ;
- **incohérence de conception** : `/api/distance` déclaré pour `GET`/`POST`/`PUT` alors qu'il
  exige un corps JSON (un `GET`/`PUT` sans corps échoue) ;
- **absence totale de tests** (couverture nulle) ;
- absence de docstrings, lambdas inutiles.

Bilan : note de maintenabilité dégradée et plusieurs code smells. (Le chiffre exact de
l'« effort de remédiation » se lit sur le tableau de bord SonarQube après le scan documenté.)

## 2. Quelle était la couverture en début de projet ? Comment l'avez-vous mesurée ?

**0 %.** Aucun test ni framework de test n'était présent. Mesurée avec **coverage.py via
pytest-cov**, dont le rapport `coverage.xml` est consommé par SonarQube
(`sonar.python.coverage.reportPaths=coverage.xml`) :

```bash
uv run pytest --cov=app
uv run coverage xml
```

Aucun test n'étant collecté, la couverture est nulle.

## 3. Quelle est la dette technique après vos modifications ? Qu'en dites-vous ?

J'ai volontairement **laissé le code de production inchangé** (hors périmètre des TP). Par
conséquent, les **code smells de maintenabilité restent présents** : la dette « structurelle »
(nommage, duplication, code mort, conception REST) est **inchangée**.

En revanche, l'ajout d'une **suite de tests** et d'une **couverture de 100 %** (cf. question 4)
améliore nettement les autres axes du *quality gate* SonarQube : la **couverture** passe de
0 % à 100 % et la **fiabilité** est sécurisée par les tests de non-régression.

Ce que j'en dis : la priorité demandée (tests et couverture) est atteinte. Pour réduire la
dette de maintenabilité restante, je **recommande** les actions correctives suivantes (non
appliquées ici) : supprimer le code mort, factoriser le dictionnaire dupliqué, renommer les
variables, remplacer le second `if` par un `else`, et mettre l'API en conformité REST
(POST uniquement sur `/api/distance`, codes `201`/`400`). À cela s'ajoute une dette
architecturale (historique en mémoire, pas de persistance, pas de CI).

## 4. Quelle est la couverture en fin de projet après vos modifications ? Qu'en dites-vous ?

La couverture **de lignes est de 100 %** sur `app.py` (métrique remontée à SonarQube via
`coverage.xml`) :

```
Name     Stmts   Miss  Cover
app.py      35      0   100%
```

Précision honnête : la **couverture de branches** est de **97 %**. Une condition reste non
couvrable (`14->exit`) : le second `if request.method == 'POST'` n'a pas de branche « faux »
atteignable (la route ne sert que GET/POST, et le cas GET est déjà traité au-dessus). C'est un
**défaut du code** (un `else` conviendrait) que j'ai identifié mais **pas corrigé**, par respect
du périmètre. Le `print` après `return` n'apparaît pas dans la mesure car CPython l'élimine
comme code inatteignable à la compilation.

La suite comprend aussi des **tests de caractérisation** (classe `TestComportementCasse`) qui **documentent les défauts de l'application sans la réparer** : entrée non numérique → **500**, coordonnée incomplète → **500**, champ de formulaire manquant → **400**, requête API sans corps JSON ou en GET/PUT → **415**. Ils vérifient le comportement réel observé, conformément à la consigne de tester l'application telle quelle.

Cette couverture provient des **tests unitaires** et **d'intégration**. Les tests
**fonctionnels Selenium** et de **performance Locust** valident en plus l'application déployée
(ils ne comptent pas dans ce pourcentage car ils s'exécutent contre un conteneur).

J'en dis que l'objectif de **couverture exhaustive** (engagement du contexte) est atteint en
lignes, en concentrant l'effort sur l'**interaction utilisateur** (formulaire web + API).
Nuance : 100 % de couverture ne garantit pas l'absence de bug — c'est la pertinence des
assertions qui compte autant que le pourcentage.

## 5. État des lieux : écart entre les attentes du contexte et l'organisation actuelle

**Attentes exprimées dans le contexte :**
- une campagne de tests **concentrée sur l'interaction utilisateur** ;
- une **couverture de test exhaustive** ;
- une montée en charge (usage massif) puis une extension planétaire (formule de Haversine).

**État à la réception du projet :**
- aucun test, aucune couverture, aucun framework de test ;
- pas de versionnage Git ni d'historique ;
- pas de documentation ni de spécification d'API ;
- dette technique élevée, aucune gestion d'erreurs ;
- API non conforme aux bonnes pratiques REST ;
- aucun outillage de mesure (SonarQube), de performance (Locust) ni de conteneurisation.

**Écart constaté :** l'organisation du développement était **immature** au regard des attentes
de qualité et de fiabilité. L'écart le plus critique : l'absence totale de tests, en
contradiction directe avec l'engagement de couverture exhaustive, et l'absence de tests
d'interaction utilisateur pourtant explicitement demandés.

**Ce qui a été mis en place (sans toucher au code de production) :**
- mise sous Git avec un historique clair (cf. question 6) ;
- campagne de tests à 4 niveaux : unitaires, intégration, **fonctionnels Selenium**
  (interaction utilisateur), **performance Locust/testcontainers** ;
- **couverture de lignes 100 %** mesurée par coverage.py et remontée à SonarQube ;
- documentation développeur + spécification **OpenAPI** + collection **Postman** ;
- outillage **SonarQube** (dette + couverture) et **Docker** (exécution + grid Selenium).


## 6. Schéma de la méthode de travail (branches)

Le sujet impose que **tous les commits soient présents sur la branche principale `main`**.
J'ai donc adopté une approche **trunk-based** : un historique linéaire sur `main` où chaque
commit est une étape isolée et clairement identifiable.

```
main
 │
 ●  08:51  Initial import (code du développeur principal, état reçu)
 │
 ●  09:05  Configuration projet uv + dockerisation (exécution + grid Selenium)
 │
 ●  09:25  Tests fixed (unitaires + intégration + Selenium + Locust)
 │
 ●  09:40  Documentation (DOCUMENTATION.md)
 │
 ●  09:52  OpenAPI (spécification openapi.yaml)
 │
 ●  10:00  SAST/DAST fixed (sonar-project.properties + commandes dans README.md)
 │
 ●  10:06  API (collection Postman de validation de l'API)
 │
 ●  10:12  Réponses au questionnaire (questions.md)
 ▼
(HEAD)
```

Le code de production n'a pas été modifié : il n'y a donc volontairement **aucun commit de
refactorisation**. Pour un projet réel en équipe, je recommanderais un modèle à **branches de
fonctionnalité** (`feature/*`) fusionnées dans `main` via *Pull Requests* après revue et CI.

## 7. L'API développée répond-elle aux exigences d'une architecture REST ? (argumentation)

**Non, pas pleinement.** Points conformes : usage de HTTP et représentation **JSON**, routes
organisées autour de ressources (`/api/distance`, `/api/distances`).

Points **non conformes** :
- **Verbes HTTP incohérents** : `/api/distance` déclare `GET`, `POST` *et* `PUT` pour une seule
  action, tout en lisant systématiquement un corps JSON — un `GET`/`PUT` sans corps échoue.
  REST impose une sémantique précise par verbe.
- **Codes de statut non respectés** : l'API renvoie toujours `200`, même quand une création
  devrait répondre `201` ou une entrée invalide `400`.
- **Absence de gestion d'erreur** structurée.
- **Découvrabilité nulle** : `/api` renvoie `{}`.
- **Nommage** mélangeant singulier/pluriel sans logique collection/élément.

Action corrective recommandée (non appliquée, hors périmètre) : restreindre `/api/distance` à
`POST` (réponse `201`), renvoyer `400` sur entrée invalide, et exposer la création via
`POST /api/distances`. La spécification `openapi.yaml` documente l'API **dans son état actuel**.

## 8. Quel framework de tests a été utilisé par le développeur principal ?

**Aucun.** Le projet transmis ne contenait aucun fichier de test ni aucune dépendance de test.
(Flask embarque pourtant un client de test via `flask.testing`, mais il n'était pas utilisé.)
J'ai introduit **pytest** (avec **pytest-cov**), complété par **Selenium** pour les tests
fonctionnels d'interaction utilisateur et **Locust** + **testcontainers** pour la performance —
l'outillage vu en cours.

## 9. Que pensez-vous des commentaires laissés par le développeur principal ?

Ils sont **insuffisants et de faible qualité** :
- seulement 2 lignes de commentaires pour tout le fichier ;
- ils décrivent l'évident plutôt que l'intention (« Si get, afficher la page vide » au-dessus
  d'un `return` explicite) : ils paraphrasent le *quoi* au lieu d'expliquer le *pourquoi* ;
- **aucun docstring** de module ou de fonction ;
- un commentaire accompagne du **code mort** (`print` placé après un `return`) ;
- aucune documentation des entrées/sorties de l'API.

Recommandation : ajouter des docstrings (rôle, paramètres, cas d'erreur) et des commentaires
expliquant les choix. J'ai fourni cette documentation à l'extérieur du code (`DOCUMENTATION.md`
et `openapi.yaml`) sans modifier les sources.
