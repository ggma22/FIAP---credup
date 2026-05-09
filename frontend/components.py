"""
frontend.components
===================
Componentes Streamlit reutilizáveis: hero, KPIs, badges, section header.
Todos seguem a identidade visual definida em theme.py.
"""

from __future__ import annotations

import streamlit as st


def hero(titulo: str, subtitulo: str, tag: str = "// CredUp Dashboard") -> None:
    """
    Banner principal usado no topo de páginas. Suporta destaque em <em>...</em>
    no título (vira teal).
    """
    st.markdown(
        f"""
        <div class="credup-hero">
            <div class="credup-hero-tag">{tag}</div>
            <h1>{titulo}</h1>
            <p>{subtitulo}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_tag(texto: str) -> None:
    """Tag estilo `// Dashboard` antes do título da seção."""
    st.markdown(
        f'<div class="credup-section-tag">{texto}</div>',
        unsafe_allow_html=True,
    )


def feature_card(icone: str, titulo: str, descricao: str) -> None:
    """Card de feature com ícone, título e descrição."""
    st.markdown(
        f"""
        <div class="credup-card">
            <div class="credup-icon">{icone}</div>
            <h4>{titulo}</h4>
            <p>{descricao}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge_fonte(fonte: str) -> None:
    """Badge no sidebar indicando se está lendo do Oracle ou do CSV."""
    if fonte == "oracle":
        classe = "oracle"
        txt = "🟢 Oracle Autonomous DB"
    else:
        classe = "csv"
        txt = "📄 CSV (modo demo)"
    st.markdown(
        f'<div class="credup-badge-fonte {classe}">{txt}</div>',
        unsafe_allow_html=True,
    )


def disclaimer(texto: str) -> None:
    """Aviso amarelo discreto."""
    st.markdown(
        f'<div class="credup-disclaimer">{texto}</div>',
        unsafe_allow_html=True,
    )


# =====================================================================
# Formatadores
# =====================================================================
def fmt_int(v: float | int) -> str:
    return f"{int(v):,}".replace(",", ".")


def fmt_milhoes(v: float) -> str:
    return f"R$ {v/1e6:,.2f} mi".replace(",", ".")


def fmt_milhares(v: float) -> str:
    return f"R$ {v/1e3:,.1f} mil".replace(",", ".")


def fmt_pct(v: float) -> str:
    return f"{v*100:.2f}%"


# =====================================================================
# KPIs
# =====================================================================
def kpis_executivos(k: dict) -> None:
    """Grade de 10 KPIs (5 + 5) usada na home e Visão Executiva."""
    if not k:
        st.warning("Nenhum boleto no recorte atual. Ajuste os filtros.")
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Boletos analisados",  fmt_int(k.get("qtd_boletos", 0)))
    c2.metric("Valor emitido",       fmt_milhoes(k.get("valor_emitido", 0)))
    c3.metric("Valor recebido",      fmt_milhoes(k.get("valor_recebido", 0)))
    c4.metric("Em aberto",           fmt_milhares(k.get("valor_em_aberto", 0)))
    c5.metric("Inadimplência (R$)",  fmt_pct(k.get("taxa_inadimplencia_valor", 0)))

    c6, c7, c8, c9, c10 = st.columns(5)
    c6.metric("Inadimplência (#)",   fmt_pct(k.get("taxa_inadimplencia_qtd", 0)))
    c7.metric("Boletos honrados",    fmt_int(k.get("qtd_honrados", 0)))
    c8.metric("Cancelados",          fmt_int(k.get("qtd_cancelados", 0)))
    c9.metric("Ticket médio",        f"R$ {k.get('ticket_medio', 0):,.0f}".replace(",", "."))
    c10.metric("Atraso médio (pagos)", f"{k.get('atraso_medio_pagos', 0):.1f} dias")


def kpis_compactos(k: dict) -> None:
    """Versão reduzida (4 cards) usada nas páginas internas."""
    if not k:
        st.warning("Nenhum boleto no recorte atual. Ajuste os filtros.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Boletos",        fmt_int(k.get("qtd_boletos", 0)))
    c2.metric("Emitido",        fmt_milhoes(k.get("valor_emitido", 0)))
    c3.metric("Em aberto",      fmt_milhares(k.get("valor_em_aberto", 0)))
    c4.metric("Inadimplência",  fmt_pct(k.get("taxa_inadimplencia_valor", 0)))
