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

### `POST /search-from-api` — Recherche via un endpoint externe

Même principe que `/search`, mais au lieu de fournir `publications` directement, tu fournis `endpointUrl` (ton backend Java par exemple). L'API récupère `data[]` puis lance la recherche.

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

### Requête `POST /search-from-api`

```json
{
  "query": "string (obligatoire)",
  "endpointUrl": "https://exemple.com/api/publications"
}
```

## Structure de la Réponse

```json
{
  "results": [
    {
      "id": 1,
      "title": "string",
      "abstractText": "string",
      "keywords": "string ou null",
      "doi": "string ou null",
      "pdfUrl": "string ou null",
      "imageUrl": "string ou null",
      "journal": "string ou null",
      "embedding": "[float] ou null",
      "publicationDate": "YYYY-MM-DD ou null",
      "status": "PUBLISHED | DRAFT | null",
      "createdAt": "ISO-8601 ou null",
      "updatedAt": "ISO-8601 ou null",
      "domain": { "id": 1, "name": "string", "description": "string" },
      "interactions": [],
      "researchers": [],
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
    {
      "id": 1,
      "title": "Deep Learning pour le Diagnostic Medical par Imagerie",
      "abstractText": "Architecture CNN pour la detection precoce de tumeurs dans les images IRM.",
      "keywords": "deep learning, CNN, imagerie medicale",
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
      "score": 0.87
    },
    {
      "id": 2,
      "title": "Cryptographie Post-Quantique",
      "abstractText": "Algorithmes resistants aux ordinateurs quantiques.",
      "keywords": "post-quantique, NIST, cryptographie",
      "doi": null,
      "pdfUrl": null,
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
      "score": 0.12
    }
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
    {
      "id": 3,
      "title": "Architecture Edge-Cloud Hybride pour Villes Intelligentes",
      "abstractText": "Infrastructure distribuee combinant edge computing et cloud.",
      "keywords": "IoT, edge computing, cloud hybride, smart city",
      "doi": null,
      "pdfUrl": "https://arxiv.org/pdf/2303.00003",
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
      "score": 0.91
    },
    {
      "id": 5,
      "title": "Tableau de Bord Temps Reel pour la Chaine d'Approvisionnement",
      "abstractText": "Plateforme BI avec Kafka, Spark Streaming et Grafana.",
      "keywords": "BI, Kafka, Spark, Grafana",
      "doi": null,
      "pdfUrl": null,
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
      "score": 0.23
    }
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

### Exemple 4 — Utiliser directement le `data[]` (copier/coller)

Si tu as déjà un JSON de type `getPublications` (comme celui que tu as partagé), tu peux prendre **uniquement le tableau `data[]`** et l'envoyer en entrée de `POST /search`.

> Important : certains titres contiennent un apostrophe (ex: `l'Art`, `l'Arabe`). Pour éviter les problèmes de quoting shell, le plus simple est d'utiliser un fichier JSON (au lieu de `-d '{...}'`).

1) Crée un fichier `payload_search.json` avec ce contenu :

```json
{
  "query": "deep learning medical imaging",
  "publications": [
    {
      "id": 1,
      "title": "Deep Learning pour le Diagnostic Medical par Imagerie",
      "abstractText": "Architecture CNN pour la detection precoce de tumeurs dans les images IRM. Notre modele atteint une precision de 97,3% sur le dataset MedMNIST.",
      "keywords": "deep learning, CNN, imagerie medicale, diagnostic, IRM",
      "doi": "10.1000/xyz123",
      "pdfUrl": "https://arxiv.org/pdf/2301.00001",
      "imageUrl": null,
      "journal": "Journal of Medical Artificial Intelligence",
      "embedding": null,
      "publicationDate": "2024-03-15",
      "status": "PUBLISHED",
      "createdAt": "2026-05-28T17:40:58.337889",
      "updatedAt": "2026-05-28T17:40:58.337889",
      "domain": {
        "id": 1,
        "name": "Intelligence Artificielle",
        "description": "Apprentissage automatique, deep learning, NLP et vision par ordinateur.",
        "hibernateLazyInitializer": {}
      },
      "interactions": [],
      "researchers": [
        {
          "id": 1,
          "institution": "Universite de Tunis El Manar",
          "position": "Maitre de conferences",
          "bio": "Specialiste en deep learning applique a la reconnaissance d'images medicales.",
          "photoUrl": "https://randomuser.me/api/portraits/men/11.jpg",
          "orcidId": "0000-0001-2345-6789",
          "createdAt": "2026-05-28T17:40:58.319382",
          "domains": [
            {
              "id": 3,
              "name": "Business Intelligence",
              "description": "Analyse de donnees, data warehousing, tableaux de bord et aide a la decision.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 1,
              "name": "Intelligence Artificielle",
              "description": "Apprentissage automatique, deep learning, NLP et vision par ordinateur.",
              "hibernateLazyInitializer": {}
            }
          ]
        },
        {
          "id": 4,
          "institution": "MIT - Massachusetts Institute of Technology",
          "position": "Research Scientist",
          "bio": "Expert en NLP et grands modeles de langage (LLM).",
          "photoUrl": "https://randomuser.me/api/portraits/men/44.jpg",
          "orcidId": "0000-0004-5678-9012",
          "createdAt": "2026-05-28T17:40:58.332404",
          "domains": [
            {
              "id": 1,
              "name": "Intelligence Artificielle",
              "description": "Apprentissage automatique, deep learning, NLP et vision par ordinateur.",
              "hibernateLazyInitializer": {}
            }
          ]
        }
      ]
    },
    {
      "id": 2,
      "title": "Cryptographie Post-Quantique : Etat de l'Art",
      "abstractText": "Analyse comparative des algorithmes resistants aux ordinateurs quantiques selectionnes par le NIST et leur integration dans les protocoles TLS 1.3.",
      "keywords": "post-quantique, NIST, cryptographie, TLS",
      "doi": "10.1000/abc456",
      "pdfUrl": "https://arxiv.org/pdf/2302.00002",
      "imageUrl": null,
      "journal": "IEEE Transactions on Information Security",
      "embedding": null,
      "publicationDate": "2024-06-01",
      "status": "PUBLISHED",
      "createdAt": "2026-05-28T17:40:58.342267",
      "updatedAt": "2026-05-28T17:40:58.342267",
      "domain": {
        "id": 2,
        "name": "Cybersecurite",
        "description": "Securite des systemes, cryptographie, detection d'intrusion et protection des donnees.",
        "hibernateLazyInitializer": {}
      },
      "interactions": [],
      "researchers": [
        {
          "id": 2,
          "institution": "Ecole Nationale d'Ingenieurs de Sfax",
          "position": "Professeure associee",
          "bio": "Chercheuse en cybersecurite et cryptographie post-quantique.",
          "photoUrl": "https://randomuser.me/api/portraits/women/22.jpg",
          "orcidId": "0000-0002-3456-7890",
          "createdAt": "2026-05-28T17:40:58.324197",
          "domains": [
            {
              "id": 4,
              "name": "Cloud Computing",
              "description": "Architectures distribuees, microservices, conteneurisation et orchestration.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 2,
              "name": "Cybersecurite",
              "description": "Securite des systemes, cryptographie, detection d'intrusion et protection des donnees.",
              "hibernateLazyInitializer": {}
            }
          ]
        }
      ]
    },
    {
      "id": 3,
      "title": "Architecture Edge-Cloud Hybride pour Villes Intelligentes",
      "abstractText": "Infrastructure distribuee combinant edge computing et cloud pour reduire la latence des applications IoT urbaines de 60%. Pilote a Sfax.",
      "keywords": "IoT, edge computing, cloud hybride, smart city",
      "doi": "10.1000/def789",
      "pdfUrl": "https://arxiv.org/pdf/2303.00003",
      "imageUrl": null,
      "journal": "Future Generation Computer Systems",
      "embedding": null,
      "publicationDate": "2024-09-20",
      "status": "PUBLISHED",
      "createdAt": "2026-05-28T17:40:58.349264",
      "updatedAt": "2026-05-28T17:40:58.349264",
      "domain": {
        "id": 5,
        "name": "Internet des Objets (IoT)",
        "description": "Capteurs connectes, protocoles embarques, edge computing et smart systems.",
        "hibernateLazyInitializer": {}
      },
      "interactions": [],
      "researchers": [
        {
          "id": 2,
          "institution": "Ecole Nationale d'Ingenieurs de Sfax",
          "position": "Professeure associee",
          "bio": "Chercheuse en cybersecurite et cryptographie post-quantique.",
          "photoUrl": "https://randomuser.me/api/portraits/women/22.jpg",
          "orcidId": "0000-0002-3456-7890",
          "createdAt": "2026-05-28T17:40:58.324197",
          "domains": [
            {
              "id": 4,
              "name": "Cloud Computing",
              "description": "Architectures distribuees, microservices, conteneurisation et orchestration.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 2,
              "name": "Cybersecurite",
              "description": "Securite des systemes, cryptographie, detection d'intrusion et protection des donnees.",
              "hibernateLazyInitializer": {}
            }
          ]
        },
        {
          "id": 3,
          "institution": "Institut Superieur d'Informatique",
          "position": "Doctorant - 3e annee",
          "bio": "Recherches sur l'IoT et les architectures edge pour les smart cities.",
          "photoUrl": "https://randomuser.me/api/portraits/men/33.jpg",
          "orcidId": "0000-0003-4567-8901",
          "createdAt": "2026-05-28T17:40:58.327992",
          "domains": [
            {
              "id": 4,
              "name": "Cloud Computing",
              "description": "Architectures distribuees, microservices, conteneurisation et orchestration.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 5,
              "name": "Internet des Objets (IoT)",
              "description": "Capteurs connectes, protocoles embarques, edge computing et smart systems.",
              "hibernateLazyInitializer": {}
            }
          ]
        }
      ]
    },
    {
      "id": 4,
      "title": "LLM Fine-Tuning pour l'Arabe Dialectal Tunisien",
      "abstractText": "Adaptation de LLaMA-3 et Mistral sur un corpus de 500K phrases en arabe tunisien. Amelioration du score BLEU de 18 points.",
      "keywords": "LLM, NLP, arabe dialectal, fine-tuning, LLaMA",
      "doi": "10.1000/ghi012",
      "pdfUrl": "https://arxiv.org/pdf/2401.00004",
      "imageUrl": null,
      "journal": "Transactions on Arabic Language Processing",
      "embedding": null,
      "publicationDate": "2025-01-10",
      "status": "PUBLISHED",
      "createdAt": "2026-05-28T17:40:58.353573",
      "updatedAt": "2026-05-28T17:40:58.353573",
      "domain": {
        "id": 1,
        "name": "Intelligence Artificielle",
        "description": "Apprentissage automatique, deep learning, NLP et vision par ordinateur.",
        "hibernateLazyInitializer": {}
      },
      "interactions": [],
      "researchers": [
        {
          "id": 1,
          "institution": "Universite de Tunis El Manar",
          "position": "Maitre de conferences",
          "bio": "Specialiste en deep learning applique a la reconnaissance d'images medicales.",
          "photoUrl": "https://randomuser.me/api/portraits/men/11.jpg",
          "orcidId": "0000-0001-2345-6789",
          "createdAt": "2026-05-28T17:40:58.319382",
          "domains": [
            {
              "id": 3,
              "name": "Business Intelligence",
              "description": "Analyse de donnees, data warehousing, tableaux de bord et aide a la decision.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 1,
              "name": "Intelligence Artificielle",
              "description": "Apprentissage automatique, deep learning, NLP et vision par ordinateur.",
              "hibernateLazyInitializer": {}
            }
          ]
        },
        {
          "id": 4,
          "institution": "MIT - Massachusetts Institute of Technology",
          "position": "Research Scientist",
          "bio": "Expert en NLP et grands modeles de langage (LLM).",
          "photoUrl": "https://randomuser.me/api/portraits/men/44.jpg",
          "orcidId": "0000-0004-5678-9012",
          "createdAt": "2026-05-28T17:40:58.332404",
          "domains": [
            {
              "id": 1,
              "name": "Intelligence Artificielle",
              "description": "Apprentissage automatique, deep learning, NLP et vision par ordinateur.",
              "hibernateLazyInitializer": {}
            }
          ]
        }
      ]
    },
    {
      "id": 5,
      "title": "Tableau de Bord Temps Reel pour la Chaine d'Approvisionnement",
      "abstractText": "Plateforme BI avec Kafka, Spark Streaming et Grafana. Reduction du delai de detection des anomalies de 4h a 3 minutes.",
      "keywords": "BI, Kafka, Spark, Grafana, temps reel, logistique",
      "doi": null,
      "pdfUrl": null,
      "imageUrl": null,
      "journal": "International Journal of Data Engineering",
      "embedding": null,
      "publicationDate": "2025-03-05",
      "status": "DRAFT",
      "createdAt": "2026-05-28T17:40:58.357478",
      "updatedAt": "2026-05-28T17:40:58.357478",
      "domain": {
        "id": 3,
        "name": "Business Intelligence",
        "description": "Analyse de donnees, data warehousing, tableaux de bord et aide a la decision.",
        "hibernateLazyInitializer": {}
      },
      "interactions": [],
      "researchers": [
        {
          "id": 1,
          "institution": "Universite de Tunis El Manar",
          "position": "Maitre de conferences",
          "bio": "Specialiste en deep learning applique a la reconnaissance d'images medicales.",
          "photoUrl": "https://randomuser.me/api/portraits/men/11.jpg",
          "orcidId": "0000-0001-2345-6789",
          "createdAt": "2026-05-28T17:40:58.319382",
          "domains": [
            {
              "id": 3,
              "name": "Business Intelligence",
              "description": "Analyse de donnees, data warehousing, tableaux de bord et aide a la decision.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 1,
              "name": "Intelligence Artificielle",
              "description": "Apprentissage automatique, deep learning, NLP et vision par ordinateur.",
              "hibernateLazyInitializer": {}
            }
          ]
        }
      ]
    },
    {
      "id": 6,
      "title": "Securisation des Conteneurs Docker en Environnement Multi-Tenant",
      "abstractText": "Vulnerabilites des configurations Docker par defaut et framework de durcissement automatise base sur les benchmarks CIS.",
      "keywords": "Docker, conteneurisation, securite, CIS, multi-tenant",
      "doi": "10.1000/jkl345",
      "pdfUrl": "https://arxiv.org/pdf/2404.00006",
      "imageUrl": null,
      "journal": "Journal of Cloud Security",
      "embedding": null,
      "publicationDate": "2025-02-18",
      "status": "PUBLISHED",
      "createdAt": "2026-05-28T17:40:58.36118",
      "updatedAt": "2026-05-28T17:40:58.36118",
      "domain": {
        "id": 4,
        "name": "Cloud Computing",
        "description": "Architectures distribuees, microservices, conteneurisation et orchestration.",
        "hibernateLazyInitializer": {}
      },
      "interactions": [],
      "researchers": [
        {
          "id": 2,
          "institution": "Ecole Nationale d'Ingenieurs de Sfax",
          "position": "Professeure associee",
          "bio": "Chercheuse en cybersecurite et cryptographie post-quantique.",
          "photoUrl": "https://randomuser.me/api/portraits/women/22.jpg",
          "orcidId": "0000-0002-3456-7890",
          "createdAt": "2026-05-28T17:40:58.324197",
          "domains": [
            {
              "id": 4,
              "name": "Cloud Computing",
              "description": "Architectures distribuees, microservices, conteneurisation et orchestration.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 2,
              "name": "Cybersecurite",
              "description": "Securite des systemes, cryptographie, detection d'intrusion et protection des donnees.",
              "hibernateLazyInitializer": {}
            }
          ]
        },
        {
          "id": 3,
          "institution": "Institut Superieur d'Informatique",
          "position": "Doctorant - 3e annee",
          "bio": "Recherches sur l'IoT et les architectures edge pour les smart cities.",
          "photoUrl": "https://randomuser.me/api/portraits/men/33.jpg",
          "orcidId": "0000-0003-4567-8901",
          "createdAt": "2026-05-28T17:40:58.327992",
          "domains": [
            {
              "id": 4,
              "name": "Cloud Computing",
              "description": "Architectures distribuees, microservices, conteneurisation et orchestration.",
              "hibernateLazyInitializer": {}
            },
            {
              "id": 5,
              "name": "Internet des Objets (IoT)",
              "description": "Capteurs connectes, protocoles embarques, edge computing et smart systems.",
              "hibernateLazyInitializer": {}
            }
          ]
        }
      ]
    }
  ]
}
```

2) Envoie la requête :

```bash
# Linux / macOS / Git Bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  --data-binary "@payload_search.json"

# Windows PowerShell (évite l'alias curl -> Invoke-WebRequest)
curl.exe -X POST "http://localhost:8000/search" -H "Content-Type: application/json" --data-binary "@payload_search.json"
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