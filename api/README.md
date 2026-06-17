# Validation de l'API my_distance (Postman)

Collection Postman permettant de valider l'API manuellement (interface Postman)
ou automatiquement en ligne de commande avec **Newman** :

```bash
# Prerequis : application lancee (uv run flask --app app run) sur http://127.0.0.1:5000
npm install -g newman
newman run api/my_distance.postman_collection.json
```

La collection couvre les routes existantes : `/api`, `/api/distance` (POST) et
`/api/distances`. Les assertions refletent le comportement actuel de l'API
(reponses HTTP 200).
