"""Função base: um 'agente' é uma chamada ao modelo com um papel (system prompt)."""

import anthropic

import config
from ferramentas.busca_web import ferramenta_busca

client = anthropic.Anthropic(api_key=config.API_KEY)


def _chamar(system: str, entrada: str, usar_busca: bool, max_tokens: int,
            esforco: str, pensar: bool):
    messages = [{"role": "user", "content": entrada}]
    kwargs = dict(
        model=config.MODELO,
        max_tokens=max_tokens,
        system=system,
        # output_config via extra_body funciona mesmo em versões antigas do SDK
        extra_body={"output_config": {"effort": esforco}},
    )
    if not pensar:
        # Haiku 5.5 pensa por padrão; desligar evita gastar max_tokens sem gerar texto
        kwargs["thinking"] = {"type": "disabled"}
    if usar_busca:
        kwargs["tools"] = [ferramenta_busca(config.MAX_BUSCAS_POR_AGENTE)]

    textos = []
    while True:
        resp = client.messages.create(messages=messages, **kwargs)
        textos += [b.text for b in resp.content if b.type == "text"]
        # A busca web pode pausar turnos longos; reenviar continua de onde parou
        if resp.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": resp.content})
            continue
        return "".join(textos).strip(), resp.stop_reason


def rodar_agente(system: str, entrada: str, usar_busca: bool = False,
                 max_tokens: int = 4000, nome: str = "agente",
                 esforco: str | None = None, pensar: bool = False) -> str:
    esforco = esforco or config.ESFORCO
    motivo = None
    for tentativa in (1, 2):
        texto, motivo = _chamar(system, entrada, usar_busca, max_tokens, esforco, pensar)
        if config.DEBUG:
            print(f"      [debug] {nome}: {len(texto)} caracteres, "
                  f"stop_reason={motivo}, max_tokens={max_tokens}, tentativa={tentativa}")
        if texto:
            if motivo == "max_tokens":
                print(f"      [aviso] {nome}: resposta cortada por limite de tokens")
            return texto
        if tentativa == 1:
            # Se estourou o limite sem texto, o pensamento consumiu tudo: dobra o limite
            if motivo == "max_tokens":
                max_tokens = min(max_tokens * 2, config.LIMITE_MAX_TOKENS)
            print(f"      [aviso] {nome}: resposta vazia (stop_reason={motivo}), "
                  f"tentando de novo com max_tokens={max_tokens}...")
    raise RuntimeError(
        f"O agente '{nome}' devolveu resposta vazia duas vezes (stop_reason={motivo}). "
        "Tente ESFORCO=low no .env ou aumente o max_tokens do agente."
    )
