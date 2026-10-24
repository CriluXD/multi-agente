"""Agente 3: consolida as pesquisas e elimina redundâncias."""

from .base import rodar_agente

SYSTEM = (
    "Você é um analista. Consolide as pesquisas abaixo em um resumo "
    "objetivo: destaque os pontos principais, aponte contradições entre "
    "fontes e remova repetições. Preserve as URLs das fontes."
)


def resumir(tema: str, pesquisas: list[str]) -> str:
    return rodar_agente(SYSTEM, f"Tema: {tema}\n\n" + "\n\n".join(pesquisas),
                        nome="resumidor", max_tokens=6000)
