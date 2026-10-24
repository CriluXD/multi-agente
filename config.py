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

# Haiku 5.5 "pensa" por padrão e os tokens de pensamento contam no max_tokens.
# Para manter barato e evitar respostas vazias: esforço baixo e pensamento desligado.
# Pode ser trocado no .env (low, medium ou high).
ESFORCO = os.getenv("ESFORCO", "low")
LIMITE_MAX_TOKENS = 20000  # teto ao reenviar após estourar max_tokens

N_SUBTOPICOS = 4          # pesquisadores rodando em paralelo
MAX_BUSCAS_POR_AGENTE = 3  # limite de buscas web por pesquisador (controla custo)
OUTPUT_DIR = BASE_DIR / "outputs"
DEBUG = os.getenv("DEBUG", "0") == "1"  # DEBUG=1 no .env mostra detalhes de cada agente
