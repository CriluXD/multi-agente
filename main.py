"""
Orquestrador: Planejador -> Pesquisadores (paralelo) -> Resumidor -> Redator

Uso:
    python main.py "Impacto da IA generativa no mercado de trabalho brasileiro"
"""

import sys
from concurrent.futures import ThreadPoolExecutor

import config  # valida a chave logo no início
from agentes import planejar, pesquisar, resumir, redigir
from ferramentas import salvar_relatorio


def main(tema: str) -> None:
    print(f"Modelo: {config.MODELO}")
    print(f"[1/4] Planejando subtópicos para: {tema}")
    subtopicos = planejar(tema)
    for s in subtopicos:
        print(f"      - {s}")

    print(f"[2/4] Pesquisando {len(subtopicos)} subtópicos em paralelo...")
    with ThreadPoolExecutor(max_workers=len(subtopicos)) as pool:
        pesquisas = list(pool.map(lambda s: pesquisar(tema, s), subtopicos))

    print("[3/4] Resumindo...")
    resumo = resumir(tema, pesquisas)

    print("[4/4] Escrevendo relatório...")
    relatorio = redigir(tema, resumo)

    caminho = salvar_relatorio(tema, relatorio)
    print(f"Pronto! Relatório salvo em {caminho}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Uso: python main.py "seu tema de pesquisa"')
    main(" ".join(sys.argv[1:]))
