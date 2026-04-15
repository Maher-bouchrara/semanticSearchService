# 📡 Semantic Search API — Guide des Appels

---

## Infos Générales

| | |
|---|---|
| **Base URL** | `http://localhost:8000` |
| **Format** | JSON |
| **Content-Type** | `application/json` |

---

## Endpoints

### `GET /` — Health Check

Vérifie que le serveur tourne.

```bash
curl http://localhost:8000/
```

**Réponse :**
```json
{ "message": "Semantic Search API is running ✅" }
```

---

### `GET /ping` — Ping

```bash
curl http://localhost:8000/ping
```

**Réponse :**
```json
{ "status": "ok" }
```

---

### `POST /search` — Recherche Sémantique

Endpoint principal. Prend une query + des publications, retourne les résultats classés par pertinence.

---

## Structure de la Requête

```json
{
  "query": "string (obligatoire)",
  "publications": [
    {
      "id": 1,
      "title": "string (obligatoire)",
      "abstractText": "string (obligatoire)",
      "keywords": "string (optionnel)",
      "doi": "string ou null",
      "pdfUrl": "string ou null",
      "journal": "string (optionnel)",
      "publicationDate": "YYYY-MM-DD (optionnel)",
      "status": "PUBLISHED ou DRAFT (optionnel)",
      "domain": {
        "id": 1,
        "name": "string",
        "description": "string"
      },
      "researchers": []
    }
  ]
}
```

## Structure de la Réponse

```json
{
  "results": [
    {
      "id": 1,
      "title": "string",
      "score": 0.87
    }
  ]
}
```

> `score` : entre `0.0` (aucun rapport) et `1.0` (correspondance parfaite). Résultats triés du meilleur au moins bon.

---

## Exemples d'Appels

### Exemple 1 — Avec `curl` (terminal)

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "deep learning medical imaging",
    "publications": [
      {
        "id": 1,
        "title": "Deep Learning pour le Diagnostic Medical par Imagerie",
        "abstractText": "Architecture CNN pour la detection precoce de tumeurs dans les images IRM.",
        "keywords": "deep learning, CNN, imagerie medicale",
        "pdfUrl": "https://arxiv.org/pdf/2301.00001"
      },
      {
        "id": 2,
        "title": "Cryptographie Post-Quantique",
        "abstractText": "Algorithmes resistants aux ordinateurs quantiques.",
        "keywords": "post-quantique, NIST, cryptographie",
        "pdfUrl": null
      }
    ]
  }'
```

**Réponse :**
```json
{
  "results": [
    { "id": 1, "title": "Deep Learning pour le Diagnostic Medical par Imagerie", "score": 0.87 },
    { "id": 2, "title": "Cryptographie Post-Quantique", "score": 0.12 }
  ]
}
```

---

### Exemple 2 — Avec Python (`requests`)

```python
import requests

url = "http://localhost:8000/search"

payload = {
    "query": "IoT edge computing smart city",
    "publications": [
        {
            "id": 3,
            "title": "Architecture Edge-Cloud Hybride pour Villes Intelligentes",
            "abstractText": "Infrastructure distribuee combinant edge computing et cloud.",
            "keywords": "IoT, edge computing, cloud hybride, smart city",
            "pdfUrl": "https://arxiv.org/pdf/2303.00003"
        },
        {
            "id": 5,
            "title": "Tableau de Bord Temps Reel pour la Chaine d'Approvisionnement",
            "abstractText": "Plateforme BI avec Kafka, Spark Streaming et Grafana.",
            "keywords": "BI, Kafka, Spark, Grafana",
            "pdfUrl": None  # pas de PDF
        }
    ]
}

response = requests.post(url, json=payload)
print(response.json())
```

**Réponse :**
```json
{
  "results": [
    { "id": 3, "title": "Architecture Edge-Cloud Hybride...", "score": 0.91 },
    { "id": 5, "title": "Tableau de Bord Temps Reel...",     "score": 0.23 }
  ]
}
```

---

### Exemple 3 — Avec le JSON complet de `getPublications`

Si tu récupères directement la réponse de ton API Java :

```python
import requests

# 1. Récupérer les publications depuis ton backend
api_response = requests.get("http://localhost:8080/api/publications").json()
publications = api_response["data"]  # extraire le tableau "data"

# 2. Envoyer à notre API de recherche
search_response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "NLP language model fine-tuning",
        "publications": publications
    }
)

results = search_response.json()["results"]
for r in results:
    print(f"[{r['score']:.2f}] {r['title']}")
```

**Réponse :**
```
[0.89] LLM Fine-Tuning pour l'Arabe Dialectal Tunisien
[0.61] Deep Learning pour le Diagnostic Medical par Imagerie
[0.21] Architecture Edge-Cloud Hybride pour Villes Intelligentes
[0.14] Cryptographie Post-Quantique : Etat de l'Art
[0.11] Tableau de Bord Temps Reel pour la Chaine d'Approvisionnement
[0.09] Securisation des Conteneurs Docker en Environnement Multi-Tenant
```

---

## Cas Particuliers

| Situation | Comportement |
|-----------|-------------|
| `pdfUrl` est `null` | Recherche sur `title + abstract + keywords` uniquement |
| `pdfUrl` inaccessible (404) | Fallback sur `title + abstract`, pas d'erreur |
| PDF sans texte (scanné) | Fallback sur `title + abstract` |
| `query` vide | Erreur `400 Bad Request` |
| `publications` vide | Erreur `400 Bad Request` |

---

## Erreurs Communes

```json
// 400 — Query vide
{ "detail": "La query ne peut pas être vide" }

// 400 — Publications vides
{ "detail": "La liste de publications ne peut pas être vide" }

// 422 — Champ obligatoire manquant (Pydantic)
{
  "detail": [
    { "type": "missing", "loc": ["body", "query"], "msg": "Field required" }
  ]
}
```

---

## Documentation Interactive

FastAPI génère automatiquement une interface de test :

```
http://localhost:8000/docs
```

> Ouvre dans ton navigateur → clique sur `POST /search` → "Try it out" → colle ton JSON → Execute.