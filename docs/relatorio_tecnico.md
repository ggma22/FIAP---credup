# 📋 Relatório Técnico — CredUp Sprint 4

**Equipe**: Giovanna Marotta · Adelaine Freire · Douglas Cavalcanti · Tiago Sgroglia · Victor de Aguiar
**Disciplina**: 1TSCP · Challenge FIAP 2025
**Versão**: 1.0 (entrega final)

---

## 1. Objetivo técnico

Construir uma plataforma analítica que combine dados transacionais de boletos B2B com indicadores de risco de crédito por CNPJ, oferecendo visualização interativa, persistência em banco relacional e classificação automática de risco.

---

## 2. Modelagem de dados

### 2.1 Modelo lógico

```
┌─────────────────────┐         ┌─────────────────────┐
│   CREDUP_BOLETOS    │         │   CREDUP_AUXILIAR   │
├─────────────────────┤         ├─────────────────────┤
│ id_boleto       PK  │         │ id_cnpj         PK  │
│ id_pagador      FK ─┼────────►│ cd_cnae_prin        │
│ id_beneficiario FK ─┼─ ┐      │ uf                  │
│ dt_emissao          │  │      │ sacado_liquidez_1m  │
│ dt_vencimento       │  │      │ cedente_liquidez_1m │
│ dt_pagamento        │  │      │ score_materialidade │
│ vlr_nominal         │  │      │ media_atraso_dias   │
│ vlr_baixa           │  │      │ score_quantidade_v2 │
│ tipo_baixa          │  │      │ ...                 │
│ tipo_especie        │  │      └─────────────────────┘
└─────────────────────┘  │              ▲
                         └──────────────┘
                          (cedente = beneficiário)
```

**Modelo escolhido**: relacional clássico, em forma normalizada. A tabela auxiliar serve simultaneamente como dimensão de **sacado** (via `id_pagador`) e dimensão de **cedente** (via `id_beneficiario`), pois 100% dos CNPJs aparecem em ambas as posições no dataset.

### 2.2 DDL (Oracle)

```sql
CREATE TABLE CREDUP_BOLETOS (
    id_boleto         VARCHAR2(128) NOT NULL,
    id_pagador        VARCHAR2(128) NOT NULL,
    id_beneficiario   VARCHAR2(128) NOT NULL,
    dt_emissao        DATE,
    dt_vencimento     DATE,
    dt_pagamento      DATE,
    vlr_nominal       NUMBER(18,2),
    vlr_baixa         NUMBER(18,2),
    tipo_baixa        VARCHAR2(120),
    tipo_especie      VARCHAR2(80),
    CONSTRAINT pk_credup_boletos PRIMARY KEY (id_boleto)
);

CREATE TABLE CREDUP_AUXILIAR (
    id_cnpj                              VARCHAR2(128) NOT NULL,
    cd_cnae_prin                         NUMBER(10),
    uf                                   VARCHAR2(2),
    sacado_indice_liquidez_1m            NUMBER(10,6),
    cedente_indice_liquidez_1m           NUMBER(10,6),
    score_materialidade_evolucao         NUMBER(10,2),
    media_atraso_dias                    NUMBER(10,4),
    indicador_liquidez_quantitativo_3m   NUMBER(10,4),
    share_vl_inad_pag_bol_6_a_15d        NUMBER(10,6),
    score_quantidade_v2                  NUMBER(10,2),
    score_materialidade_v2               NUMBER(10,2),
    CONSTRAINT pk_credup_auxiliar PRIMARY KEY (id_cnpj)
);
```

### 2.3 Índices

```sql
CREATE INDEX idx_bol_pagador      ON CREDUP_BOLETOS(id_pagador);
CREATE INDEX idx_bol_beneficiario ON CREDUP_BOLETOS(id_beneficiario);
CREATE INDEX idx_bol_dt_venc      ON CREDUP_BOLETOS(dt_vencimento);
CREATE INDEX idx_bol_tipo_baixa   ON CREDUP_BOLETOS(tipo_baixa);
CREATE INDEX idx_aux_uf           ON CREDUP_AUXILIAR(uf);
CREATE INDEX idx_aux_cnae         ON CREDUP_AUXILIAR(cd_cnae_prin);
```

**Justificativa**:
- `idx_bol_pagador` e `idx_bol_beneficiario`: aceleram o JOIN com a auxiliar (consulta mais frequente do dashboard).
- `idx_bol_dt_venc`: o filtro de período é o mais usado no dashboard.
- `idx_bol_tipo_baixa`: usado em dashboards de status e classificações de risco.
- `idx_aux_uf` e `idx_aux_cnae`: agregações geográficas e setoriais.

