"""
backend.business_rules
======================
Regras de negócio puras — recebem dados, devolvem classificações.

Não conhece Oracle, CSV nem Streamlit. Funções determinísticas que
podem ser testadas isoladamente.
"""

from __future__ import annotations

import pandas as pd

# =====================================================================
# Mapeamento tipo_baixa → status de negócio
# =====================================================================
# Os códigos vêm do bureau bancário (CIP / Banco Central):
#   0 / 1 / 9  → liquidação normal (interbancária / intrabancária / STR)
#   5          → cancelado pelo cedente (não é inadimplência)
#   6          → protesto (default grave)
#   7          → vencido sem pagamento (default por decurso de prazo)
#   8          → liquidado pela instituição destinatária
#   NaN        → sem baixa registrada (em aberto)
STATUS_MAP = {
    "0": "Pago", "1": "Pago", "9": "Pago",
    "8": "Liquidado pela destinatária",
    "5": "Cancelado",
    "6": "Protesto",
    "7": "Vencido sem pagamento",
}

STATUS_HONRADOS:      set[str] = {"Pago", "Liquidado pela destinatária"}
STATUS_INADIMPLENTES: set[str] = {"Em aberto", "Protesto", "Vencido sem pagamento"}


# =====================================================================
# Funções de classificação
# =====================================================================
def classifica_status(tipo_baixa) -> str:
    """Mapeia o código bruto de tipo_baixa para um status legível de negócio."""
    if pd.isna(tipo_baixa):
        return "Em aberto"
    code = str(tipo_baixa).split(" - ")[0].strip()
    return STATUS_MAP.get(code, "Outro")


def faixa_atraso(dias) -> str:
    """Bucketiza dias de atraso em faixas usadas pelo painel."""
    if pd.isna(dias) or dias <= 0:
        return "Em dia"
    if dias <= 7:
        return "1-7d"
    if dias <= 15:
        return "8-15d"
    if dias <= 30:
        return "16-30d"
    if dias <= 60:
        return "31-60d"
    return "60d+"


def classifica_risco(row) -> str:
    """
    Classificação de risco por boleto, combinando:
        - status do boleto
        - liquidez do sacado (1 mês)
        - score quantitativo do sacado (v2)
        - dias de atraso

    Regra:
        ALTO  → status inadimplente,
                ou liquidez < 0.5,
                ou score < 800,
                ou dias_atraso > 30
        MÉDIO → liquidez < 0.7,
                ou score < 900,
                ou dias_atraso > 7
        BAIXO → caso contrário
    """
    if row["status_negocio"] in STATUS_INADIMPLENTES:
        return "Alto"

    liq = row.get("sacado_indice_liquidez_1m")
    sc  = row.get("score_quantidade_v2")
    da  = row.get("dias_atraso")

    if (pd.notna(liq) and liq < 0.5) or \
       (pd.notna(sc)  and sc  < 800) or \
       (pd.notna(da)  and da  > 30):
        return "Alto"

    if (pd.notna(liq) and liq < 0.7) or \
       (pd.notna(sc)  and sc  < 900) or \
       (pd.notna(da)  and da  > 7):
        return "Médio"

    return "Baixo"
