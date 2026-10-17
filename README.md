# Multi-agente de pesquisa

Pipeline: **Planejador → Pesquisadores (paralelo) → Resumidor → Redator**.

## Estrutura
```
multi_agente/
├── main.py              # orquestrador (ponto de entrada)
├── config.py            # modelo, limites e leitura da chave
├── .env                 # SUA chave (não versionar)  <- criar a partir do .env.example
├── .env.example         # modelo do arquivo de chave
├── requirements.txt
├── agentes/             # um arquivo por agente
│   ├── base.py
│   ├── planejador.py
│   ├── pesquisador.py
│   ├── resumidor.py
│   └── redator.py
├── ferramentas/         # busca web e salvamento de arquivos
└── outputs/             # relatórios gerados (.md)
```

## Como usar
```
pip install -r requirements.txt
cp .env.example .env          # Windows: copy .env.example .env
# edite o .env e cole sua chave
python main.py "seu tema de pesquisa"
```

O modelo padrão é o mais barato (`claude-haiku-5-5`). Para trocar, defina
`MODELO` no `.env`. Para controlar custo, ajuste `N_SUBTOPICOS` e
`MAX_BUSCAS_POR_AGENTE` em `config.py`.
