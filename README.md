<div align="center">

# 💳 CredUp

### Inteligência Analítica para FIDC e FII

**Plataforma que padroniza métricas de risco e retorno entre FIDC e FII, simplificando a comparação para o investidor pessoa física que já conhece FII e quer diversificar para crédito estruturado.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Oracle](https://img.shields.io/badge/Oracle_Autonomous_DB-23-F80000?style=flat&logo=oracle&logoColor=white)](https://www.oracle.com/autonomous-database/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com)
[![FIAP](https://img.shields.io/badge/FIAP-Challenge_2025-EE2A7B?style=flat)](https://www.fiap.com.br)
[![License](https://img.shields.io/badge/license-Academic-blue?style=flat)](LICENSE.md)

[Sobre](#-sobre) · [Como rodar](#-como-rodar) · [Arquitetura](#%EF%B8%8F-arquitetura) · [Documentação](#-documentação) · [Equipe](#-equipe)

</div>

---

## 📌 Sobre

**CredUp** é uma plataforma de inteligência analítica que une duas classes de ativos historicamente analisadas em silos — **FIDC** (Fundos de Direitos Creditórios) e **FII** (Fundos de Investimento Imobiliário) — em uma única régua de comparação.

### O problema

O investidor PF intermediário (28-45 anos, perfil moderado a agressivo) que já investe em FII e quer diversificar para FIDC enfrenta:

- **Métricas em formatos incompatíveis** entre as duas classes
- **Acesso restrito** a dados granulares de FIDC
- **Dilema entre liquidez do FII e retorno potencial do FIDC** sem ferramenta integrada de análise

### A solução

O CredUp **padroniza a análise** das duas classes e oferece:

1. **Comparativo direto** FIDC × FII com mesma metodologia
2. **Demonstração da metodologia** aplicada a uma carteira-exemplo de 7.118 boletos (R$ 165,8 mi em duplicatas mercantis) — o mesmo nível de detalhe que aparece quando você analisa um FIDC real
3. **Conteúdo educacional** sobre Resolução CVM 175 e estrutura de cotas
4. **Direcionamento** para portais oficiais (B3, CVM, Anbima) onde o investidor pesquisa fundos reais

> A CredUp **não vende FIDC nem FII** — facilita a análise e o entendimento das duas classes para que o investidor decida com confiança.

---

## ✨ Funcionalidades

| | |
|---|---|
| 📊 **Análise transacional** | 7.118 boletos com classificação automática de status (pago, em aberto, protestado, cancelado, vencido) |
| ⚠️ **Classificação de risco** | Score determinístico **Baixo / Médio / Alto** por boleto, combinando liquidez, score quantitativo e atraso |
| 🎯 **Concentração explícita** | Identificação de risco por cedente, UF e CNAE — sinaliza dependência de um único originador |
| 📅 **Análise temporal** | Evolução mensal de emissão × pagamento, tendência de atraso ao longo do tempo |
| 🔎 **Drill-down** | Tabela navegável de boletos com filtros aplicados e exportação CSV |
| 💼 **Conteúdo educacional** | Página sobre FIDC (Resolução CVM 175, classes de cota, portais oficiais) |
| ⚡ **Simulador** | Calcula inadimplência projetada baseada em volume, concentração e perfil dos sacados |

---

## 🚀 Como rodar

### Pré-requisitos

- **Python 3.12+** ([baixar](https://www.python.org/downloads/))
- (Opcional) **Oracle Autonomous Database** com wallet e usuário configurado

### Modo demo (CSV) — para a banca

Sem credenciais Oracle, o app cai automaticamente em modo CSV usando os arquivos de `backend/data/`. Ideal para revisão rápida.

```bash
git clone https://github.com/SEU_USUARIO/credup.git
cd credup
pip install -r requirements.txt
streamlit run Home.py
```

Acesse `http://localhost:8501`. O badge no sidebar mostra **📄 CSV (modo demo)**.

### Modo produção (Oracle Autonomous Database)

#### 1. Configurar credenciais

```bash
cp .env.example .env
# edite .env com suas credenciais Oracle
```

Conteúdo esperado do `.env`:

```env
ORACLE_USER=credup_app
ORACLE_PASSWORD=SuaSenhaForte
ORACLE_DSN=seu_db_medium
ORACLE_WALLET_DIR=/caminho/para/wallet
ORACLE_WALLET_PASSWORD=SenhaDaWallet
```

#### 2. Popular o banco

**Opção A — Database Actions (sem código):**
- Abra Database Actions → Data Load → Local File
- Arraste os CSVs de `backend/data/` e nomeie as tabelas como `BASE_BOLETOS_FIAP` e `BASE_AUXILIAR_FIAP`
- Rode `backend/etl/schema.sql` no SQL Worksheet para criar PKs e índices

**Opção B — Script Python:**
```bash
python -m backend.etl.setup_oracle --recreate
```

#### 3. Rodar o dashboard

```bash
streamlit run Home.py
```

O badge no sidebar deve ficar **🟢 Oracle Autonomous DB**.

### Deploy público (Streamlit Cloud)

Ver guia completo em [`docs/deploy_streamlit_cloud.md`](docs/deploy_streamlit_cloud.md).

---

## 🏗️ Arquitetura

```
credup/
│
├── Home.py                       ← Entry point (página inicial)
├── pages/                        ← Páginas analíticas (Streamlit multipage)
│   ├── 1_Visao_Executiva.py
│   ├── 2_Analise_Temporal.py
│   ├── 3_Risco_e_Concentracao.py
│   ├── 4_Detalhamento.py
│   └── 5_Investir.py
│
├── backend/                      ← 🔧 Camada de dados + regras de negócio
│   ├── database.py                  Conexão Oracle (com fallback CSV)
│   ├── data_loader.py               Pipeline ETL (extrai → tipa → enriquece)
│   ├── business_rules.py            Status, atraso, classificação de risco
│   ├── kpis.py                      Agregações executivas
│   ├── data/                        CSVs de fallback (modo demo)
│   └── etl/
│       ├── setup_oracle.py          Script Python de ingestão
│       └── schema.sql               DDL puro (executável no SQL Worksheet)
│
├── frontend/                     ← 🎨 Componentes UI Streamlit reutilizáveis
│   ├── theme.py                     Paleta CredUp dark + CSS global
│   ├── components.py                Hero, KPIs, badges, formatadores
│   ├── filters.py                   Sidebar de filtros
│   └── charts.py                    Gráficos Plotly (11 funções)
│
├── .streamlit/
│   ├── config.toml                  Tema visual nativo
│   └── secrets.toml.example         Template para Streamlit Cloud
│
├── docs/                         ← 📚 Documentação técnica
│   ├── arquitetura.md
│   ├── dicionario_dados.md
│   ├── relatorio_tecnico.md
│   ├── deploy_streamlit_cloud.md
│   └── screenshots/
│
├── apresentacao/                 PPT + prints do dashboard
├── video_pitch/                  Roteiro do vídeo pitch
├── planilha_integrantes/         XLSX de identificação
│
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE.md
├── CHANGELOG.md
└── README.md                     Este arquivo
```

### Princípios de design

- **🔧 Backend não conhece Streamlit** — pode ser testado isolado, reutilizado em outros frontends
- **🎨 Frontend não conhece Oracle** — recebe DataFrames prontos
- **📄 Modo dual** — Oracle em produção, CSV como fallback automático para a banca
- **🛡️ Princípio de menor privilégio** — usuário `credup_app` tem permissão apenas de leitura
- **♻️ Cache** — `@st.cache_data` evita re-carga entre páginas

---

## 📊 Indicadores principais

Calculados sobre o universo de 7.118 boletos:

| Indicador | Valor |
|---|---:|
| Boletos analisados | **7.118** |
| Valor total emitido | R$ **165,8 mi** |
| Valor recebido | R$ **129,6 mi** |
| Em aberto / inadimplente | R$ **4,02 mi** |
| Taxa de inadimplência (R$) | **2,43%** |
| Atraso médio (dos pagos) | **16,3 dias** |
| Concentração no top 1 cedente | **25,8%** |
| Concentração em SP | **61%** |

### Regras de classificação de risco

```
ALTO   → status inadimplente,
         OU sacado_indice_liquidez_1m < 0,5,
         OU score_quantidade_v2 < 800,
         OU dias_atraso > 30

MÉDIO  → sacado_indice_liquidez_1m < 0,7,
         OU score_quantidade_v2 < 900,
         OU dias_atraso > 7

BAIXO  → caso contrário
```

Implementação em [`backend/business_rules.py`](backend/business_rules.py).

---

## 🛠️ Stack

- **Python 3.12+** — linguagem principal
- **Oracle Autonomous Database (OCI)** — persistência relacional
- **`oracledb`** — driver oficial Python ↔ Oracle
- **pandas + numpy** — tratamento e modelagem
- **Streamlit 1.31+** — frontend reativo (multipage nativo)
- **Plotly** — visualizações interativas
- **python-dotenv** — gerenciamento de credenciais locais

---

## 📚 Documentação

| Documento | Conteúdo |
|---|---|
| [`docs/arquitetura.md`](docs/arquitetura.md) | Visão técnica detalhada da arquitetura |
| [`docs/dicionario_dados.md`](docs/dicionario_dados.md) | Estrutura completa das tabelas e colunas |
| [`docs/relatorio_tecnico.md`](docs/relatorio_tecnico.md) | Decisões técnicas, algoritmos e segurança |
| [`docs/deploy_streamlit_cloud.md`](docs/deploy_streamlit_cloud.md) | Passo a passo de deploy público |
| [`backend/etl/schema.sql`](backend/etl/schema.sql) | DDL Oracle pronto para executar |

---

## 👥 Equipe

| Nome | RM |
|---|---|
| Giovanna Marotta | 567717 |
| Adelaine Freire | 568465 |
| Douglas Cavalcanti | 567841 |
| Tiago Sgroglia | 567170 |
| Victor de Aguiar | 567463 |

---

## ⚠️ Limitações e próximos passos

**Limitações atuais:**
- Janela analítica restrita a um mês (vencimentos em maio/2024)
- Identificadores são hashes SHA-256 (sem razão social legível)
- CNAE em código numérico (sem dimensão de descrição)
- Classificação de risco baseada em regras determinísticas, não em modelo preditivo
- Dados estáticos — sem pipeline de atualização automática

**Roadmap:**
- [ ] Modelo preditivo de inadimplência (XGBoost / LightGBM)
- [ ] Pipeline de ingestão automatizado (Apache Airflow)
- [ ] Dimensão de CNAE com descrições (IBGE)
- [ ] Sistema de alertas de concentração crítica
- [ ] Versão mobile responsiva
- [ ] Integração com APIs do CIP (dados em tempo real)

---

## 📜 Licença

Trabalho acadêmico desenvolvido no contexto do **Challenge FIAP 2025 · Turma 1TSCP**.
Uso restrito a fins educacionais. Ver [LICENSE.md](LICENSE.md).

---

<div align="center">

**Made with 💚 by 1TSCP @ FIAP · 2025**

</div>
