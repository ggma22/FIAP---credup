# 🎨 frontend/

Componentes Streamlit reutilizáveis pelas páginas. Não conhece Oracle — recebe DataFrames prontos do backend.

## Módulos

| Arquivo | Responsabilidade |
|---|---|
| [`theme.py`](theme.py) | Paleta CredUp dark + CSS global injetado. Centraliza identidade visual. |
| [`components.py`](components.py) | Hero banner, badge da fonte, KPI grids, formatadores. |
| [`filters.py`](filters.py) | Sidebar de filtros e função `aplicar_filtros(df, sel)`. |
| [`charts.py`](charts.py) | 11 funções Plotly para gráficos comuns (barras, donut, scatter, linhas). |

## Paleta CredUp

| Cor | Hex | Uso |
|---|---|---|
| Navy | `#0A2540` | Background principal |
| Navy escuro | `#061829` | Seções alternadas |
| Navy profundo | `#050E1B` | Footer / overlays |
| Teal | `#00BFA5` | Accent / botões / destaques |
| Verde | `#10B981` | Risco baixo / status pago |
| Dourado | `#F59E0B` | Risco médio / atenção |
| Vermelho | `#EF4444` | Risco alto / inadimplência |

## Princípios

- **Sem lógica de negócio** — apenas renderização
- **Componentes reutilizáveis** — `feature_card`, `hero`, `badge_fonte` usados em várias páginas
- **CSS centralizado** — toda customização visual em `theme.py`
- **Mobile-friendly** — media queries para `max-width: 768px`
