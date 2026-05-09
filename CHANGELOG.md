# Changelog

Todas as mudanças relevantes neste projeto são registradas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [1.0.0] — Sprint 4 · Solução Final

### Adicionado
- Persistência em **Oracle Autonomous Database** (OCI), com fallback automático para CSV
- Dashboard Streamlit multipage com 5 páginas analíticas:
  - Home (hero + simulador + KPIs + navegação)
  - Visão Executiva (KPIs detalhados + status, espécie, risco, atraso)
  - Análise Temporal (emissão × pagamento, tendência de atraso)
  - Risco & Concentração (top cedentes, UF, CNAE, matriz de risco)
  - Detalhamento (tabela navegável + export CSV)
  - Investir (educacional sobre FIDC: CVM 175, classes de cota, portais oficiais)
- Tema dark navy + teal com glass morphism, identidade visual coesa
- Backend modular (database, data_loader, business_rules, kpis)
- Frontend componentizado (theme, components, filters, charts)
- Usuário de aplicação `credup_app` com permissão de leitura mínima
- Script de ingestão `setup_oracle.py` + `schema.sql` puro
- Documentação técnica em `docs/` (arquitetura, dicionário, relatório, deploy)
- Apresentação PowerPoint de 12 slides
- Roteiro de vídeo pitch (5 minutos)
- Planilha de identificação de integrantes

### Tecnologias
- Python 3.12, pandas, numpy
- Streamlit 1.31+, Plotly
- oracledb 2.0+
- Oracle Autonomous Database

### Equipe
- Giovanna Marotta (RM 567717)
- Adelaine Freire (RM 568465)
- Douglas Cavalcanti (RM 567841)
- Tiago Sgroglia (RM 567170)
- Victor de Aguiar (RM 567463)

---

## [0.2.0] — Sprint 2 · Arquitetura da Solução

### Adicionado
- Definição da arquitetura de referência
- Apresentação institucional do CredUp
- Mockup do dashboard

---

## [0.1.0] — Sprint 1 · Concepção

### Adicionado
- Identificação do problema de mercado (FIDC e duplicatas mercantis)
- Pesquisa de plataformas existentes
- Definição da proposta de valor
