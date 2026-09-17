# 🧭 Verificador Currículo x Vaga

> **🇺🇸 In English:** a Streamlit app that compares a résumé (PDF or text) with
> a job description. It extracts text with `pdfplumber`, matches technical and
> soft skills against a curated dictionary (showing what matches and what is
> missing), and measures text similarity with TF-IDF + cosine similarity, or
> with multilingual sentence embeddings when `sentence-transformers` is
> installed. Both signals are combined into a 0–100% fit score with concrete
> suggestions on what to adjust before applying. Covered by 18 pytest tests,
> including false-positive cases in skill matching.

Ferramenta em Python que compara um currículo com a descrição de uma vaga e
mostra o quanto eles têm em comum — quais skills batem, quais estão faltando,
e um score geral de compatibilidade.

## A dor que isso resolve

Na hora de procurar estágio, é difícil saber se vale a pena aplicar pra uma
vaga ou o que ajustar no currículo antes de mandar. Este projeto nasceu dessa
necessidade: uma ferramenta rápida para checar a aderência entre currículo e
vaga *antes* de aplicar, com sugestões concretas do que destacar ou incluir.

## Como funciona

1. **Extração de texto** — lê o currículo em PDF ou texto puro (`pdfplumber`).
2. **Análise de skills** — compara currículo e vaga contra um dicionário de
   skills técnicas e comportamentais (linguagens, frameworks, bancos de
   dados, cloud/devops, dados/IA, metodologias, soft skills), apontando o
   que está presente nos dois e o que a vaga pede e falta no currículo.
3. **Similaridade de texto** — calcula o quão parecidos os dois textos são,
   usando **TF-IDF + similaridade de cosseno** (scikit-learn) por padrão. Se
   o pacote opcional `sentence-transformers` estiver instalado, usa
   **embeddings multilíngues** para uma comparação semântica (entende que
   "liderar equipe" e "liderança" são parecidos, por exemplo).
4. **Relatório final** — combina os dois sinais num score de 0 a 100% e gera
   sugestões práticas de ajuste.

## Rodando localmente

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
streamlit run app.py
```

Acesse [http://localhost:8501](http://localhost:8501) e cole (ou envie em
PDF) seu currículo e a descrição de uma vaga.

### Ativando o modo semântico (opcional)

```bash
pip install sentence-transformers
```

Com o pacote instalado, o app passa a oferecer o modo de comparação
semântica automaticamente — sem ele, tudo continua funcionando via TF-IDF.

## Rodando os testes

```bash
pip install -r requirements-dev.txt
pytest -v
```

18 testes cobrindo extração de PDF/texto, matching de skills (incluindo
casos de falso positivo, tipo "r" não casar dentro de "trabalho"),
similaridade e o relatório final.

## Estrutura do projeto

```
resume-job-matcher/
├── app.py                  # interface Streamlit
├── matcher/
│   ├── extractor.py        # extração de texto de PDF/txt
│   ├── keywords.py         # dicionário de skills e comparação
│   ├── similarity.py       # TF-IDF / embeddings + cosseno
│   └── report.py           # consolida tudo num relatório
├── tests/                  # suíte pytest
├── sample_data/            # currículo e vaga de exemplo para testar
├── requirements.txt
└── requirements-dev.txt
```

## Tecnologias

Python, Streamlit, scikit-learn (TF-IDF), pdfplumber, pytest e,
opcionalmente, sentence-transformers para embeddings semânticos.

## Limitações

O dicionário de skills é curado manualmente e não cobre tudo — o resultado é
um ponto de partida para revisar o currículo, não uma verdade absoluta (nem
substitui um ATS real usado por empresas).

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.
