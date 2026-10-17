"""Utilitários para salvar resultados na pasta outputs/."""

import re
import unicodedata
from datetime import datetime
from pathlib import Path

import config


def _slug(texto: str, limite: int = 50) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9]+", "_", texto).strip("_").lower()
    return texto[:limite] or "relatorio"


def salvar_relatorio(tema: str, conteudo: str) -> Path:
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    nome = f"{datetime.now():%Y%m%d_%H%M%S}_{_slug(tema)}.md"
    caminho = config.OUTPUT_DIR / nome
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho
