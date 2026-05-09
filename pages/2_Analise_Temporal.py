"""
Página: 📅 Análise Temporal
===========================
Comportamento da carteira ao longo do tempo: emissão × pagamento,
sazonalidade e tendência de atraso. Demonstração da metodologia.
"""

import streamlit as st

from backend import carregar_dados, kpis_principais
from frontend.theme import aplicar_tema
from frontend.components import hero, kpis_compactos
from frontend.filters import renderizar_sidebar, aplicar_filtros
from frontend import charts


st.set_page_config(
    page_title="CredUp · Análise Temporal",
    page_icon="📅",
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
    titulo='📅 Análise Temporal',
    subtitulo=(
        "Como a carteira se comporta ao longo do tempo. "
        "Curvas de emissão × pagamento expõem sazonalidade e a evolução do atraso "
        "mostra se a qualidade da carteira está melhorando ou piorando."
    ),
    tag="// METODOLOGIA EM AÇÃO",
)

st.info(
    "💡 **Por que isso importa para o investidor:** FIDCs com sazonalidade forte "
    "ou tendência crescente de atraso podem ter dificuldade de pagar a rentabilidade-alvo "
    "em períodos de stress. Um FIDC saudável tem curva de pagamento estável e atraso "
    "controlado mês a mês."
)

k = kpis_principais(dff) if len(dff) else {}
kpis_compactos(k)

st.divider()


# ---------------- Curva principal ----------------
st.markdown("##### Evolução mensal — emissão × pagamento")
if len(dff):
    st.plotly_chart(charts.temporal_emi_x_pag(dff), use_container_width=True)
else:
    st.info("Sem dados no recorte atual.")


# ---------------- Quantidade × tendência ----------------
col_e, col_f = st.columns(2)

with col_e:
    st.markdown("##### Quantidade de boletos por mês de vencimento")
    if len(dff):
        st.plotly_chart(charts.boletos_por_mes_venc(dff), use_container_width=True)

with col_f:
    st.markdown("##### Tendência de atraso ao longo do tempo (mediana)")
    if len(dff):
        st.plotly_chart(charts.tendencia_atraso(dff), use_container_width=True)


st.info(
    "**Como ler isso como investidor:** picos de vencimento concentrados em poucos "
    "meses indicam dependência de um único ciclo de caixa — risco se algo der errado "
    "naquele período. Já a tendência crescente de atraso é um sinal amarelo: a "
    "qualidade da carteira está se deteriorando."
)
