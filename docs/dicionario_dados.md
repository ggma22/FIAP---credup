# 📖 Dicionário de Dados — CredUp

Documentação técnica das duas bases utilizadas no projeto.

---

## Tabela 1 — `CREDUP_BOLETOS` (origem: `base_boletos_fiap.csv`)

Boletos transacionais (duplicatas mercantis) com vencimento em maio/2024.
**7.118 registros · 10 colunas originais + 8 derivadas.**

### Colunas originais

| Coluna | Tipo | Nulos | Descrição |
|---|---|---:|---|
| `id_boleto` | VARCHAR2(128) | 0 | Identificador hash (SHA-256) único do boleto. **PK**. |
| `id_pagador` | VARCHAR2(128) | 0 | Hash do CNPJ do **sacado** (devedor). FK para `CREDUP_AUXILIAR.id_cnpj`. |
| `id_beneficiario` | VARCHAR2(128) | 0 | Hash do CNPJ do **cedente** (originador / vendedor). |
| `dt_emissao` | DATE | 0 | Data de emissão da duplicata. Range: 2019-08-16 a 2024-05-31. |
| `dt_vencimento` | DATE | 0 | Data de vencimento. Janela analítica: maio/2024. |
| `dt_pagamento` | DATE | 70 | Data efetiva da baixa. Nulo quando boleto está em aberto. |
| `vlr_nominal` | NUMBER(18,2) | 0 | Valor nominal emitido (R$). Soma total: R$ 165.853.488,09. |
| `vlr_baixa` | NUMBER(18,2) | 820 | Valor efetivamente recebido (R$). Nulo quando não houve baixa monetária (cancelados ou em aberto). |
| `tipo_baixa` | VARCHAR2(120) | 70 | Código + descrição do tipo de liquidação. Ver mapeamento abaixo. |
| `tipo_especie` | VARCHAR2(80) | 0 | Espécie do título (DM, DMI, DS, DSI, NP, NF, ME, etc.). |

### Mapeamento de `tipo_baixa` → `status_negocio` (derivado)

| Código | Descrição original | Status de negócio | Quantidade |
|:-:|---|---|---:|
| `0` | Baixa integral interbancária | **Pago** | 5.138 |
| `1` | Baixa integral intrabancária | **Pago** | 1.120 |
| `9` | Baixa integral interbancária — Liquidação via STR | **Pago** | 40 |
| `8` | Baixa integral por solicitação da inst. destinatária | **Liquidado pela destinatária** | 324 |
| `5` | Baixa integral por solicitação do cedente | **Cancelado** | 316 |
| `7` | Baixa integral por decurso de prazo | **Vencido sem pagamento** | 77 |
| `6` | Baixa integral por envio para protesto | **Protesto** | 33 |
| `NULL` | (sem registro de baixa) | **Em aberto** | 70 |

### Distribuição de `tipo_especie`

| Código | Descrição | Qtd |
|---|---|---:|
| DM | Duplicata Mercantil | 5.529 |
| DMI | Duplicata Mercantil por Indicação | 1.488 |
| DS | Duplicata de Serviço | 66 |
| OUTROS | — | 16 |
| DSI | Duplicata de Serviço por Indicação | 9 |
| ME | Mensalidade Escolar | 4 |
| NP | Nota Promissória | 3 |
| NF | Nota Fiscal | 2 |
| Cartão de Crédito | — | 1 |

### Colunas derivadas (criadas em `data_processing.py`)

