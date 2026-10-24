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


def _salvar(tema: str, conteudo: str, prefixo: str, carimbo: str) -> Path:
    config.OUTPUT_DIR.mkdir(exist_ok=True)
    caminho = config.OUTPUT_DIR / f"{carimbo}_{prefixo}_{_slug(tema)}.md"
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


def novo_carimbo() -> str:
    return f"{datetime.now():%Y%m%d_%H%M%S}"


def salvar_relatorio(tema: str, conteudo: str, carimbo: str | None = None) -> Path:
    return _salvar(tema, conteudo, "relatorio", carimbo or novo_carimbo())


def salvar_revisao(tema: str, conteudo: str, carimbo: str | None = None) -> Path:
    return _salvar(tema, conteudo, "revisao", carimbo or novo_carimbo())
