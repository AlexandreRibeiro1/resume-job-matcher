"""Extração e comparação de palavras-chave técnicas entre currículo e vaga."""
from __future__ import annotations

import re
from collections import Counter

# Dicionário de skills comuns em vagas de tecnologia (PT/EN misturado,
# como normalmente aparece em currículos e descrições de vaga no Brasil).
SKILLS: dict[str, list[str]] = {
    "linguagens": [
        "python", "javascript", "typescript", "java", "c++", "c#", "sql",
        "r", "go", "golang", "rust", "php", "kotlin", "swift", "html", "css",
    ],
    "frameworks_libs": [
        "react", "vue", "angular", "django", "flask", "fastapi", "node.js",
        "node", "spring", "express", "next.js", ".net", "pandas", "numpy",
        "scikit-learn", "pytorch", "tensorflow", "keras",
    ],
    "bancos_de_dados": [
        "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis",
        "oracle", "sql server", "firebase", "elasticsearch",
    ],
    "nuvem_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "jenkins",
        "terraform", "linux", "git", "github", "gitlab",
    ],
    "dados_e_ia": [
        "machine learning", "deep learning", "nlp", "llm", "data science",
        "etl", "power bi", "tableau", "excel", "spark", "airflow", "opencv",
    ],
    "metodologias": ["scrum", "agile", "ágil", "kanban", "devops", "tdd"],
    "soft_skills": [
        "comunicação", "trabalho em equipe", "liderança", "proatividade",
        "resolução de problemas", "organização", "colaboração",
    ],
}

ALL_SKILLS = sorted({skill for group in SKILLS.values() for skill in group})

_STOPWORDS = {
    # português
    "para", "com", "uma", "um", "que", "dos", "das", "por", "sua", "seu",
    "nos", "nas", "como", "mais", "ser", "está", "esta", "este", "isso",
    "sobre", "entre", "após", "ainda", "também", "quando", "onde", "pelo",
    "pela", "todo", "toda", "todos", "todas", "outro", "outra", "muito",
    "muita", "cada", "esse", "essa", "aos", "são", "ter", "seus", "suas",
    # inglês
    "the", "and", "for", "with", "you", "your", "are", "will", "have",
    "this", "that", "from", "our", "who", "job", "role", "years", "work",
    "team", "must", "able", "into", "using", "such", "than", "they",
}

_TOKEN_RE = re.compile(r"[a-zà-ú0-9\.\+\#]+", re.IGNORECASE)


def _normalize(text: str) -> str:
    return text.lower()


def _contains_skill(text_lower: str, skill: str) -> bool:
    pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
    return re.search(pattern, text_lower) is not None


def find_skills(text: str) -> set[str]:
    """Retorna o subconjunto de ALL_SKILLS presente no texto."""
    text_lower = _normalize(text)
    return {skill for skill in ALL_SKILLS if _contains_skill(text_lower, skill)}


def extract_generic_terms(text: str, exclude: set[str], top_n: int = 10, min_count: int = 2) -> list[str]:
    """Extrai termos frequentes fora do dicionário fixo de skills.

    Serve para capturar palavras específicas da vaga que não estão no
    dicionário (ex: nome de uma ferramenta interna ou tecnologia nova).
    """
    tokens = _TOKEN_RE.findall(text.lower())
    tokens = [t for t in tokens if len(t) >= 4 and t not in _STOPWORDS and t not in exclude]
    counts = Counter(tokens)
    common = [word for word, count in counts.most_common(30) if count >= min_count]
    return common[:top_n]


def compare(resume_text: str, job_text: str) -> dict:
    """Compara currículo e vaga, retornando skills batidas, faltando e termos extras."""
    job_skills = find_skills(job_text)
    resume_skills = find_skills(resume_text)

    matched = sorted(job_skills & resume_skills)
    missing = sorted(job_skills - resume_skills)
    extra_terms = extract_generic_terms(job_text, exclude=job_skills)

    coverage = len(matched) / len(job_skills) if job_skills else 1.0

    return {
        "job_skills": sorted(job_skills),
        "resume_skills": sorted(resume_skills),
        "matched": matched,
        "missing": missing,
        "extra_terms": extra_terms,
        "coverage": coverage,
    }
