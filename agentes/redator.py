"""Agente 4: escreve o relatório final em Markdown."""

from .base import rodar_agente

SYSTEM = (
    "Você é um redator de relatórios profissionais em português do Brasil. "
    "Escreva em Markdown com: título, resumo executivo, seções por tema, "
    "conclusões, limitações e uma seção 'Fontes' com as URLs. "
    "Use apenas informações presentes no resumo recebido."
)


def redigir(tema: str, resumo: str) -> str:
    return rodar_agente(SYSTEM, f"Tema: {tema}\n\nResumo:\n{resumo}", max_tokens=6000)
