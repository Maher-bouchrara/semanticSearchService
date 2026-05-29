# Semantic Search API — Documentation

## Overview

Cette API réalise une **recherche sémantique** sur une liste de publications scientifiques.

- Elle calcule un `score` de similarité entre une `query` et chaque publication.
- Si `pdfUrl` est fourni et accessible, le texte PDF est utilisé (sinon fallback sur `title + abstractText (+ keywords)`).
- Les résultats sont **triés par `score` décroissant**.

## Base URL

- `http://localhost:8000`

## Content-Type

- `application/json`

## CORS

Le service active CORS (utile pour appeler l'API depuis un navigateur / frontend).

- Par défaut : `allow_origins = ["*"]` (dev-friendly)
- Pour la prod : remplace par une liste d'origins autorisées (ex: `http://localhost:5173`, `https://mon-app.com`)

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

L'API sera disponible sur `http://localhost:8000`.

## Endpoints

### `GET /` — Health check

**Response**
```json
{ "message": "Semantic Search API is running ✅" }
```

---

### `GET /ping` — Ping

**Response**
```json
{ "status": "ok" }
```

---

### `POST /search` — Recherche sémantique (publications fournies)

Minimum requis par publication : `id`, `title`, `abstractText`.

**Request body**
```json
{
  "query": "string",
  "publications": [
    {
      "id": 1,
      "title": "string",
      "abstractText": "string",
      "keywords": "string | null",
      "doi": "string | null",
      "pdfUrl": "string | null",
      "imageUrl": "string | null",
      "journal": "string | null",
      "embedding": "[float] | null",
      "publicationDate": "YYYY-MM-DD | null",
      "status": "PUBLISHED | DRAFT | null",
      "createdAt": "ISO-8601 | null",
      "updatedAt": "ISO-8601 | null",
      "domain": {
        "id": 1,
        "name": "string",
        "description": "string"
      },
      "interactions": [],
      "researchers": [
        {
          "id": 1,
          "institution": "string",
          "position": "string",
          "bio": "string",
          "photoUrl": "string | null",
          "orcidId": "string | null",
          "createdAt": "ISO-8601 | null",
          "domains": [
            { "id": 1, "name": "string", "description": "string" }
          ]
        }
      ]
    }
  ]
}
```

**Response body** (publication complète + `score`)
```json
{
  "results": [
    {
      "id": 1,
      "title": "...",
      "abstractText": "...",
      "keywords": "...",
      "doi": null,
      "pdfUrl": "https://arxiv.org/pdf/2301.00001",
      "imageUrl": null,
      "journal": null,
      "embedding": null,
      "publicationDate": null,
      "status": null,
      "createdAt": null,
      "updatedAt": null,
      "domain": null,
      "interactions": [],
      "researchers": [],
      "score": 0.8732
    }
  ]
}
```

**curl (recommandé via fichier JSON)**
```bash
# Linux / macOS / Git Bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  --data-binary "@payload_search.json"

# Windows PowerShell (évite l'alias curl -> Invoke-WebRequest)
curl.exe -X POST "http://localhost:8000/search" -H "Content-Type: application/json" --data-binary "@payload_search.json"
```

**Python (`requests`)**
```python
import requests

payload = {
  "query": "deep learning medical imaging",
  "publications": [
    {
      "id": 1,
      "title": "Deep Learning pour le Diagnostic Medical par Imagerie",
      "abstractText": "Architecture CNN pour la detection precoce de tumeurs dans les images IRM.",
      "keywords": "deep learning, CNN, imagerie medicale",
      "pdfUrl": "https://arxiv.org/pdf/2301.00001",
    }
  ],
}

r = requests.post("http://localhost:8000/search", json=payload, timeout=120)
r.raise_for_status()
print(r.json())
```

---

### `POST /search-from-api` — Recherche via un endpoint externe

L’API récupère le JSON depuis `endpointUrl` (attendu au format `{ success, message, data: [...], timestamp }`) puis utilise `data[]` comme `publications`.

**Request body**
```json
{
  "query": "string",
  "endpointUrl": "http://localhost:8080/api/publications"
}
```

**Response body**
- Identique à `POST /search` (liste de publications complètes + `score`).

**Python (`requests`)**
```python
import requests

payload = {
  "query": "NLP language model fine-tuning",
  "endpointUrl": "http://localhost:8080/api/publications",
}

r = requests.post("http://localhost:8000/search-from-api", json=payload, timeout=120)
r.raise_for_status()
print(r.json())
```

---

## Errors

### `400 Bad Request`
- `query` vide
- `publications` vide (pour `/search`)
- `data[]` vide (pour `/search-from-api`)

### `422 Unprocessable Entity`
- JSON invalide / champs obligatoires manquants

### `502 Bad Gateway`
- `endpointUrl` inaccessible / timeout
- réponse non-JSON
- format inattendu par rapport au wrapper `{ success, message, data, timestamp }`

---

## Interactive docs (OpenAPI)

FastAPI expose automatiquement :

- Swagger UI : `http://localhost:8000/docs`
- OpenAPI JSON : `http://localhost:8000/openapi.json`
