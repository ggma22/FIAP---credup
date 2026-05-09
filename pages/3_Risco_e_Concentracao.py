"""
Página: ⚠️ Risco & Concentração
================================
Onde mora o risco real do FIDC: top cedentes, distribuição geográfica,
setor (CNAE) e matriz de risco cruzando liquidez × score do sacado.
"""

import streamlit as st

from backend import carregar_dados, kpis_principais
from frontend.theme import aplicar_tema
from frontend.components import hero, kpis_compactos
from frontend.filters import renderizar_sidebar, aplicar_filtros
from frontend import charts


st.set_page_config(
    page_title="CredUp · Risco & Concentração",
    page_icon="⚠️",
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
    titulo='⚠️ Risco & Concentração',
    subtitulo=(
        "A análise mais importante para o investidor de FIDC. "
        "Aqui você vê dependência de um único cedente, exposição geográfica, "
        "setor predominante e o cruzamento liquidez × score dos sacados."
    ),
    tag="// METODOLOGIA EM AÇÃO",
)

st.info(
    "💡 **A regra de ouro do FIDC:** quanto mais concentrada a carteira, maior o "
    "risco. Um único cedente respondendo por 25% ou mais do volume é sinal "
    "amarelo — se essa empresa quebrar, todo o fundo sofre. Os gráficos abaixo "
    "expõem exatamente esse tipo de concentração oculta."
)

k = kpis_principais(dff) if len(dff) else {}
kpis_compactos(k)

st.divider()


# ---------------- Top cedentes ----------------
st.markdown("##### Concentração — Top 10 cedentes (originadores)")
if len(dff):
    st.plotly_chart(charts.top_cedentes(dff), use_container_width=True)
    st.caption(
        "Barras teal = volume emitido. Barras vermelhas = volume em aberto. "
        "Concentração elevada num único cedente é o principal risco estrutural "
        "de uma carteira de FIDC."
    )

st.divider()


# ---------------- UF e CNAE ----------------
col_g, col_h = st.columns(2)

with col_g:
    st.markdown("##### Volume por UF do sacado (devedor)")
    if len(dff):
        st.plotly_chart(charts.volume_por_uf(dff), use_container_width=True)
        st.caption(
            "A cor mostra a taxa de inadimplência por UF. Um FIDC muito concentrado "
            "em um único estado fica vulnerável a choques regionais."
        )

with col_h:
    st.markdown("##### Top 10 divisões CNAE (atividade do sacado)")
    if len(dff):
        st.plotly_chart(charts.top_cnae(dff), use_container_width=True)
        st.caption(
            "Concentração setorial é outro fator de risco. Setores cíclicos "
            "(construção, agro, varejo) podem amplificar perdas em recessões."
        )


# ---------------- Matriz de risco ----------------
st.markdown("##### Matriz de risco — liquidez do sacado × score quantitativo")

if len(dff):
    fig = charts.matriz_risco(dff)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "Cada bolha é um boleto. Tamanho = valor nominal. "
            "Cores = classificação Baixo / Médio / Alto. O quadrante inferior "
            "esquerdo (baixa liquidez + score baixo) concentra os boletos de risco Alto. "
            "FIDCs saudáveis têm a maioria do volume no quadrante superior direito."
        )
    else:
        st.info("Não há dados de liquidez/score suficientes no recorte atual.")
