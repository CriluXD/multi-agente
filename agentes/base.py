"""Função base: um 'agente' é uma chamada ao modelo com um papel (system prompt)."""

import anthropic

import config
from ferramentas.busca_web import ferramenta_busca

client = anthropic.Anthropic(api_key=config.API_KEY)


def rodar_agente(system: str, entrada: str, usar_busca: bool = False,
                 max_tokens: int = 4000) -> str:
    messages = [{"role": "user", "content": entrada}]
    kwargs = dict(model=config.MODELO, max_tokens=max_tokens, system=system)
    if usar_busca:
        kwargs["tools"] = [ferramenta_busca(config.MAX_BUSCAS_POR_AGENTE)]

    while True:
        resp = client.messages.create(messages=messages, **kwargs)
        # A busca web pode pausar turnos longos; reenviar continua de onde parou
        if resp.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": resp.content})
            continue
        return "".join(b.text for b in resp.content if b.type == "text").strip()
