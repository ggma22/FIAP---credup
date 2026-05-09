# 📄 pages/

Páginas adicionais do dashboard Streamlit. Cada arquivo aqui vira automaticamente uma página no menu lateral, ordenada pelo prefixo numérico.

## Convenção do Streamlit

- Arquivo na raiz (`Home.py`) → página inicial
- Arquivos em `pages/` com prefixo numérico → páginas adicionais ordenadas
- O Streamlit gera a navegação no sidebar automaticamente

## Páginas

| Arquivo | Conteúdo |
|---|---|
| [`1_Visao_Executiva.py`](1_Visao_Executiva.py) | KPIs detalhados, status da carteira, tipo de espécie, risco e atraso |
| [`2_Analise_Temporal.py`](2_Analise_Temporal.py) | Curvas mensais de emissão × pagamento e tendência de atraso |
| [`3_Risco_e_Concentracao.py`](3_Risco_e_Concentracao.py) | Top cedentes, UF, CNAE e matriz de risco (liquidez × score) |
| [`4_Detalhamento.py`](4_Detalhamento.py) | Tabela navegável + export CSV do recorte filtrado |
| [`5_Investir.py`](5_Investir.py) | Conteúdo educacional sobre FIDC: Resolução CVM 175, classes de cota, portais oficiais |

## Estrutura típica de uma página

```python
import streamlit as st
from backend import carregar_dados, kpis_principais
from frontend.theme import aplicar_tema
from frontend.components import hero, kpis_compactos
from frontend.filters import renderizar_sidebar, aplicar_filtros
from frontend import charts

st.set_page_config(page_title="CredUp · …", page_icon="…", layout="wide")
aplicar_tema()

@st.cache_data(show_spinner="Carregando carteira…")
def get_dados():
    return carregar_dados()

bol, aux, df, fonte = get_dados()
sel = renderizar_sidebar(df, fonte)
dff = aplicar_filtros(df, sel)

hero(titulo="…", subtitulo="…", tag="// SEÇÃO")
# … renderiza KPIs, charts, etc.
```

Os filtros do sidebar são compartilhados via `st.session_state`, então o usuário ajusta uma vez e a seleção persiste ao trocar de página.
