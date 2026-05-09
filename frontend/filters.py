"""
frontend.filters
================
Sidebar minimalista — apenas o badge indicando a fonte de dados
(Oracle ou CSV). As funções `renderizar_sidebar` e `aplicar_filtros`
foram preservadas para manter a interface das páginas, mas agora
não filtram nada (devolvem o DataFrame inteiro).
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from frontend.components import badge_fonte


def renderizar_sidebar(df: pd.DataFrame, fonte: str) -> dict:
    """
    Renderiza apenas o badge da fonte no sidebar.
    Retorna dicionário vazio (mantém compatibilidade com aplicar_filtros).
    """
    with st.sidebar:
        badge_fonte(fonte)
        st.caption("Bases: 7.118 boletos + 4.612 CNPJs")
    return {}


def aplicar_filtros(df: pd.DataFrame, sel: dict) -> pd.DataFrame:
    """Sem filtros — devolve o DataFrame inteiro."""
    return df.copy()
