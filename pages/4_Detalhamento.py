"""
Página: 🔎 Detalhamento
========================
Drill-down até o nível do boleto individual. Tabela navegável + export CSV.
"""

import streamlit as st

from backend import carregar_dados
from frontend.theme import aplicar_tema
from frontend.components import hero
from frontend.filters import renderizar_sidebar, aplicar_filtros


st.set_page_config(
    page_title="CredUp · Detalhamento",
    page_icon="🔎",
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
    titulo='🔎 Detalhamento',
    subtitulo=(
        "Drill-down até o nível do boleto individual. "
        "Use os filtros laterais para isolar segmentos da carteira "
        "e exporte o recorte em CSV para análise externa."
    ),
    tag="// METODOLOGIA EM AÇÃO",
)

st.info(
    "💡 **Por que isso existe:** o investidor pessoa física raramente tem acesso "
    "à granularidade real da carteira de um FIDC. A maior parte dos prospectos só "
    "mostra agregados. O CredUp mantém o nível mais granular possível para você "
    "entender de onde vêm os indicadores."
)

st.caption(
    f"**{len(dff):,}** boletos no recorte · "
    f"R$ {dff['vlr_nominal'].sum()/1e6:,.2f} mi nominais"
    .replace(",", ".") if len(dff) else "Sem dados no recorte atual."
)

st.divider()


# ---------------- Tabela ----------------
cols_show = [
    "id_boleto", "dt_emissao", "dt_vencimento", "dt_pagamento",
    "vlr_nominal", "vlr_recebido",
    "status_negocio", "faixa_atraso", "dias_atraso",
    "tipo_especie", "uf_sacado", "cnae_div_sacado",
    "sacado_indice_liquidez_1m", "score_quantidade_v2", "risco",
]

if len(dff):
    show = dff[cols_show].copy() \
              .sort_values("vlr_nominal", ascending=False) \
              .head(500)
    show["id_boleto"] = show["id_boleto"].str[:12] + "…"

    st.dataframe(
        show,
        use_container_width=True,
        height=520,
        column_config={
            "vlr_nominal":  st.column_config.NumberColumn("Nominal (R$)",  format="R$ %.2f"),
            "vlr_recebido": st.column_config.NumberColumn("Recebido (R$)", format="R$ %.2f"),
            "dt_emissao":    st.column_config.DateColumn("Emissão"),
            "dt_vencimento": st.column_config.DateColumn("Vencimento"),
            "dt_pagamento":  st.column_config.DateColumn("Pagamento"),
            "dias_atraso":   st.column_config.NumberColumn("Atraso (d)"),
            "sacado_indice_liquidez_1m":
                st.column_config.ProgressColumn("Liquidez sacado", min_value=0, max_value=1),
            "score_quantidade_v2": st.column_config.NumberColumn("Score qtde"),
        },
    )

    st.caption(
        "Mostrando os 500 maiores boletos do filtro atual. "
        "Use os filtros laterais para refinar."
    )

    csv = dff[cols_show].to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Baixar resultado filtrado (CSV)",
        csv, "boletos_filtrados.csv", "text/csv",
    )

else:
    st.warning("Nenhum boleto corresponde aos filtros atuais.")
