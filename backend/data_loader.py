"""
backend.data_loader
===================
Pipeline orquestrador. Combina:
    database.buscar_dados_brutos()  → DataFrames crus (Oracle ou CSV)
    business_rules.*                 → classificações
e devolve um conjunto pronto para consumo do frontend.

API pública:
    carregar_dados()  →  (bol, aux, bol_enriquecido, fonte)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from backend.database import buscar_dados_brutos
from backend.business_rules import (
    classifica_status,
    faixa_atraso,
    classifica_risco,
    STATUS_INADIMPLENTES,
)


def _tipar_e_derivar_boletos(bol: pd.DataFrame) -> pd.DataFrame:
    """Converte tipos e cria colunas derivadas no DataFrame de boletos."""
    for col in ("dt_emissao", "dt_vencimento", "dt_pagamento"):
        bol[col] = pd.to_datetime(bol[col], errors="coerce")

    bol["dias_atraso"]    = (bol["dt_pagamento"] - bol["dt_vencimento"]).dt.days
    bol["mes_emissao"]    = bol["dt_emissao"].dt.to_period("M").astype(str)
    bol["mes_vencimento"] = bol["dt_vencimento"].dt.to_period("M").astype(str)
    bol["mes_pagamento"]  = bol["dt_pagamento"].dt.to_period("M").astype(str)

    bol["status_negocio"] = bol["tipo_baixa"].apply(classifica_status)
    bol["faixa_atraso"]   = bol["dias_atraso"].apply(faixa_atraso)
    bol["em_aberto"]      = bol["status_negocio"].isin(STATUS_INADIMPLENTES)
    bol["vlr_em_aberto"]  = np.where(bol["em_aberto"], bol["vlr_nominal"], 0.0)
    bol["vlr_recebido"]   = bol["vlr_baixa"].fillna(0.0)

    return bol


def _derivar_auxiliar(aux: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas derivadas no DataFrame auxiliar."""
    aux["cnae_div"] = (aux["cd_cnae_prin"].fillna(0) // 10000).astype("Int64")
    return aux


def _enriquecer_boletos(bol: pd.DataFrame, aux: pd.DataFrame) -> pd.DataFrame:
    """
    Cruza boletos com indicadores de risco do sacado (id_pagador → id_cnpj),
    e classifica risco do boleto.
    """
    risco_cols = [
        "id_cnpj", "uf", "cd_cnae_prin", "cnae_div",
        "sacado_indice_liquidez_1m", "score_quantidade_v2",
        "score_materialidade_v2", "media_atraso_dias",
        "share_vl_inad_pag_bol_6_a_15d",
    ]
    enr = bol.merge(
        aux[risco_cols].rename(columns={
            "id_cnpj":  "id_pagador",
            "uf":       "uf_sacado",
            "cnae_div": "cnae_div_sacado",
        }),
        on="id_pagador",
        how="left",
    )
    enr["risco"] = enr.apply(classifica_risco, axis=1)
    return enr


# ---------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------
def carregar_dados() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    """
    Carrega e processa as duas bases.
    Retorna (boletos, auxiliar, boletos_enriquecidos, fonte).
    """
    bol, aux, fonte = buscar_dados_brutos()
    bol = _tipar_e_derivar_boletos(bol)
    aux = _derivar_auxiliar(aux)
    enr = _enriquecer_boletos(bol, aux)
    return bol, aux, enr, fonte


# ---------------------------------------------------------------------
# Smoke test (rodar diretamente: `python -m backend.data_loader`)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    bol, aux, enr, fonte = carregar_dados()
    print(f"Fonte: {fonte.upper()}")
    print(f"Boletos: {len(bol):,}  |  Auxiliar: {len(aux):,}  |  Enriquecido: {len(enr):,}")

    from backend.kpis import kpis_principais
    k = kpis_principais(enr)
    print(f"Emitido:  R$ {k['valor_emitido']/1e6:,.2f} mi")
    print(f"Recebido: R$ {k['valor_recebido']/1e6:,.2f} mi")
    print(f"Em aberto: R$ {k['valor_em_aberto']/1e6:,.2f} mi")
    print(f"Inadimplência (R$): {k['taxa_inadimplencia_valor']*100:.2f}%")
