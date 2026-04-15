# embedding_utils.py — Charge le modèle et convertit du texte en vecteurs

from sentence_transformers import SentenceTransformer
import numpy as np

# ── Chargement du modèle ──────────────────────────────────────────
# On charge le modèle UNE SEULE FOIS au démarrage de l'app
# (pas à chaque requête — ce serait très lent)
# La première fois : téléchargement ~90MB
# Les fois suivantes : chargement depuis le cache local
print("ena embedding_utils.py")
print("⏳ Chargement du modèle d'embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Modèle chargé !")


def get_embedding(text: str) -> np.ndarray:
    """
    Convertit un texte en vecteur numérique (embedding).

    Paramètres:
        text (str): N'importe quel texte

    Retourne:
        np.ndarray: Un tableau de 384 nombres flottants
    """
    # encode() fait tout le travail :
    # tokenisation → passage dans le réseau de neurones → vecteur
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding


def get_embeddings_batch(texts: list[str]) -> np.ndarray:
    """
    Convertit une LISTE de textes en vecteurs d'un seul coup.
    Beaucoup plus rapide que d'appeler get_embedding() en boucle.

    Paramètres:
        texts (list[str]): Liste de textes à encoder

    Retourne:
        np.ndarray: Tableau 2D — une ligne par texte, 384 colonnes
    """
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings