# main.py — Point d'entrée final avec l'endpoint /search complet

from fastapi import FastAPI, HTTPException
from app.models import SearchRequest, SearchResponse
from app.search import semantic_search

app = FastAPI(
    title="Semantic Search API",
    description="Recherche sémantique sur des publications scientifiques",
    version="1.0.0"
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
    Recherche sémantique sur une liste de publications.

    - Télécharge les PDFs disponibles
    - Calcule la similarité sémantique avec la query
    - Retourne les publications triées par pertinence
    """

    # Vérifications basiques
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="La query ne peut pas être vide"
        )

    if not request.publications:
        raise HTTPException(
            status_code=400,
            detail="La liste de publications ne peut pas être vide"
        )

    # Lancer la pipeline de recherche
    results = semantic_search(
        query=request.query,
        publications=request.publications
    )

    return SearchResponse(results=results)