"""Agente 1: quebra o tema em subtópicos."""

import json

import config
from .base import rodar_agente

SYSTEM = (
    "Você é um planejador de pesquisa. Divida o tema em subtópicos "
    "complementares e não sobrepostos. Responda SOMENTE com um array JSON "
    "de strings, sem markdown e sem texto extra."
)


def planejar(tema: str) -> list[str]:
    saida = rodar_agente(SYSTEM, f"Tema: {tema}\nGere {config.N_SUBTOPICOS} subtópicos.")
    saida = saida.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(saida)[: config.N_SUBTOPICOS]
    except json.JSONDecodeError:
        return [tema]  # fallback: pesquisa o tema inteiro
