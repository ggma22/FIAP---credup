# 🔧 backend/

Camada de **dados e regras de negócio** do CredUp. Independente do Streamlit — pode ser testada isoladamente, reutilizada em outros frontends (Flask, FastAPI, Jupyter).

## Módulos

| Arquivo | Responsabilidade |
|---|---|
| [`database.py`](database.py) | Conexão com Oracle Autonomous DB. Faz fallback automático para CSV se não houver credenciais. Única parte que conhece TLS, wallet, etc. |
| [`business_rules.py`](business_rules.py) | Funções puras: classificação de status, faixa de atraso, classificação de risco. Determinísticas e testáveis. |
| [`data_loader.py`](data_loader.py) | Pipeline orquestrador: extrai → tipa → enriquece → classifica. |
| [`kpis.py`](kpis.py) | Agregações executivas a partir do DataFrame enriquecido. |
| [`etl/setup_oracle.py`](etl/setup_oracle.py) | Script standalone que popula o Oracle a partir dos CSVs. |
| [`etl/schema.sql`](etl/schema.sql) | DDL puro, executável diretamente no SQL Worksheet do Database Actions. |

## Smoke test

Pra validar que o backend funciona sem subir Streamlit:

```bash
python -m backend.data_loader
```

Saída esperada:
```
Fonte: CSV
Boletos: 7,118  |  Auxiliar: 4,612  |  Enriquecido: 7,118
Emitido:  R$ 165.85 mi
Recebido: R$ 129.56 mi
Em aberto: R$ 4.02 mi
Inadimplência (R$): 2.43%
```

Com credenciais Oracle no `.env` da raiz, a fonte vira `ORACLE`.

## Princípios

- **Funções puras** quando possível — facilita teste
- **Sem `import streamlit`** — backend não conhece UI
- **Fallback gracioso** — Oracle indisponível → CSV automático, não quebra
- **Tratamento de erros visível** — printa `[CredUp]` no console, não esconde falhas
