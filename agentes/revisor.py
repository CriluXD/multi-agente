"""Agente 3.5: revisa o resumo contra a pesquisa, corrige e lista o que estava errado."""

from dataclasses import dataclass

from .base import rodar_agente

M_RESUMO = "=== RESUMO CORRIGIDO ==="
M_ERROS_RESUMO = "=== ERROS NO RESUMO ==="
M_ERROS_PESQUISA = "=== PROBLEMAS NA PESQUISA ==="

SYSTEM = f"""Você é um revisor crítico e rigoroso. Receberá a PESQUISA BRUTA feita
por pesquisadores e o RESUMO escrito por um analista. Sua tarefa:

1. Comparar o resumo com a pesquisa bruta e encontrar erros no resumo: números
   ou datas alterados, afirmações sem respaldo na pesquisa, distorções,
   omissões importantes e fontes (URLs) perdidas ou trocadas.
2. Apontar problemas na própria pesquisa: contradições entre subtópicos,
   afirmações sem URL de fonte, dados suspeitos ou desatualizados, fontes fracas.
3. Escrever o resumo corrigido, mantendo as URLs das fontes.

Responda EXATAMENTE neste formato, com estes três marcadores em linhas próprias:

{M_RESUMO}
(resumo completo já corrigido)

{M_ERROS_RESUMO}
(lista em tópicos; cada item: o que estava errado -> como foi corrigido.
Se não houver erros, escreva "Nenhum erro encontrado.")

{M_ERROS_PESQUISA}
(lista em tópicos; cada item: o problema e em qual subtópico aparece.
Se não houver, escreva "Nenhum problema encontrado.")
"""


@dataclass
class Revisao:
    resumo_corrigido: str
    erros_resumo: str
    problemas_pesquisa: str


def _extrair(texto: str, inicio: str, fim: str | None) -> str:
    if inicio not in texto:
        return ""
    parte = texto.split(inicio, 1)[1]
    if fim and fim in parte:
        parte = parte.split(fim, 1)[0]
    return parte.strip()


def interpretar(saida: str) -> Revisao:
    return Revisao(
        resumo_corrigido=_extrair(saida, M_RESUMO, M_ERROS_RESUMO),
        erros_resumo=_extrair(saida, M_ERROS_RESUMO, M_ERROS_PESQUISA),
        problemas_pesquisa=_extrair(saida, M_ERROS_PESQUISA, None),
    )


def revisar(tema: str, pesquisas: list[str], resumo: str) -> Revisao:
    if not resumo.strip():
        raise ValueError("O resumo recebido pelo revisor está vazio.")
    entrada = (
        f"Tema: {tema}\n\n"
        "## PESQUISA BRUTA\n" + "\n\n".join(pesquisas) + "\n\n"
        f"## RESUMO A REVISAR\n{resumo}"
    )
    # Revisão é a tarefa mais exigente: libera o pensamento (esforço médio) e
    # dá folga de tokens, já que o pensamento conta no max_tokens.
    saida = rodar_agente(SYSTEM, entrada, max_tokens=16000, nome="revisor",
                         esforco="medium", pensar=True)
    revisao = interpretar(saida)
    if not revisao.resumo_corrigido:
        # Fallback: se o modelo não seguiu o formato, mantém o resumo original
        revisao.resumo_corrigido = resumo
        revisao.erros_resumo = "(Não foi possível interpretar a revisão.)\n\n" + saida
    return revisao