---

## 3. Pipeline de ingestão

### 3.1 Fluxo

```
CSV files
    │
    ▼
pandas.read_csv()
    │
    ▼
Conversão de tipos (datetime, numeric)
    │
    ▼
oracledb.connect() com mTLS (Wallet)
    │
    ▼
TRUNCATE → cursor.executemany() em lote
    │
    ▼
COMMIT + criação de índices
    │
    ▼
Smoke test (COUNT + SUM)
```

### 3.2 Tratamentos aplicados

| Operação | Implementação |
|---|---|
| Conversão de datas | `pd.to_datetime(errors='coerce')` |
| Tratamento de NaN/NaT | conversão para `None` antes do INSERT |
| Bulk insert | `cursor.executemany(sql, rows, batcherrors=True)` — performance |
| Captura de erros | `cursor.getbatcherrors()` — mostra erros sem abortar |
| Idempotência | `TRUNCATE` antes de inserir; flag `--recreate` para DROP |

### 3.3 Performance

Numa máquina de desenvolvimento típica (Oracle Autonomous Free Tier · DSN `_medium`):
- **Setup completo**: ~25 segundos
- **Insert de 7.118 boletos**: ~3 segundos
- **Insert de 4.612 auxiliares**: ~2 segundos
- **Criação de índices**: ~5 segundos

---

## 4. Algoritmos de análise

### 4.1 Classificação de risco por boleto

Função `_classifica_risco(row)` em `data_processing.py`. Implementa um **scorecard determinístico de 3 níveis**:

```python
def _classifica_risco(row) -> str:
    if row["status_negocio"] in {"Em aberto", "Protesto", "Vencido sem pagamento"}:
        return "Alto"

    liq = row.get("sacado_indice_liquidez_1m")
    sc  = row.get("score_quantidade_v2")
    da  = row.get("dias_atraso")

    if (pd.notna(liq) and liq < 0.5) or \
       (pd.notna(sc) and sc < 800) or \
       (pd.notna(da) and da > 30):
        return "Alto"

    if (pd.notna(liq) and liq < 0.7) or \
       (pd.notna(sc) and sc < 900) or \
       (pd.notna(da) and da > 7):
        return "Médio"

    return "Baixo"
```

**Justificativa dos limites**:
- `liquidez < 0,5`: percentil ~5 da distribuição da base — empresas de baixa liquidez declarada.
- `score < 800`: percentil ~20 do score quantitativo — sinal de comportamento de risco.
- `atraso > 30`: limite contratual usual para escalada de cobrança em FIDCs.

### 4.2 KPIs agregados

A função `kpis_principais(df)` retorna 13 indicadores. Os mais críticos:

```python
taxa_inadimplencia_valor = sum(vlr_em_aberto) / sum(vlr_nominal)
atraso_medio_pagos       = mean(dias_atraso onde dias_atraso > 0)
concentracao_top1        = max(sum(vlr_nominal) por id_beneficiario) / sum(vlr_nominal)
```

### 4.3 Análises temporais

Agregações por `mes_emissao`, `mes_vencimento` e `mes_pagamento` para gerar:
- Curva de emissão × recebimento (dual-axis)
- Tendência de atraso mediano por mês
- Quantidade de boletos vencendo por mês

### 4.4 Análises de concentração

- **Top N cedentes**: `groupby('id_beneficiario').sum('vlr_nominal')` — identifica risco de concentração.
- **Volume por UF**: `groupby('uf_sacado').sum('vlr_nominal')` cruzado com taxa de inadimplência (escala de cor).
- **Top divisões CNAE**: `groupby('cnae_div_sacado')` para análise setorial.

---

## 5. Dashboard

### 5.1 Tecnologia

- **Streamlit 1.31+**: framework Python para apps de dados, escolhido por:
  - Tempo de desenvolvimento curto
  - Suporte nativo a `st.dataframe` interativo
  - Cache automático (`@st.cache_data`)
  - Deploy gratuito no Streamlit Community Cloud

- **Plotly**: biblioteca de gráficos interativos. Vantagens sobre matplotlib:
  - Zoom, pan, hover nativos
  - Exportação para PNG e SVG
  - Compatibilidade total com Streamlit via `st.plotly_chart`

### 5.2 Estrutura de páginas

O app é uma single-page application com 4 abas (`st.tabs`):