| Coluna | Cálculo | Uso |
|---|---|---|
| `dias_atraso` | `dt_pagamento - dt_vencimento` (dias) | Negativo = pago antes; positivo = atrasado |
| `mes_emissao` | `YYYY-MM` de `dt_emissao` | Análise temporal |
| `mes_vencimento` | `YYYY-MM` de `dt_vencimento` | Filtros |
| `mes_pagamento` | `YYYY-MM` de `dt_pagamento` | Análise temporal |
| `status_negocio` | mapeamento de `tipo_baixa` | Categorização de negócio |
| `faixa_atraso` | `Em dia` / `1-7d` / `8-15d` / `16-30d` / `31-60d` / `60d+` | Análise de atraso |
| `em_aberto` | bool — `status_negocio` ∈ {`Em aberto`, `Protesto`, `Vencido sem pagamento`} | Flag de inadimplência |
| `vlr_em_aberto` | `vlr_nominal` se `em_aberto` else 0 | Cálculo de valor inadimplente |
| `vlr_recebido` | `vlr_baixa` (NaN → 0) | Soma do efetivamente recebido |

---

## Tabela 2 — `CREDUP_AUXILIAR` (origem: `base_auxiliar_fiap.csv`)

Indicadores de risco de crédito por CNPJ. **4.612 registros · 11 colunas.**

| Coluna | Tipo | Nulos | Range / Distribuição | Descrição |
|---|---|---:|---|---|
| `id_cnpj` | VARCHAR2(128) | 0 | — | Hash SHA-256 do CNPJ. **PK**. |
| `cd_cnae_prin` | NUMBER(10) | 2 | 7 dígitos | CNAE principal (código IBGE da atividade econômica). |
| `uf` | VARCHAR2(2) | 359 | SP=1.260, PR=800, SC=437, MG=310… | UF da empresa. |
| `sacado_indice_liquidez_1m` | NUMBER(10,6) | 19 | 0,1 – 1,0 (mediana 0,9) | Índice de liquidez do sacado em janela de 1 mês. Valores próximos de 1 = melhor liquidez. |
| `cedente_indice_liquidez_1m` | NUMBER(10,6) | 2.149 | 0,1 – 1,0 (mediana 0,9) | Índice de liquidez do cedente em janela de 1 mês. Alta nulidade: nem todo CNPJ atua como cedente. |
| `score_materialidade_evolucao` | NUMBER(10,2) | 3 | 19 – 966 (mediana 895) | Score de evolução da materialidade (tendência de comportamento histórico). |
| `media_atraso_dias` | NUMBER(10,4) | 5 | 0 – 365 (mediana 178) | Média histórica de atraso da empresa em dias. |
| `indicador_liquidez_quantitativo_3m` | NUMBER(10,4) | 20 | — | Indicador quantitativo de liquidez em janela de 3 meses. |
| `share_vl_inad_pag_bol_6_a_15d` | NUMBER(10,6) | 5 | 0 – 1 | Participação do valor inadimplido em boletos pagos entre 6-15 dias. |
| `score_quantidade_v2` | NUMBER(10,2) | 6 | 22 – 986 (mediana 968) | Score baseado em quantidade de operações. Cauda longa para baixos valores. |
| `score_materialidade_v2` | NUMBER(10,2) | 6 | 42 – 989 (mediana 988) | Score baseado em materialidade financeira. |

### Coluna derivada

| Coluna | Cálculo | Uso |
|---|---|---|
| `cnae_div` | `cd_cnae_prin // 10000` | Divisão CNAE (3 dígitos) — agrupamento setorial. |

### Top 10 divisões CNAE no portfólio

| Divisão | Qtd CNPJs |
|:-:|---:|
| 478 | 739 |
| 477 | 629 |
| 471 | 253 |
| 474 | 195 |
| 464 | 179 |
| 475 | 147 |
| 463 | 132 |
| 141 | 127 |
| 222 | 114 |
| 468 | 107 |

---

## Cruzamento das bases

```sql
SELECT b.*, a.uf AS uf_sacado, a.sacado_indice_liquidez_1m,
       a.score_quantidade_v2, a.media_atraso_dias
FROM CREDUP_BOLETOS b
LEFT JOIN CREDUP_AUXILIAR a ON a.id_cnpj = b.id_pagador;
```

Resultado: **100% dos boletos têm match** (3.525 sacados + 1.189 cedentes únicos = 4.612 CNPJs).
