"""
frontend.charts
===============
Funções Plotly reutilizáveis. Todas configuradas para o tema dark
do CredUp: backgrounds transparentes, fontes claras, hovers em teal.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from frontend.theme import (
    NAVY, NAVY_DARK, TEAL, TEAL_LT, GRAY, GRAY_LT, WHITE,
    GREEN, GOLD, RED,
    CORES_RISCO, CORES_STATUS, CORES_FAIXA_ATRASO,
)


# =====================================================================
# Layout default que toda figura herda
# =====================================================================
def _layout_dark(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=GRAY_LT, size=12),
        legend=dict(
            font=dict(color=GRAY_LT, size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor=NAVY_DARK,
            bordercolor=TEAL,
            font=dict(color=WHITE, family="Inter"),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(color=GRAY, size=11),
        title_font=dict(color=GRAY_LT, size=12),
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(color=GRAY, size=11),
        title_font=dict(color=GRAY_LT, size=12),
    )
    return fig


# =====================================================================
# Visão executiva
# =====================================================================
def status_horizontal(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("status_negocio").agg(
        qtd=("id_boleto", "count"),
        vlr=("vlr_nominal", "sum"),
    ).reset_index().sort_values("vlr", ascending=True)

    fig = px.bar(
        g, x="vlr", y="status_negocio", orientation="h",
        color="status_negocio", color_discrete_map=CORES_STATUS,
        text=g["qtd"].astype(int).map(lambda v: f"{v:,} boletos".replace(",", ".")),
        labels={"vlr": "Valor nominal (R$)", "status_negocio": ""},
    )
    fig.update_traces(textposition="outside", textfont_color=GRAY_LT)
    fig.update_xaxes(tickformat=",.0f")
    fig.update_layout(showlegend=False)
    return _layout_dark(fig, 380)


def especie_donut(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("tipo_especie").agg(vlr=("vlr_nominal", "sum")).reset_index()
    fig = px.pie(
        g, values="vlr", names="tipo_especie", hole=0.6,
        color_discrete_sequence=[TEAL, "#34D399", GOLD, RED, GRAY, "#475569", TEAL_LT],
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(color=NAVY, size=12, family="Inter"),
        marker=dict(line=dict(color=NAVY, width=2)),
    )
    return _layout_dark(fig, 380)


def risco_barras(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("risco").agg(qtd=("id_boleto", "count")).reset_index()
    ordem = ["Baixo", "Médio", "Alto"]
    g["risco"] = pd.Categorical(g["risco"], categories=ordem, ordered=True)
    g = g.sort_values("risco")

    fig = go.Figure()
    fig.add_bar(
        x=g["risco"], y=g["qtd"],
        marker=dict(
            color=[CORES_RISCO[r] for r in g["risco"]],
            line=dict(width=0),
        ),
        text=g["qtd"].map(lambda v: f"{v:,}".replace(",", ".")),
        textposition="outside",
        textfont=dict(color=WHITE, size=12),
    )
    fig.update_layout(showlegend=False, yaxis_title="Quantidade de boletos")
    return _layout_dark(fig, 320)


def faixa_atraso_barras(df: pd.DataFrame) -> go.Figure:
    ordem = ["Em dia", "1-7d", "8-15d", "16-30d", "31-60d", "60d+"]
    g = df.groupby("faixa_atraso").agg(vlr=("vlr_nominal", "sum")).reset_index()
    g["faixa_atraso"] = pd.Categorical(g["faixa_atraso"], categories=ordem, ordered=True)
    g = g.sort_values("faixa_atraso").dropna()

    fig = px.bar(
        g, x="faixa_atraso", y="vlr",
        color="faixa_atraso", color_discrete_map=CORES_FAIXA_ATRASO,
        text=g["vlr"].map(lambda v: f"R$ {v/1e3:,.0f}k".replace(",", ".")),
        labels={"vlr": "Valor (R$)", "faixa_atraso": ""},
    )
    fig.update_traces(textposition="outside", textfont_color=GRAY_LT)
    fig.update_layout(showlegend=False)
    return _layout_dark(fig, 320)


# =====================================================================
# Análise temporal
# =====================================================================
def temporal_emi_x_pag(df: pd.DataFrame) -> go.Figure:
    emi = df.groupby("mes_emissao").agg(
        emitido=("vlr_nominal", "sum"),
    ).reset_index().rename(columns={"mes_emissao": "mes"})

    pag = df.dropna(subset=["mes_pagamento"]).groupby("mes_pagamento").agg(
        recebido=("vlr_recebido", "sum"),
    ).reset_index().rename(columns={"mes_pagamento": "mes"})

    t = emi.merge(pag, on="mes", how="outer").sort_values("mes").fillna(0)

    fig = go.Figure()
    fig.add_bar(
        x=t["mes"], y=t["emitido"], name="Emitido",
        marker_color=TEAL_LT, opacity=0.55,
    )
    fig.add_scatter(
        x=t["mes"], y=t["recebido"], name="Recebido",
        mode="lines+markers",
        line=dict(color=TEAL, width=3),
        marker=dict(size=9, line=dict(color=NAVY, width=2)),
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12, x=0),
        yaxis_title="Valor (R$)",
    )
    return _layout_dark(fig, 380)


def boletos_por_mes_venc(df: pd.DataFrame) -> go.Figure:
    g = df.groupby("mes_vencimento").agg(
        qtd=("id_boleto", "count"),
    ).reset_index().sort_values("mes_vencimento")

    fig = px.bar(
        g, x="mes_vencimento", y="qtd",
        color_discrete_sequence=[TEAL],
        text=g["qtd"].map(lambda v: f"{v:,}".replace(",", ".")),
        labels={"mes_vencimento": "", "qtd": "Boletos"},
    )
    fig.update_traces(textposition="outside", textfont_color=GRAY_LT)
    return _layout_dark(fig, 320)


def tendencia_atraso(df: pd.DataFrame) -> go.Figure:
    g = df[df["dias_atraso"] > 0].groupby("mes_pagamento")["dias_atraso"]\
            .median().reset_index().sort_values("mes_pagamento")

    fig = px.line(
        g, x="mes_pagamento", y="dias_atraso", markers=True,
        color_discrete_sequence=[RED],
        labels={"mes_pagamento": "", "dias_atraso": "Atraso mediano (dias)"},
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=9))
    return _layout_dark(fig, 320)


# =====================================================================
# Risco & Concentração
# =====================================================================
def top_cedentes(df: pd.DataFrame, n: int = 10) -> go.Figure:
    g = df.groupby("id_beneficiario").agg(
        qtd=("id_boleto", "count"),
        vlr=("vlr_nominal", "sum"),
        inad=("vlr_em_aberto", "sum"),
    ).sort_values("vlr", ascending=False).head(n).reset_index()
    g["pct"] = g["vlr"] / df["vlr_nominal"].sum() * 100
    g["cedente_id"] = g["id_beneficiario"].str[:10] + "…"

    fig = go.Figure()
    fig.add_bar(
        x=g["cedente_id"], y=g["vlr"],
        marker_color=TEAL, name="Volume emitido",
        text=g["pct"].map(lambda v: f"{v:.1f}%"),
        textposition="outside",
        textfont_color=TEAL_LT,
    )
    fig.add_bar(
        x=g["cedente_id"], y=g["inad"],
        marker_color=RED, name="Em aberto",
    )
    fig.update_layout(
        barmode="group",
        yaxis_title="Valor (R$)",
        legend=dict(orientation="h", y=1.12, x=0),
    )
    return _layout_dark(fig, 380)


def volume_por_uf(df: pd.DataFrame) -> go.Figure:
    g = df.dropna(subset=["uf_sacado"]).groupby("uf_sacado").agg(
        qtd=("id_boleto", "count"),
        vlr=("vlr_nominal", "sum"),
        inad=("vlr_em_aberto", "sum"),
    ).reset_index().sort_values("vlr", ascending=False).head(15)
    g["taxa_inad"] = g["inad"] / g["vlr"] * 100

    fig = px.bar(
        g, x="uf_sacado", y="vlr", color="taxa_inad",
        color_continuous_scale=[[0, GREEN], [0.5, GOLD], [1, RED]],
        labels={"uf_sacado": "UF", "vlr": "Valor (R$)", "taxa_inad": "Inad. %"},
        text=g["qtd"].map(lambda v: f"{v:,}".replace(",", ".")),
    )
    fig.update_traces(textposition="outside", textfont_color=GRAY_LT)
    fig.update_layout(coloraxis_colorbar=dict(
        tickfont=dict(color=GRAY_LT),
        title_font=dict(color=GRAY_LT),
    ))
    return _layout_dark(fig, 360)


def top_cnae(df: pd.DataFrame, n: int = 10) -> go.Figure:
    g = df.dropna(subset=["cnae_div_sacado"]).groupby("cnae_div_sacado").agg(
        qtd=("id_boleto", "count"),
        vlr=("vlr_nominal", "sum"),
    ).reset_index().sort_values("vlr", ascending=False).head(n)
    g["cnae_label"] = g["cnae_div_sacado"].astype(str)
    g_sorted = g.sort_values("vlr")

    fig = px.bar(
        g_sorted, x="vlr", y="cnae_label", orientation="h",
        color="vlr", color_continuous_scale=[[0, TEAL_LT], [1, TEAL]],
        text=g_sorted["qtd"].map(lambda v: f"{v:,}".replace(",", ".")),
        labels={"vlr": "Valor (R$)", "cnae_label": "CNAE (divisão)"},
    )
    fig.update_traces(textposition="outside", textfont_color=GRAY_LT)
    fig.update_layout(coloraxis_showscale=False)
    return _layout_dark(fig, 360)


def matriz_risco(df: pd.DataFrame, sample: int = 1500) -> go.Figure | None:
    sub = df.dropna(subset=["sacado_indice_liquidez_1m", "score_quantidade_v2"])
    if not len(sub):
        return None

    sub_sample = sub.sample(min(sample, len(sub)), random_state=42)

    fig = px.scatter(
        sub_sample,
        x="sacado_indice_liquidez_1m", y="score_quantidade_v2",
        color="risco", color_discrete_map=CORES_RISCO,
        size="vlr_nominal", size_max=18,
        hover_data={
            "vlr_nominal": ":,.2f", "uf_sacado": True, "status_negocio": True,
            "sacado_indice_liquidez_1m": False, "score_quantidade_v2": False,
        },
        labels={
            "sacado_indice_liquidez_1m": "Liquidez sacado (1m)",
            "score_quantidade_v2": "Score quantitativo (v2)",
        },
    )
    fig.update_layout(legend_title="Risco")
    return _layout_dark(fig, 420)
