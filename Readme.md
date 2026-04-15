# Semantic Search API - Setup Guide

## 🐧 Linux Setup

### 1. Check Python and pip
```bash
python3 --version
pip3 --version
```

### 2. Install Python and pip (if needed)
```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

### 3. Navigate to your project folder
```bash
cd /path/to/Semantique
```

### 4. Create a virtual environment
```bash
python3 -m venv venv
```

### 5. Activate the virtual environment
```bash
source venv/bin/activate
```

### 6. Install dependencies
```bash
pip install -r requirements.txt
```

### 7. Run the API server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 🪟 Windows Setup

### 1. Check Python and pip
```cmd
python --version
pip --version
```

### 2. Install Python (if needed)
- Download from [python.org](https://www.python.org/downloads/)
- Run the installer and **check "Add Python to PATH"**
- Verify installation: `python --version`

### 3. Navigate to your project folder
```cmd
cd C:\path\to\Semantique
```

### 4. Create a virtual environment
```cmd
python -m venv venv
```

### 5. Activate the virtual environment
```cmd
venv\Scripts\activate
```

### 6. Install dependencies
```cmd
pip install -r requirements.txt
```

### 7. Run the API server
```cmd
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 🧪 Test the API

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
      },
      {
        "id": 4,
        "title": "LLM Fine-Tuning pour larabe Dialectal Tunisien",
        "abstractText": "Adaptation de LLaMA-3 et Mistral sur un corpus de 500K phrases.",
        "keywords": "LLM, NLP, arabe dialectal, fine-tuning",
        "pdfUrl": null
      }
    ]
  }'
```

---

## 📋 How It Works

```
POST /search { query, publications[] }
    ↓
main.py receives the request
    ↓
search.py: semantic_search()
    ↓
get_embedding(query) → query vector (384 dims)
    ↓
For each publication:
  ├── pdf_utils.py: extract_text_from_pdf()
  ├── split_into_chunks() → N chunks of 500 chars
  ├── get_embeddings_batch() → N vectors
  ├── cosine_similarity() → N scores
  └── max(scores) → 1 score per publication
    ↓
Sort results by score (descending)
    ↓
SearchResponse { results[] }
```