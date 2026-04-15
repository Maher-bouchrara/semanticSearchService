# test_pdf.py — Script de test rapide (à supprimer après)

from pdf_utils import extract_text_from_pdf

# Test 1 — PDF qui existe (publication 1)
print("=== Test 1 : PDF valide ===")
text = extract_text_from_pdf("https://arxiv.org/pdf/2301.00001")
if text:
    print(f"Longueur du texte : {len(text)} caractères")
    print(f"Début du texte :\n{text[:300]}")
else:
    print("Aucun texte extrait")

print("\n=== Test 2 : URL invalide ===")
text2 = extract_text_from_pdf("https://url-qui-nexiste-pas.com/fake.pdf")
print(f"Résultat : {text2}")  # Doit afficher None

print("\n=== Test 3 : pdfUrl est None ===")
# Simule ce qu'on fera dans search.py
pdf_url = None
if pdf_url:
    text3 = extract_text_from_pdf(pdf_url)
else:
    text3 = None
    print("pdfUrl est None → on saute le téléchargement")
print(f"Résultat : {text3}")