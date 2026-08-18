from pathlib import Path

from matcher.report import build_report

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def test_build_report_with_sample_data():
    resume_text = (SAMPLE_DIR / "sample_resume.txt").read_text(encoding="utf-8")
    job_text = (SAMPLE_DIR / "sample_job.txt").read_text(encoding="utf-8")

    report = build_report(resume_text, job_text, similarity_mode="tfidf")

    assert 0 <= report["overall_score"] <= 100
    assert report["similarity"]["method"] == "tfidf"
    assert "matched" in report["keywords"]
    assert "missing" in report["keywords"]
    assert len(report["suggestions"]) >= 1


def test_build_report_high_score_when_texts_are_the_same():
    text = "Python, SQL, trabalho em equipe e machine learning."
    report = build_report(text, text, similarity_mode="tfidf")
    assert report["overall_score"] >= 90
