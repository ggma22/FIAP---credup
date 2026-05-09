# 🏗️ Arquitetura — CredUp Sprint 4

Esta página descreve a **arquitetura técnica** da plataforma CredUp,
explicando como as camadas se comunicam e a justificativa de cada
decisão de design.

---

## 1. Visão de alto nível

```
┌──────────────────────────────────────────────────────────────────┐
│                       USUÁRIO (navegador)                        │
└────────────────────────────┬─────────────────────────────────────┘
                             │ HTTPS
┌────────────────────────────▼─────────────────────────────────────┐
│                   FRONTEND  (Streamlit + Plotly)                 │
│                                                                  │
│   Home.py  ← entry point (HOME)                         │
│   pages/                                                         │
│      1_Visao_Executiva.py    2_Analise_Temporal.py               │
│      3_Risco_e_Concentracao  4_Detalhamento.py                   │
│                                                                  │
│   frontend/                                                      │
│      theme.py        ← paleta + CSS                              │
│      components.py   ← hero, KPIs, badges                        │
│      filters.py      ← sidebar de filtros                        │
│      charts.py       ← funções Plotly reutilizáveis              │
└────────────────────────────┬─────────────────────────────────────┘
                             │ chamadas Python (in-process)
┌────────────────────────────▼─────────────────────────────────────┐
│                    BACKEND  (Python puro)                        │
│                                                                  │
│   data_loader.py  ← orquestra  →  kpis.py    (agregações)        │
│       │                       →  business_rules.py (status,risco)│
│       ▼                                                          │
│   database.py  ← decide a fonte                                  │
│       │                                                          │
│       ├─→ Oracle Autonomous DB (produção, online)                │
│       └─→ CSV local (fallback / modo demo)                       │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
         ┌─────────────┐         ┌─────────────┐
         │   ORACLE    │         │  backend/   │
         │ Autonomous  │         │   data/     │
         │     DB      │         │  *.csv      │
         └─────────────┘         └─────────────┘
```

---

## 2. Camadas

### 2.1 Backend (`backend/`)

Camada de dados e regras de negócio. **Não conhece Streamlit.**

| Módulo | Responsabilidade |
|---|---|
| `database.py` | Conexão com Oracle Autonomous DB. Faz fallback para CSV se não houver credenciais. Única parte que sabe de TLS, wallet, etc. |
| `business_rules.py` | Funções puras: classificação de status, faixa de atraso, classificação de risco. Determinísticas e testáveis. |
| `data_loader.py` | Pipeline orquestrador: extrai (via `database`) → tipa → enriquece → classifica (via `business_rules`). |
| `kpis.py` | Agregações executivas a partir do DataFrame enriquecido. |
| `etl/setup_oracle.py` | Script standalone que popula o Oracle a partir dos CSVs. |
| `etl/schema.sql` | DDL puro, executável diretamente no SQL Worksheet do Database Actions. |

**Vantagem da separação**: o backend pode ser testado em isolamento (rodar `python -m backend.data_loader` e ver os KPIs sem subir Streamlit), e poderia ser reaproveitado por outro frontend (Flask, FastAPI, Jupyter) sem alteração.

### 2.2 Frontend (`frontend/`)

Componentes Streamlit reutilizáveis. **Não conhece Oracle.** Recebe DataFrames prontos.

| Módulo | Responsabilidade |
|---|---|
| `theme.py` | Paleta de cores, mapas de cor para gráficos, e CSS injetado. Centraliza identidade visual. |
| `components.py` | Hero banner, badge da fonte, grades de KPIs, formatadores. |
| `filters.py` | Sidebar de filtros e função `aplicar_filtros(df, sel)`. |
| `charts.py` | Funções Plotly por tipo de visualização. Cada função recebe um DataFrame e devolve uma `Figure`. |

**Vantagem da separação**: trocar o tema da app é mexer em um só lugar (`theme.py`); adicionar um gráfico novo é 10 linhas em `charts.py` + 2 linhas na página que vai usar.

### 2.3 Páginas (`pages/`)

Streamlit usa convenção de pastas: arquivos em `pages/` viram páginas adicionais no menu lateral, automaticamente. O nome do arquivo (sem prefixo numérico) vira o título do menu.

| Arquivo | Conteúdo |
|---|---|
| `1_Visao_Executiva.py` | KPIs grandes, status da carteira, espécie, risco e atraso. |
| `2_Analise_Temporal.py` | Curvas mensais e tendência de atraso. |
| `3_Risco_e_Concentracao.py` | Top cedentes, UF, CNAE e matriz de risco. |
| `4_Detalhamento.py` | Tabela navegável + export CSV. |

**Cada página é independente** — pode ser carregada diretamente sem passar pela home, e cada uma chama `carregar_dados()` (resultado é cacheado entre páginas via `@st.cache_data`).

### 2.4 Entry point (`Home.py`)

A página HOME. Mostra KPIs principais e cards de navegação para as 4 páginas. É o arquivo apontado pelo Streamlit Cloud no deploy.

---

## 3. Fluxo de dados

