# search.py — Orchestre toute la logique de recherche sémantique

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.models import Publication, PublicationResult
from app.pdf_utils import extract_text_from_pdf
from app.embedding_utils import get_embedding, get_embeddings_batch

print("ena search.py")

# ─────────────────────────────────────────────────────────────────
# ÉTAPE 1 — Découper un texte en chunks
# ─────────────────────────────────────────────────────────────────

def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Découpe un texte long en petits morceaux qui se chevauchent légèrement.

    Paramètres:
        text       : le texte complet à découper
        chunk_size : taille de chaque chunk en caractères (défaut: 500)
        overlap    : chevauchement entre chunks (défaut: 100 chars)

    Retourne:
        Liste de strings (les chunks)

    Exemple:
        text = "ABCDEFGHIJ" (10 chars)
        chunk_size=4, overlap=1
        → ["ABCD", "DEFG", "GHIJ"]
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # Ne pas ajouter un chunk vide ou trop court (bruit)
        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())

        # Avancer de (chunk_size - overlap) pour créer le chevauchement
        start += chunk_size - overlap

    return chunks


# ─────────────────────────────────────────────────────────────────
# ÉTAPE 2 — Calculer le score d'une publication vs la query
# ─────────────────────────────────────────────────────────────────

def compute_publication_score(
    query_embedding: np.ndarray,
    publication: Publication
) -> float:
    """
    Calcule le score de similarité entre la query et une publication.

    Stratégie :
    1. Construire le texte de base = title + abstract
    2. Si pdfUrl existe → télécharger et ajouter le texte du PDF
    3. Découper en chunks
    4. Calculer la similarité cosinus entre la query et chaque chunk
    5. Retourner le score MAX (le chunk le plus pertinent)

    Retourne:
        float entre 0.0 et 1.0
    """

    # ── Construire le texte de base ───────────────────────────────
    # On combine title + abstract — toujours disponibles
    base_text = f"{publication.title}. {publication.abstractText}"

    # Ajouter les keywords si disponibles — ils sont très informatifs
    if publication.keywords:
        base_text += f". Keywords: {publication.keywords}"

    # ── Tenter d'extraire le texte du PDF ─────────────────────────
    pdf_text = None
    if publication.pdfUrl:
        print(f"  📥 Téléchargement PDF pour : {publication.title[:50]}...")
        pdf_text = extract_text_from_pdf(publication.pdfUrl)

    # ── Assembler tout le texte disponible ────────────────────────
    if pdf_text:
        # On a le PDF complet → on l'utilise + le texte de base
        full_text = base_text + "\n\n" + pdf_text
        print(f"  📄 Texte total : {len(full_text)} caractères (avec PDF)")
    else:
        # Pas de PDF → on utilise uniquement title + abstract
        full_text = base_text
        print(f"  📝 Texte total : {len(full_text)} caractères (sans PDF)")

    # ── Découper en chunks ────────────────────────────────────────
    chunks = split_into_chunks(full_text, chunk_size=500, overlap=100)

    if not chunks:
        # Sécurité : si aucun chunk (texte vide), score = 0
        return 0.0

    print(f"  🔪 {len(chunks)} chunks créés")

    # ── Calculer les embeddings de tous les chunks d'un coup ──────
    # get_embeddings_batch() est plus rapide qu'une boucle
    chunk_embeddings = get_embeddings_batch(chunks)

    # ── Calculer la similarité cosinus ───────────────────────────
    # query_embedding shape  : (384,)      → on le reshape en (1, 384)
    # chunk_embeddings shape : (N, 384)    → N chunks, 384 dimensions
    # cosine_similarity retourne : (1, N)  → un score par chunk

    similarities = cosine_similarity(
        query_embedding.reshape(1, -1),   # (1, 384)
        chunk_embeddings                   # (N, 384)
    )
    # similarities[0] → tableau 1D de N scoresz

    # ── Garder le score MAX ───────────────────────────────────────
    # Si UN SEUL chunk est très pertinent → la publication l'est aussi
    max_score = float(np.max(similarities[0]))

    return max_score


# ─────────────────────────────────────────────────────────────────
# ÉTAPE 3 — Pipeline principale : query + publications → résultats
# ─────────────────────────────────────────────────────────────────

def semantic_search(
    query: str,
    publications: list[Publication]
) -> list[PublicationResult]:
    """
    Fonction principale appelée par l'endpoint POST /search.

    Paramètres:
        query        : texte de recherche de l'utilisateur
        publications : liste de publications à évaluer

    Retourne:
        Liste de PublicationResult triée par score décroissant
    """

    print(f"\n🔍 Recherche : '{query}'")
    print(f"📚 {len(publications)} publications à analyser\n")

    # ── Encoder la query UNE SEULE FOIS ──────────────────────────
    # Inutile de la recalculer pour chaque publication
    print("⚙️  Encodage de la query...")
    query_embedding = get_embedding(query)
    print("✅ Query encodée\n")

    # ── Calculer le score pour chaque publication ─────────────────
    results = []

    for i, publication in enumerate(publications):
        print(f"[{i+1}/{len(publications)}] {publication.title[:60]}...")

        score = compute_publication_score(query_embedding, publication)

        print(f"  ⭐ Score : {score:.4f}\n")

        results.append(PublicationResult(
            **publication.dict(),
            score=round(score, 4)   # Arrondir à 4 décimales
        ))

    # ── Trier par score décroissant ───────────────────────────────
    # Le meilleur résultat apparaît en premier
    results.sort(key=lambda r: r.score, reverse=True)

    print(f"✅ Recherche terminée — meilleur score : {results[0].score}")

    return results