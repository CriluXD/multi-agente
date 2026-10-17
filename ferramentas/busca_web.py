"""Definição da ferramenta de busca web (executada pela própria API)."""


def ferramenta_busca(max_usos: int = 3) -> dict:
    return {"type": "web_search_20250305", "name": "web_search", "max_uses": max_usos}
