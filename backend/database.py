"""
backend.database
================
Camada de conexão com a fonte de dados.

Estratégia "dual":
    1) Se variáveis ORACLE_* estiverem definidas (.env ou st.secrets) → Oracle
    2) Caso contrário → CSV local em backend/data/ (modo demo)

Esta é a ÚNICA parte do projeto que conhece detalhes de Oracle / CSV.
O restante do backend recebe DataFrames e não sabe de onde vieram.
"""

from __future__ import annotations

import os
import base64
import tempfile
import zipfile
from pathlib import Path

import pandas as pd

# ----- carrega .env (modo dev local) -----
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def _hydrate_streamlit_secrets() -> None:
    """Promove st.secrets['oracle'] para variáveis de ambiente, se rodando no Streamlit Cloud."""
    try:
        import streamlit as st  # noqa
        if "oracle" in st.secrets:
            sec = st.secrets["oracle"]
            for k in ("ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_DSN",
                      "ORACLE_WALLET_B64", "ORACLE_WALLET_PASSWORD"):
                if k in sec and not os.environ.get(k):
                    os.environ[k] = str(sec[k])
    except Exception:
        pass


_hydrate_streamlit_secrets()


# Caminho dos CSVs de fallback (relativo à raiz do projeto)
_CSV_DIR = Path(__file__).parent / "data"


# ---------------------------------------------------------------------
# Oracle Autonomous DB
# ---------------------------------------------------------------------
def _setup_wallet_b64() -> str | None:
    """Decodifica a wallet em base64 (Streamlit Cloud) e retorna o caminho local extraído."""
    b64 = os.environ.get("ORACLE_WALLET_B64")
    if b64:
        wallet_dir = Path(tempfile.gettempdir()) / "credup_wallet"
        wallet_dir.mkdir(exist_ok=True)
        zip_path = wallet_dir / "wallet.zip"
        zip_path.write_bytes(base64.b64decode(b64))
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(wallet_dir)
        return str(wallet_dir)
    return os.environ.get("ORACLE_WALLET_DIR")


def _conectar_oracle():
    user = os.environ.get("ORACLE_USER")
    pwd  = os.environ.get("ORACLE_PASSWORD")
    dsn  = os.environ.get("ORACLE_DSN")
    if not (user and pwd and dsn):
        return None

    try:
        import oracledb
    except ImportError:
        print("[CredUp] oracledb não instalado — usando CSV.")
        return None

    wallet = _setup_wallet_b64()
    wallet_pwd = os.environ.get("ORACLE_WALLET_PASSWORD") or pwd

    kwargs = dict(user=user, password=pwd, dsn=dsn)
    if wallet:
        kwargs["config_dir"] = wallet
        kwargs["wallet_location"] = wallet
        kwargs["wallet_password"] = wallet_pwd

    try:
        return oracledb.connect(**kwargs)
    except Exception as e:
        print(f"[CredUp] Falha ao conectar Oracle: {e}. Caindo para CSV.")
        return None


def _ler_oracle(conn) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    """Lê as duas tabelas no schema ADMIN (qualified)."""
    try:
        bol = pd.read_sql("SELECT * FROM ADMIN.BASE_BOLETOS_FIAP",  conn)
        aux = pd.read_sql("SELECT * FROM ADMIN.BASE_AUXILIAR_FIAP", conn)
        bol.columns = [c.lower() for c in bol.columns]
        aux.columns = [c.lower() for c in aux.columns]
        return bol, aux
    except Exception as e:
        print(f"[CredUp] Erro ao ler tabelas Oracle: {e}")
        return None


# ---------------------------------------------------------------------
# CSV (fallback)
# ---------------------------------------------------------------------
def _ler_csv() -> tuple[pd.DataFrame, pd.DataFrame]:
    bol = pd.read_csv(_CSV_DIR / "base_boletos_fiap.csv")
    aux = pd.read_csv(_CSV_DIR / "base_auxiliar_fiap.csv")
    return bol, aux


# ---------------------------------------------------------------------
# API pública do módulo
# ---------------------------------------------------------------------
def buscar_dados_brutos() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """
    Retorna (boletos, auxiliar, fonte).
        - fonte ∈ {"oracle", "csv"}
    """
    conn = _conectar_oracle()
    if conn is not None:
        try:
            res = _ler_oracle(conn)
            if res is not None:
                bol, aux = res
                return bol, aux, "oracle"
        finally:
            try: conn.close()
            except Exception: pass

    bol, aux = _ler_csv()
    return bol, aux, "csv"