| Aba | Conteúdo |
|---|---|
| **Visão Executiva** | KPIs, status, tipo_especie, risco, faixa de atraso |
| **Análise Temporal** | Evolução mensal emitido × recebido, tendência de atraso |
| **Risco & Concentração** | Top cedentes, UF, CNAE, matriz risco |
| **Detalhamento** | DataFrame interativo com 500 maiores boletos + export CSV |

### 5.3 Sistema de filtros

Todos os filtros são `st.multiselect` ou `st.slider` no sidebar, aplicados de forma combinada à máscara booleana `dff = df[mask]`. Filtros disponíveis:
- Mês de vencimento
- Status do boleto
- Classificação de risco
- UF do sacado
- Tipo de espécie
- Faixa de valor nominal

### 5.4 Cache e performance

```python
@st.cache_data
def get_dados():
    return carregar_dados()
```

O cache do Streamlit garante que as 7.118 linhas só são lidas uma vez por sessão. As operações de filtro e agregação são feitas em memória via pandas, com tempo de resposta < 100ms.

---

## 6. Segurança

### 6.1 Gestão de credenciais

| Ambiente | Mecanismo |
|---|---|
| Desenvolvimento local | `.env` (excluído do `.gitignore`) |
| Streamlit Community Cloud | `st.secrets` na interface web |
| Repositório GitHub público | **zero credenciais** — apenas `.env.example` e `secrets.toml.example` |

### 6.2 Wallet do Oracle

A wallet (`cwallet.sso`, `tnsnames.ora`, etc.) **nunca é commitada**. No deploy:
- O conteúdo do `.zip` da wallet é codificado em base64 e colado no `secrets.toml`
- O `data_processing.py` decodifica a wallet em `/tmp/credup_wallet/` em runtime
- O diretório `/tmp` é volátil — wallet recriada a cada cold start

### 6.3 Modo dual

Caso a banca não tenha credenciais Oracle, o `data_processing.py` faz fallback automático para os CSVs em `data/`. O badge no sidebar indica claramente a fonte ativa (🟢 Oracle ou 📄 CSV).

---

## 7. Tratamento de erros

### 7.1 Conexão Oracle

```python
try:
    return oracledb.connect(**kwargs)
except Exception as e:
    print(f"Falha ao conectar Oracle: {e}. Caindo para CSV.")
    return None
```

### 7.2 Tabelas inexistentes

```python
try:
    bol = pd.read_sql("SELECT * FROM CREDUP_BOLETOS", conn)
    aux = pd.read_sql("SELECT * FROM CREDUP_AUXILIAR", conn)
    return bol, aux
except Exception:
    return None  # → fallback CSV
```

### 7.3 Inserção em lote

```python
cur.executemany(sql, rows, batcherrors=True)
err = cur.getbatcherrors()
if err:
    print(f"{len(err)} erros (mostrando 3): {err[:3]}")
```

Permite que linhas individuais falhem (ex: violação de PK) sem abortar todo o batch.

---

## 8. Limitações e riscos conhecidos

| Limitação | Mitigação atual | Próximo passo |
|---|---|---|
| Janela de 1 mês de vencimento | Documentado no dashboard e relatório | Solicitar dataset mais amplo |
| CNAE em código numérico | `cnae_div` agrupa em famílias | Adicionar dimensão de descrição CNAE/IBGE |
| Classificação de risco determinística | Regras transparentes e auditáveis | Modelo XGBoost treinado com histórico de defaults |
| Single-tenant (sem auth) | Dashboard é apenas leitura | Adicionar autenticação OAuth (Streamlit Auth) |
| Cold start lento (Oracle Free) | Cache do Streamlit | Migrar para tier pago ou Postgres dedicado |

---

## 9. Métricas de qualidade

- **Cobertura de testes**: smoke test em `setup_oracle.py` valida COUNT e SUM após ingestão.
- **Tempo de execução do app**: < 2s para carregar todas as visualizações com 7.118 linhas.
- **Tamanho do código-fonte**: ~1.200 linhas Python (sem libs).
- **Dependências**: 7 pacotes em `requirements.txt`, todos com versões mínimas explícitas.

---

## 10. Repositório e deploy

- **Repositório**: `https://github.com/[user]/credup`
- **Dashboard online**: `https://[seu-app].streamlit.app`
- **Vídeo pitch**: `https://youtu.be/[seu-video]`
- **Documentação**: pasta `documentacao/`

> Os links serão preenchidos pela equipe ao final da publicação.
