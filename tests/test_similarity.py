from matcher.similarity import compute_similarity, tfidf_similarity


def test_tfidf_similarity_identical_texts_is_high():
    text = "Python, SQL, pandas e machine learning para análise de dados."
    score = tfidf_similarity(text, text)
    assert 0.99 <= score <= 1.0


def test_tfidf_similarity_unrelated_texts_is_lower():
    resume = "Cozinheiro com experiência em confeitaria e panificação."
    job = "Vaga para desenvolvedor Python com experiência em Django e APIs REST."
    score = tfidf_similarity(resume, job)
    assert 0.0 <= score < 0.3


def test_tfidf_similarity_related_texts_is_moderate():
    resume = "Desenvolvedor com experiência em Python e SQL."
    job = "Vaga para desenvolvedor Python, com conhecimento em SQL e APIs."
    score = tfidf_similarity(resume, job)
    assert score > 0.3


def test_compute_similarity_forced_tfidf_mode():
    result = compute_similarity("Python e SQL", "Python e SQL", mode="tfidf")
    assert result["method"] == "tfidf"
    assert 0.0 <= result["score"] <= 1.0


def test_tfidf_similarity_handles_empty_text_gracefully():
    score = tfidf_similarity("", "")
    assert score == 0.0
