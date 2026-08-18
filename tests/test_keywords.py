from pathlib import Path

from matcher.keywords import compare, find_skills

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def test_find_skills_detects_known_terms():
    text = "Tenho experiência com Python, Docker e SQL."
    skills = find_skills(text)
    assert "python" in skills
    assert "docker" in skills
    assert "sql" in skills


def test_find_skills_avoids_false_positive_substring():
    # "r" e "go" não devem "casar" dentro de outras palavras
    text = "Um amigo meu foi trabalhar comigo em um projeto."
    skills = find_skills(text)
    assert "r" not in skills  # não deve casar dentro de "trabalhar"
    assert "go" not in skills  # não deve casar dentro de "amigo"/"comigo"


def test_find_skills_matches_multiword_skill():
    text = "Precisamos de alguém com trabalho em equipe e machine learning."
    skills = find_skills(text)
    assert "trabalho em equipe" in skills
    assert "machine learning" in skills


def test_compare_with_sample_resume_and_job():
    resume_text = (SAMPLE_DIR / "sample_resume.txt").read_text(encoding="utf-8")
    job_text = (SAMPLE_DIR / "sample_job.txt").read_text(encoding="utf-8")

    result = compare(resume_text, job_text)

    assert "python" in result["matched"]
    assert "sql" in result["matched"]
    # a vaga pede docker e aws como diferencial, que não estão no currículo de exemplo
    assert "docker" in result["missing"]
    assert "aws" in result["missing"]
    assert 0.0 <= result["coverage"] <= 1.0


def test_compare_full_coverage_when_texts_identical():
    text = "Python, SQL e trabalho em equipe."
    result = compare(text, text)
    assert result["missing"] == []
    assert result["coverage"] == 1.0
