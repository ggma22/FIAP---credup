"""
CredUp — Backend
================
Camada de dados e regras de negócio.

Módulos:
    database        — conexão com Oracle (com fallback CSV automático)
    business_rules  — classificações de status, atraso e risco
    data_loader     — pipeline: extrai → tipa → enriquece → classifica
    kpis            — agregações executivas (totais, taxas, médias)
    etl             — scripts standalone para popular o Oracle
"""
from backend.data_loader import carregar_dados
from backend.kpis import kpis_principais
from backend.business_rules import STATUS_HONRADOS, STATUS_INADIMPLENTES

__all__ = [
    "carregar_dados",
    "kpis_principais",
    "STATUS_HONRADOS",
    "STATUS_INADIMPLENTES",
]
