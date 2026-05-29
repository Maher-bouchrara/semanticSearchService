# main.py - Point d'entree final avec l'endpoint /search complet

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

from app.models import PublicationsApiResponse, SearchFromApiRequest, SearchRequest, SearchResponse
from app.search import semantic_search

app = FastAPI(
    title="Semantic Search API",
    description="Recherche semantique sur des publications scientifiques",
    version="1.0.0"
)

# CORS (pour permettre l'appel depuis un frontend / autre projet)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Semantic Search API is running ✅"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    """
    Recherche semantique sur une liste de publications.

    - Telecharge les PDFs disponibles
    - Calcule la similarite semantique avec la query
    - Retourne les publications triees par pertinence
    """

    # Verifications basiques
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="La query ne peut pas etre vide"
        )

    if not request.publications:
        raise HTTPException(
            status_code=400,
            detail="La liste de publications ne peut pas etre vide"
        )

    # Lancer la pipeline de recherche
    results = semantic_search(
        query=request.query,
        publications=request.publications
    )

    return SearchResponse(results=results)


def fetch_publications(url: str):
    """
    Recupere les publications depuis un endpoint externe.
    """
    try:
        response = requests.get(url, timeout=30)
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur reseau lors de la recuperation des publications: {exc}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Publications API error: {response.status_code}"
        )

    try:
        payload = response.json()
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="Reponse JSON invalide depuis l'API des publications"
        )

    try:
        parsed = PublicationsApiResponse.parse_obj(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Format inattendu de l'API des publications: {exc}"
        )

    return parsed.data


@app.post("/search-from-api", response_model=SearchResponse)
def search_from_api(request: SearchFromApiRequest):
    """
    Recherche semantique en recuperant les publications depuis un endpoint externe.
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="La query ne peut pas etre vide"
        )

    publications = fetch_publications(request.endpointUrl)
    if not publications:
        raise HTTPException(
            status_code=400,
            detail="La liste de publications recuperee est vide"
        )

    results = semantic_search(
        query=request.query,
        publications=publications
    )

    return SearchResponse(results=results)