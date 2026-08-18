"""Consolida similaridade e análise de keywords em um relatório único."""
from __future__ import annotations

from . import keywords, similarity


def build_report(resume_text: str, job_text: str, similarity_mode: str = "auto") -> dict:
    kw = keywords.compare(resume_text, job_text)
    sim = similarity.compute_similarity(resume_text, job_text, mode=similarity_mode)

    overall = 0.5 * sim["score"] + 0.5 * kw["coverage"]
    overall_pct = round(overall * 100)

    suggestions: list[str] = []

    if kw["missing"]:
        top_missing = kw["missing"][:5]
        suggestions.append(
            "Considere adicionar ou destacar experiência com: " + ", ".join(top_missing) + "."
        )

    if kw["extra_terms"]:
        suggestions.append(
            "A vaga também repete termos fora do dicionário padrão de skills: "
            + ", ".join(kw["extra_terms"][:5])
            + ". Vale conferir se algum deles se aplica ao seu currículo."
        )

    if overall_pct >= 75:
        suggestions.append("Boa aderência: seu currículo já cobre a maior parte do que a vaga pede.")
    elif overall_pct >= 45:
        suggestions.append(
            "Aderência mediana: ajustar algumas palavras-chave pode aumentar bastante a compatibilidade."
        )
    else:
        suggestions.append(
            "Aderência baixa: essa vaga pode pedir um perfil bem diferente do que o currículo mostra hoje."
        )

    return {
        "overall_score": overall_pct,
        "similarity": sim,
        "keywords": kw,
        "suggestions": suggestions,
    }
