"""Configurações centrais do projeto. A chave vem do arquivo .env."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY or "coloque-sua-chave" in API_KEY:
    sys.exit(
        "Chave não encontrada. Copie .env.example para .env e preencha "
        "ANTHROPIC_API_KEY."
    )

# Modelo mais barato da família (Haiku). Pode ser trocado no .env.
MODELO = os.getenv("MODELO", "claude-haiku-5-5")

N_SUBTOPICOS = 4          # pesquisadores rodando em paralelo
MAX_BUSCAS_POR_AGENTE = 3  # limite de buscas web por pesquisador (controla custo)
OUTPUT_DIR = BASE_DIR / "outputs"
