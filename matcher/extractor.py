"""Extração de texto de currículos em PDF ou texto puro."""
from __future__ import annotations

import io
from pathlib import Path
from typing import Union

import pdfplumber

FileLike = Union[str, Path, "io.IOBase"]


class ExtractionError(Exception):
    """Levantado quando não é possível extrair texto do arquivo."""


def _read_pdf(stream_or_path) -> str:
    pages_text = []
    with pdfplumber.open(stream_or_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages_text.append(text)
    return "\n".join(pages_text)


def extract_text(source: FileLike) -> str:
    """Extrai texto de um caminho (str/Path) ou de um arquivo em memória.

    Aceita .pdf e .txt. Para arquivos em memória (ex: upload do Streamlit),
    o objeto precisa ter os atributos `.name` e `.read()`.
    """
    # Caminho em disco
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise ExtractionError(f"Arquivo não encontrado: {path}")
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            text = _read_pdf(path)
        elif suffix in (".txt", ".md"):
            text = path.read_text(encoding="utf-8", errors="ignore")
        else:
            raise ExtractionError(f"Formato não suportado: {suffix}")

    # Arquivo em memória (ex: st.file_uploader)
    else:
        name = getattr(source, "name", "")
        suffix = Path(name).suffix.lower()
        raw = source.read()
        if suffix == ".pdf":
            text = _read_pdf(io.BytesIO(raw))
        elif suffix in (".txt", ".md") or suffix == "":
            text = raw.decode("utf-8", errors="ignore") if isinstance(raw, bytes) else raw
        else:
            raise ExtractionError(f"Formato não suportado: {suffix}")

    text = text.strip()
    if not text:
        raise ExtractionError(
            "Não foi possível extrair texto do arquivo (pode ser um PDF escaneado/imagem)."
        )
    return text
