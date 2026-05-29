# models.py - Modeles Pydantic correspondant exactement au JSON reel

from pydantic import BaseModel, Field
from typing import Optional, List, Any

print("ena models.py")

# ------------------------------------
# SOUS-MODELES (objets imbriques)
# ------------------------------------

class Domain(BaseModel):
    """Un domaine de recherche (ex: Intelligence Artificielle)"""
    id: int
    name: str
    description: str

    class Config:
        # Ignore les champs inconnus comme "hibernateLazyInitializer"
        # Sans ca, Pydantic leverait une erreur sur ce champ Java
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
    domains: List[Domain] = Field(default_factory=list)

    class Config:
        extra = "ignore"


# ------------------------------------
# MODELE PRINCIPAL - UNE PUBLICATION
# ------------------------------------

class Publication(BaseModel):
    """
    Represente une publication de recherche complete.
    Correspond exactement a un objet dans data[] du JSON.
    """
    id: int
    title: str
    abstractText: str
    keywords: Optional[str] = None
    doi: Optional[str] = None           # Peut etre null
    pdfUrl: Optional[str] = None        # Peut etre null (ex: publication 5)
    imageUrl: Optional[str] = None
    journal: Optional[str] = None
    embedding: Optional[List[float]] = None
    publicationDate: Optional[str] = None
    status: Optional[str] = None        # "PUBLISHED" ou "DRAFT"
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    domain: Optional[Domain] = None
    interactions: List[Any] = Field(default_factory=list)
    researchers: List[Researcher] = Field(default_factory=list)

    class Config:
        extra = "ignore"


# ------------------------------------
# WRAPPER - LA REPONSE COMPLETE DE TON API
# ------------------------------------

class PublicationsApiResponse(BaseModel):
    """
    Le JSON complet retourne par ton endpoint getPublications.
    On l'utilise pour parser la reponse entiere proprement.
    """
    success: bool
    message: str
    data: List[Publication]
    timestamp: str


# ------------------------------------
# INPUT DE NOTRE API - POST /search
# ------------------------------------

class SearchRequest(BaseModel):
    """
    Ce que l'utilisateur envoie a notre API.
    Il envoie la query + la liste complete des publications.
    """
    query: str
    publications: List[Publication]


class SearchFromApiRequest(BaseModel):
    """
    Recherche semantique a partir d'un endpoint externe.
    """
    query: str
    endpointUrl: str = "example/api/getpubs"


# ------------------------------------
# OUTPUT DE NOTRE API - Resultats classes
# ------------------------------------
class PublicationResult(Publication):
    """Une publication complete avec son score de pertinence"""
    score: float


class SearchResponse(BaseModel):
    """La reponse finale de POST /search"""
    results: List[PublicationResult]