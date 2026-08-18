"""Score de similaridade semântica entre currículo e vaga.

Usa TF-IDF + similaridade de cosseno como método padrão (rápido, sem
downloads). Se o pacote opcional `sentence-transformers` estiver instalado,
usa embeddings multilíngues para uma comparação mais semântica (entende
sinônimos, não só palavras idênticas).
"""
from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
_embedder = None


def semantic_available() -> bool:
    try:
        import sentence_transformers  # noqa: F401
    except ImportError:
        return False
    return True


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer

        _embedder = SentenceTransformer(_EMBEDDING_MODEL_NAME)
    return _embedder


def _clamp_unit(score: float) -> float:
    """Corrige imprecisão de ponto flutuante (ex: 1.0000000000000002)."""
    return max(0.0, min(1.0, score))


def tfidf_similarity(resume_text: str, job_text: str) -> float:
    try:
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform([resume_text, job_text])
    except ValueError:
        return 0.0
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return _clamp_unit(float(score))


def semantic_similarity(resume_text: str, job_text: str) -> float:
    model = _get_embedder()
    embeddings = model.encode([resume_text, job_text])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return _clamp_unit(float(score))


def compute_similarity(resume_text: str, job_text: str, mode: str = "auto") -> dict:
    """Calcula a similaridade. `mode`: "tfidf", "semantic" ou "auto".

    "auto" usa embeddings semânticos se disponíveis, caindo para TF-IDF
    automaticamente caso contrário (ou em caso de qualquer erro no download
    do modelo, para o app nunca quebrar por falta de internet).
    """
    if mode in ("semantic", "auto") and semantic_available():
        try:
            score = semantic_similarity(resume_text, job_text)
            return {"score": score, "method": "semantic"}
        except Exception:
            if mode == "semantic":
                raise

    score = tfidf_similarity(resume_text, job_text)
    return {"score": score, "method": "tfidf"}
