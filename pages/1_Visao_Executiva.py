"""
Página: 📊 Visão Executiva
==========================
Demonstração da metodologia CredUp aplicada a uma carteira-exemplo
de 7.118 boletos. KPIs consolidados, distribuição por status, espécie,
classificação de risco e atraso.
"""

import streamlit as st

from backend import carregar_dados, kpis_principais
from frontend.theme import aplicar_tema
from frontend.components import hero, kpis_executivos
from frontend.filters import renderizar_sidebar, aplicar_filtros
from frontend import charts


st.set_page_config(
    page_title="CredUp · Visão Executiva",
    page_icon="📊",
    layout="wide",
)
aplicar_tema()


@st.cache_data(show_spinner="Carregando carteira…")
def get_dados():
    return carregar_dados()


bol, aux, df, fonte = get_dados()
sel = renderizar_sidebar(df, fonte)
dff = aplicar_filtros(df, sel)


# =====================================================================
hero(
    titulo='📊 Visão Executiva',
    subtitulo=(
        "KPIs consolidados, status da carteira, classificação de risco e atraso. "
        "Demonstração da metodologia em uma carteira-exemplo — exatamente o nível "
        "de detalhe que aparece quando você analisa um FIDC real."
    ),
    tag="// METODOLOGIA EM AÇÃO",
)

st.info(
    "💡 **O que você está vendo:** uma carteira-exemplo de 7.118 boletos é o tipo de "
    "lastro que existe dentro de um FIDC. O CredUp processa esses dados e gera os "
    "indicadores abaixo. Quando você usar a plataforma para avaliar um FIDC real, "
    "a leitura é a mesma."
)

k = kpis_principais(dff) if len(dff) else {}
kpis_executivos(k)

st.divider()


# ---------------- Linha 1 — Status & Espécie ----------------
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown("##### Distribuição por status do boleto")
    if len(dff):
        st.plotly_chart(charts.status_horizontal(dff), use_container_width=True)
    else:
        st.info("Sem dados no recorte atual.")

with col_b:
    st.markdown("##### Composição por tipo de espécie")
    if len(dff):
        st.plotly_chart(charts.especie_donut(dff), use_container_width=True)


# ---------------- Linha 2 — Risco & Atraso ----------------
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("##### Distribuição por classificação de risco")
    if len(dff):
        st.plotly_chart(charts.risco_barras(dff), use_container_width=True)

with col_d:
    st.markdown("##### Distribuição por faixa de atraso")
    if len(dff):
        st.plotly_chart(charts.faixa_atraso_barras(dff), use_container_width=True)


# ---------------- Insight executivo (linguagem do investidor) ----------------
if len(dff):
    pct_aberto = k.get("taxa_inadimplencia_valor", 0) * 100
    pct_atraso = (dff["dias_atraso"] > 0).sum() / len(dff) * 100

    st.info(
        f"**Como ler isso como investidor:** {pct_aberto:.2f}% do volume da carteira "
        f"está em aberto/inadimplente. Mas atenção — {pct_atraso:.1f}% dos boletos foram "
        f"pagos com atraso (média de {k.get('atraso_medio_pagos', 0):.1f} dias). Esse "
        f"atraso reduz a rentabilidade efetiva do FIDC mesmo sem virar default. "
        f"Em um fundo real, isso aparece como diferença entre rentabilidade-alvo e "
        f"rentabilidade realizada."
    )
