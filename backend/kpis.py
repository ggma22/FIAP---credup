"""
backend.kpis
============
Agregações executivas a partir do DataFrame de boletos enriquecidos.
"""

from __future__ import annotations

import pandas as pd

from backend.business_rules import STATUS_HONRADOS, STATUS_INADIMPLENTES


def kpis_principais(df: pd.DataFrame) -> dict:
    """
    Recebe o DataFrame ENRIQUECIDO de boletos (com status_negocio e dias_atraso)
    e devolve um dicionário de métricas executivas.
    """
    if not len(df):
        return {}

    total_emitido  = float(df["vlr_nominal"].sum())
    total_recebido = float(df["vlr_recebido"].sum())
    total_aberto   = float(df["vlr_em_aberto"].sum())
    qtd            = len(df)
    qtd_honr       = int(df["status_negocio"].isin(STATUS_HONRADOS).sum())
    qtd_inad       = int(df["status_negocio"].isin(STATUS_INADIMPLENTES).sum())
    qtd_canc       = int((df["status_negocio"] == "Cancelado").sum())
    pa             = df.loc[df["dias_atraso"] > 0, "dias_atraso"]

    return {
        "qtd_boletos":              qtd,
        "valor_emitido":            total_emitido,
        "valor_recebido":           total_recebido,
        "valor_em_aberto":          total_aberto,
        "qtd_honrados":             qtd_honr,
        "qtd_inadimplentes":        qtd_inad,
        "qtd_cancelados":           qtd_canc,
        "taxa_inadimplencia_qtd":   qtd_inad   / qtd            if qtd            else 0.0,
        "taxa_inadimplencia_valor": total_aberto / total_emitido if total_emitido else 0.0,
        "ticket_medio":             float(df["vlr_nominal"].mean()),
        "ticket_mediana":           float(df["vlr_nominal"].median()),
        "atraso_medio_pagos":       float(pa.mean())   if len(pa) else 0.0,
        "atraso_mediana_pagos":     float(pa.median()) if len(pa) else 0.0,
    }