```
        ┌───────────────────┐
        │   USUÁRIO ABRE    │
        │   /Visao_Executiva│
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │   page renderiza  │
        │   set_page_config │
        │   aplica_tema()   │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────┐
        │  carregar_dados() │ ← cache hit? ─→ retorna direto
        │     (cached)      │
        └─────────┬─────────┘
                  │ cache miss
        ┌─────────▼─────────┐
        │  database.        │
        │  buscar_dados_    │
        │  brutos()         │
        └─────────┬─────────┘
                  │
       ┌──────────┴──────────┐
       │ tem ORACLE_USER?    │
       └──────────┬──────────┘
              sim │ não
        ┌─────────▼─────────┐
        │  oracledb.connect │   ┌───────────────┐
        │  read_sql(...)    │   │  pd.read_csv  │
        └─────────┬─────────┘   └───────┬───────┘
                  │                     │
                  └──────────┬──────────┘
                             ▼
                   ┌───────────────────┐
                   │ tipar + derivar   │
                   │ status + risco    │
                   │ classificar       │
                   └─────────┬─────────┘
                             ▼
                   ┌───────────────────┐
                   │ DataFrame pronto  │
                   │ → frontend rendera│
                   └───────────────────┘
```

---

## 4. Persistência: Oracle Autonomous Database

### 4.1 Modelo lógico

```
┌─────────────────────┐         ┌─────────────────────┐
│ BASE_BOLETOS_FIAP   │         │ BASE_AUXILIAR_FIAP  │
├─────────────────────┤         ├─────────────────────┤
│ id_boleto      PK   │         │ id_cnpj         PK  │
│ id_pagador     FK ──┼────────►│ cd_cnae_prin        │
│ id_beneficiario     │         │ uf                  │
│ dt_emissao          │         │ sacado_liquidez_1m  │
│ dt_vencimento       │         │ score_quantidade_v2 │
│ dt_pagamento        │         │ media_atraso_dias   │
│ vlr_nominal         │         │ ...                 │
│ vlr_baixa           │         └─────────────────────┘
│ tipo_baixa          │
│ tipo_especie        │
└─────────────────────┘
```

### 4.2 Índices

Pensados para as queries mais frequentes do dashboard:

- `idx_bol_pagador` — JOIN com auxiliar (consulta mais comum)
- `idx_bol_dt_venc` — filtro temporal pelo sidebar
- `idx_bol_tipo_baixa` — agregação por status
- `idx_aux_uf`, `idx_aux_cnae` — agregações geográficas e setoriais

### 4.3 Segurança

- Usuário dedicado `credup_app` com permissão **apenas de leitura** nas 2 tabelas (princípio de menor privilégio).
- ADMIN só é usado pelo script de ingestão.
- Wallet com mTLS — todas as conexões usam TLS server-side.
- ACL configurado no Autonomous DB ("Allow secure access from everywhere") para permitir conexão do Streamlit Cloud.

---

## 5. Deployment

### Local

```
streamlit run Home.py
```

Lê `.env` na raiz, conecta no Oracle (ou cai pra CSV).

### Streamlit Community Cloud

- Repositório GitHub público com TODO o código + CSVs.
- Credenciais Oracle no painel "Secrets" do Streamlit Cloud (não no código).
- Wallet codificada em base64 nos secrets, decodificada em `/tmp` em runtime.

Detalhes em [`deploy_streamlit_cloud.md`](deploy_streamlit_cloud.md).

---

## 6. Decisões de design

| Decisão | Justificativa |
|---|---|
| **Streamlit multipage** (`pages/`) ao invés de `st.tabs` | Cada seção tem URL própria, suporte a navegação por menu, melhor experiência mobile. |
| **Backend modular puro** | Permite testes isolados, reuso em outros frontends, e separação clara de "lógica" vs "UI". |
| **Modo dual Oracle/CSV** | A banca consegue rodar local sem credencial; o app online usa o banco real. |
| **Usuário dedicado de leitura** | Princípio de menor privilégio — comprometer o app não compromete o banco. |
| **Cache do Streamlit (`@st.cache_data`)** | Carga de 7.118 linhas só uma vez por sessão; navegação entre páginas é instantânea. |
| **Plotly over Matplotlib** | Interatividade nativa (zoom, hover) que o usuário-gestor espera de um BI. |
| **DDL em arquivo `.sql` separado** | Documenta o schema de forma executável, independente do Python. |

---

## 7. Como rodar testes / validações

### Validar backend (sem subir Streamlit)

```bash
python -m backend.data_loader
```

Esperado:
```
Fonte: CSV
Boletos: 7,118  |  Auxiliar: 4,612  |  Enriquecido: 7,118
Emitido:  R$ 165.85 mi
Recebido: R$ 129.56 mi
Em aberto: R$ 4.02 mi
Inadimplência (R$): 2.43%
```

### Validar conexão Oracle

```bash
python -c "from backend.database import buscar_dados_brutos; bol, aux, fonte = buscar_dados_brutos(); print(f'Fonte: {fonte} | {len(bol):,} boletos')"
```

Esperado: `Fonte: oracle | 7,118 boletos` (ou `csv` se sem credenciais).
