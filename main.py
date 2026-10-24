"""
Orquestrador: Planejador -> Pesquisadores (paralelo) -> Resumidor -> Revisor -> Redator

Uso:
    python main.py "Impacto da IA generativa no mercado de trabalho brasileiro"
"""

import sys
from concurrent.futures import ThreadPoolExecutor

import config  # valida a chave logo no início
from agentes import planejar, pesquisar, resumir, revisar, redigir
from ferramentas import salvar_relatorio, salvar_revisao, novo_carimbo


def pesquisar_seguro(tema: str, subtopico: str) -> str | None:
    """Um pesquisador com falha não derruba os outros."""
    try:
        return pesquisar(tema, subtopico)
    except Exception as e:  # noqa: BLE001
        print(f"      [erro] pesquisa de '{subtopico}' falhou: {e}")
        return None


def exigir(texto: str, etapa: str) -> str:
    if not texto or not texto.strip():
        sys.exit(f"Erro: a etapa '{etapa}' retornou vazio. Rode com DEBUG=1 no "
                 ".env para ver detalhes. Nada foi enviado ao redator.")
    return texto


def imprimir_revisao(revisao) -> str:
    """Mostra a revisão no terminal e devolve o mesmo texto em Markdown."""
    texto = (
        "# Revisão do resumo\n\n"
        "## Erros encontrados no resumo (e correções)\n"
        f"{revisao.erros_resumo}\n\n"
        "## Problemas encontrados na pesquisa\n"
        f"{revisao.problemas_pesquisa}\n"
    )
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70 + "\n")
    return texto


def main(tema: str) -> None:
    carimbo = novo_carimbo()
    print(f"Modelo: {config.MODELO}")

    print(f"[1/5] Planejando subtópicos para: {tema}")
    subtopicos = planejar(tema)
    for s in subtopicos:
        print(f"      - {s}")

    print(f"[2/5] Pesquisando {len(subtopicos)} subtópicos em paralelo...")
    with ThreadPoolExecutor(max_workers=len(subtopicos)) as pool:
        resultados = list(pool.map(lambda s: pesquisar_seguro(tema, s), subtopicos))
    pesquisas = [r for r in resultados if r]
    if not pesquisas:
        sys.exit("Erro: nenhuma pesquisa retornou conteúdo.")
    if len(pesquisas) < len(subtopicos):
        print(f"      [aviso] {len(subtopicos) - len(pesquisas)} subtópico(s) sem resultado")

    print("[3/5] Resumindo...")
    resumo = exigir(resumir(tema, pesquisas), "resumidor")

    print("[4/5] Revisando o resumo contra a pesquisa...")
    revisao = revisar(tema, pesquisas, resumo)
    exigir(revisao.resumo_corrigido, "revisor")
    texto_revisao = imprimir_revisao(revisao)
    caminho_revisao = salvar_revisao(tema, texto_revisao, carimbo)

    print("[5/5] Escrevendo relatório com o resumo corrigido...")
    relatorio = redigir(tema, revisao.resumo_corrigido)
    caminho = salvar_relatorio(tema, relatorio, carimbo)

    print(f"Pronto!\n  Relatório: {caminho}\n  Revisão:   {caminho_revisao}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Uso: python main.py "seu tema de pesquisa"')
    main(" ".join(sys.argv[1:]))
