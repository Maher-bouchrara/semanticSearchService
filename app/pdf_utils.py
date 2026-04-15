# pdf_utils.py — Télécharge et extrait le texte d'un PDF depuis une URL
# Tout se passe en mémoire — aucun fichier sauvegardé sur disque

import fitz          # PyMuPDF — pour lire les PDFs
import requests      # Pour télécharger le PDF depuis l'URL

print("ena pdf_utils.py")

def extract_text_from_pdf(url: str) -> str | None:
    """
    Télécharge un PDF depuis une URL et extrait tout son texte.

    Paramètres:
        url (str): L'URL du PDF (ex: "https://arxiv.org/pdf/2301.00001")

    Retourne:
        str  → le texte complet du PDF si succès
        None → si l'URL est invalide, le PDF inaccessible, ou une erreur survient
    """

    # ── Étape 1 : Télécharger le PDF ──────────────────────────────
    try:
        response = requests.get(
            url,
            timeout=15,   # Abandon si pas de réponse après 15 secondes
            headers={
                # Certains serveurs bloquent les requêtes sans User-Agent
                # On se fait passer pour un navigateur normal
                "User-Agent": "Mozilla/5.0"
            }
        )

        # Si le serveur répond avec une erreur (404, 403, 500...)
        # .raise_for_status() lève une exception automatiquement
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout — le PDF n'a pas répondu à temps : {url}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur téléchargement PDF ({url}) : {e}")
        return None

    # ── Étape 2 : Ouvrir le PDF depuis la mémoire ─────────────────
    try:
        # response.content = les bytes bruts du fichier PDF
        # fitz.open() peut lire depuis des bytes directement
        # "pdf" indique à fitz le format du fichier
        pdf_document = fitz.open(stream=response.content, filetype="pdf")

    except Exception as e:
        print(f"❌ Impossible d'ouvrir le PDF ({url}) : {e}")
        return None

    # ── Étape 3 : Extraire le texte de chaque page ────────────────
    full_text = ""

    for page_number in range(len(pdf_document)):
        # Accéder à une page (index commence à 0)
        page = pdf_document[page_number]

        # Extraire le texte de cette page
        # get_text() retourne une chaîne avec tout le texte de la page
        page_text = page.get_text()

        # Ajouter le texte de cette page au texte complet
        full_text += page_text

    # Fermer le document pour libérer la mémoire
    pdf_document.close()

    # ── Étape 4 : Vérifier qu'on a bien extrait quelque chose ─────
    # Certains PDFs sont des images scannées → pas de texte extractible
    if not full_text.strip():
        print(f"⚠️  PDF sans texte extractible (peut-être scanné) : {url}")
        return None

    print(f"✅ PDF extrait : {len(full_text)} caractères — {url}")
    return full_text