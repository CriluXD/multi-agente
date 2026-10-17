"""Agente 2: pesquisa na web e devolve achados com fontes."""

from .base import rodar_agente

SYSTEM = (
    "Você é um pesquisador rigoroso. Use a busca na web para encontrar "
    "informações atuais e confiáveis. Devolva achados em tópicos curtos, "
    "com dados concretos (números, datas, nomes) e a URL da fonte de cada "
    "afirmação. Não invente nada que não tenha encontrado."
)


def pesquisar(tema: str, subtopico: str) -> str:
    entrada = f"Tema geral: {tema}\nSubtópico a pesquisar: {subtopico}"
    return f"### {subtopico}\n" + rodar_agente(SYSTEM, entrada, usar_busca=True)
