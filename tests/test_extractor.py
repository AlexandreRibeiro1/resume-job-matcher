import io
from pathlib import Path

import pytest

from matcher.extractor import ExtractionError, extract_text

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def test_extract_text_from_txt_path():
    text = extract_text(SAMPLE_DIR / "sample_resume.txt")
    assert "Python" in text
    assert len(text) > 50


def test_extract_text_missing_file():
    with pytest.raises(ExtractionError):
        extract_text(SAMPLE_DIR / "nao_existe.txt")


def test_extract_text_unsupported_format(tmp_path):
    bad_file = tmp_path / "curriculo.docx"
    bad_file.write_text("conteúdo qualquer")
    with pytest.raises(ExtractionError):
        extract_text(bad_file)


class FakeUpload(io.BytesIO):
    """Simula um arquivo do st.file_uploader (tem .name e .read())."""

    def __init__(self, data: bytes, name: str):
        super().__init__(data)
        self.name = name


def test_extract_text_from_memory_txt():
    upload = FakeUpload("Currículo com acentuação: é, ç, ã".encode("utf-8"), "curriculo.txt")
    text = extract_text(upload)
    assert "acentuação" in text


def test_extract_text_empty_file_raises(tmp_path):
    empty = tmp_path / "vazio.txt"
    empty.write_text("   ")
    with pytest.raises(ExtractionError):
        extract_text(empty)


def test_extract_text_from_pdf(tmp_path):
    from reportlab.pdfgen import canvas

    pdf_path = tmp_path / "curriculo.pdf"
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, "Experiencia com Python, SQL e Docker.")
    c.save()

    text = extract_text(pdf_path)
    assert "Python" in text
    assert "Docker" in text
