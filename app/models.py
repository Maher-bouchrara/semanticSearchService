# models.py — Modèles Pydantic correspondant exactement au JSON réel

from pydantic import BaseModel
from typing import Optional, List

print("ena models.py")

# ─────────────────────────────────────────
# SOUS-MODÈLES (objets imbriqués)
# ─────────────────────────────────────────

class Domain(BaseModel):
    """Un domaine de recherche (ex: Intelligence Artificielle)"""
    id: int
    name: str
    description: str

    class Config:
        # Ignore les champs inconnus comme "hibernateLazyInitializer"
        # Sans ça, Pydantic lèverait une erreur sur ce champ Java
        extra = "ignore"


class Researcher(BaseModel):
    """Un chercheur auteur de la publication"""
    id: int
    institution: str
    position: str
    bio: str
    photoUrl: Optional[str] = None
    orcidId: Optional[str] = None
    createdAt: Optional[str] = None
    domains: Optional[List[Domain]] = []

    class Config:
        extra = "ignore"


# ─────────────────────────────────────────
# MODÈLE PRINCIPAL — UNE PUBLICATION
# ─────────────────────────────────────────

class Publication(BaseModel):
    """
    Représente une publication de recherche complète.
    Correspond exactement à un objet dans data[] du JSON.
    """
    id: int
    title: str
    abstractText: str
    keywords: Optional[str] = None
    doi: Optional[str] = None           # Peut être null
    pdfUrl: Optional[str] = None        # Peut être null (ex: publication 5)
    journal: Optional[str] = None
    publicationDate: Optional[str] = None
    status: Optional[str] = None        # "PUBLISHED" ou "DRAFT"
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    domain: Optional[Domain] = None
    researchers: Optional[List[Researcher]] = []

    class Config:
        extra = "ignore"


# ─────────────────────────────────────────
# WRAPPER — LA RÉPONSE COMPLÈTE DE TON API
# ─────────────────────────────────────────

class PublicationsApiResponse(BaseModel):
    """
    Le JSON complet retourné par ton endpoint getPublications.
    On l'utilise pour parser la réponse entière proprement.
    """
    success: bool
    message: str
    data: List[Publication]
    timestamp: str


# ─────────────────────────────────────────
# INPUT DE NOTRE API — POST /search
# ─────────────────────────────────────────

class SearchRequest(BaseModel):
    """
    Ce que l'utilisateur envoie à notre API.
    Il envoie la query + la liste complète des publications.
    """
    query: str
    publications: List[Publication]


# ─────────────────────────────────────────
# OUTPUT DE NOTRE API — Résultats classés
# ─────────────────────────────────────────

class PublicationResult(BaseModel):
    """Un résultat dans la liste finale classée"""
    id: int
    title: str
    score: float


class SearchResponse(BaseModel):
    """La réponse finale de POST /search"""
    results: List[PublicationResult]