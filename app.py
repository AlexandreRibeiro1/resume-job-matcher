"""Verificador de compatibilidade currículo x vaga (Streamlit)."""
from __future__ import annotations

import streamlit as st

from matcher.extractor import ExtractionError, extract_text
from matcher.report import build_report
from matcher.similarity import semantic_available

st.set_page_config(page_title="Currículo x Vaga", page_icon="🧭", layout="centered")

st.title("🧭 Verificador Currículo x Vaga")
st.caption(
    "Compare seu currículo com a descrição de uma vaga e descubra o que ajustar "
    "antes de aplicar. Tudo roda localmente, nenhum arquivo é enviado a terceiros."
)

with st.sidebar:
    st.header("Configurações")
    if semantic_available():
        mode_label = st.radio(
            "Método de comparação",
            ["Automático (semântico)", "TF-IDF (palavra a palavra)"],
            help=(
                "O modo semântico usa embeddings e entende sinônimos "
                "(ex: 'liderar' ~ 'liderança'). O TF-IDF compara termos exatos."
            ),
        )
        similarity_mode = "auto" if mode_label.startswith("Automático") else "tfidf"
    else:
        similarity_mode = "tfidf"
        st.info(
            "Modo semântico desativado — instale `sentence-transformers` para "
            "comparações que entendem sinônimos. Usando TF-IDF por padrão."
        )

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Seu currículo")
    resume_file = st.file_uploader("Envie um PDF ou .txt", type=["pdf", "txt"], key="resume_file")
    resume_text_input = st.text_area("...ou cole o texto aqui", height=200, key="resume_text")

with col2:
    st.subheader("💼 Descrição da vaga")
    job_text_input = st.text_area("Cole a descrição da vaga aqui", height=280, key="job_text")

analyze = st.button("Analisar compatibilidade", type="primary", use_container_width=True)

if analyze:
    resume_text = ""
    try:
        if resume_file is not None:
            resume_text = extract_text(resume_file)
        elif resume_text_input.strip():
            resume_text = resume_text_input.strip()
    except ExtractionError as exc:
        st.error(f"Erro ao ler o currículo: {exc}")

    job_text = job_text_input.strip()

    if not resume_text:
        st.warning("Envie um arquivo ou cole o texto do seu currículo.")
    elif not job_text:
        st.warning("Cole a descrição da vaga.")
    else:
        report = build_report(resume_text, job_text, similarity_mode=similarity_mode)

        st.divider()
        score = report["overall_score"]
        st.subheader("Resultado")

        score_col, method_col = st.columns([1, 1])
        with score_col:
            st.metric("Compatibilidade geral", f"{score}%")
            st.progress(min(max(score, 0), 100) / 100)
        with method_col:
            method = report["similarity"]["method"]
            st.metric("Método usado", "Semântico" if method == "semantic" else "TF-IDF")
            coverage_pct = round(report["keywords"]["coverage"] * 100)
            st.metric("Cobertura de skills da vaga", f"{coverage_pct}%")

        kw = report["keywords"]

        st.markdown("#### ✅ Skills em comum")
        if kw["matched"]:
            st.markdown(" ".join(f"`{s}`" for s in kw["matched"]))
        else:
            st.caption("Nenhuma skill do dicionário padrão em comum foi encontrada.")

        st.markdown("#### ⚠️ Skills da vaga que não aparecem no currículo")
        if kw["missing"]:
            st.markdown(" ".join(f"`{s}`" for s in kw["missing"]))
        else:
            st.caption("Nenhuma — seu currículo cobre todas as skills reconhecidas da vaga.")

        if kw["extra_terms"]:
            st.markdown("#### 🔎 Outros termos frequentes na vaga")
            st.caption("Fora do dicionário padrão, mas repetidos — vale conferir.")
            st.markdown(" ".join(f"`{s}`" for s in kw["extra_terms"]))

        st.markdown("#### 💡 Sugestões")
        for suggestion in report["suggestions"]:
            st.markdown(f"- {suggestion}")

st.divider()
with st.expander("Como funciona?"):
    st.markdown(
        """
        1. O texto do currículo e da vaga é comparado por **similaridade de texto**
           (TF-IDF + cosseno, ou embeddings semânticos se disponíveis).
        2. Um dicionário de **skills técnicas e comportamentais** comuns em vagas
           de tecnologia é usado para achar o que a vaga pede e o que falta no currículo.
        3. Os dois sinais são combinados num **score geral de 0 a 100%**.

        O dicionário de skills é limitado e pode não cobrir tudo — use o resultado
        como um ponto de partida, não como verdade absoluta.
        """
    )
