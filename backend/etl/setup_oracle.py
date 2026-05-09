"""
CredUp — Ingestão CSV → Oracle Autonomous Database
==================================================
Cria as tabelas BASE_BOLETOS_FIAP e BASE_AUXILIAR_FIAP no schema ADMIN
(ou no schema do usuário conectado), com índices para as queries do
dashboard, e faz bulk insert dos dois CSVs.

Como rodar:
    1) Tenha um .env com:
         ORACLE_USER=ADMIN
         ORACLE_PASSWORD=<senha>
         ORACLE_DSN=<servico, ex: credup_medium>
         ORACLE_WALLET_DIR=<caminho da wallet descompactada>   (opcional)
         ORACLE_WALLET_PASSWORD=<senha da wallet>              (opcional)

    2) python -m backend.etl.setup_oracle
       ou: python -m backend.etl.setup_oracle --recreate

OBS: O Migue usou o Database Actions web (Data Load) na entrega real,
o que é totalmente equivalente. Este script existe para reprodutibilidade.
"""

from __future__ import annotations

import os
import sys
import argparse
from pathlib import Path

import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

try:
    import oracledb
except ImportError:
    print("Instale o driver: pip install oracledb")
    sys.exit(1)


# ---------------------------------------------------------------------
# DDL — pode ser visto no schema.sql ao lado deste arquivo.
# ---------------------------------------------------------------------
DDL_BOLETOS = """
CREATE TABLE BASE_BOLETOS_FIAP (
    id_boleto         VARCHAR2(128) NOT NULL,
    id_pagador        VARCHAR2(128) NOT NULL,
    id_beneficiario   VARCHAR2(128) NOT NULL,
    dt_emissao        DATE,
    dt_vencimento     DATE,
    dt_pagamento      DATE,
    vlr_nominal       NUMBER(18,2),
    vlr_baixa         NUMBER(18,2),
    tipo_baixa        VARCHAR2(120),
    tipo_especie      VARCHAR2(80),
    CONSTRAINT pk_boletos PRIMARY KEY (id_boleto)
)
"""

DDL_AUXILIAR = """
CREATE TABLE BASE_AUXILIAR_FIAP (
    id_cnpj                              VARCHAR2(128) NOT NULL,
    cd_cnae_prin                         NUMBER(10),
    uf                                   VARCHAR2(2),
    sacado_indice_liquidez_1m            NUMBER(10,6),
    cedente_indice_liquidez_1m           NUMBER(10,6),
    score_materialidade_evolucao         NUMBER(10,2),
    media_atraso_dias                    NUMBER(10,4),
    indicador_liquidez_quantitativo_3m   NUMBER(10,4),
    share_vl_inad_pag_bol_6_a_15d        NUMBER(10,6),
    score_quantidade_v2                  NUMBER(10,2),
    score_materialidade_v2               NUMBER(10,2),
    CONSTRAINT pk_auxiliar PRIMARY KEY (id_cnpj)
)
"""

INDEXES = [
    "CREATE INDEX idx_bol_pagador      ON BASE_BOLETOS_FIAP(id_pagador)",
    "CREATE INDEX idx_bol_beneficiario ON BASE_BOLETOS_FIAP(id_beneficiario)",
    "CREATE INDEX idx_bol_dt_venc      ON BASE_BOLETOS_FIAP(dt_vencimento)",
    "CREATE INDEX idx_bol_tipo_baixa   ON BASE_BOLETOS_FIAP(tipo_baixa)",
    "CREATE INDEX idx_aux_uf           ON BASE_AUXILIAR_FIAP(uf)",
    "CREATE INDEX idx_aux_cnae         ON BASE_AUXILIAR_FIAP(cd_cnae_prin)",
]


def conectar():
    user = os.environ.get("ORACLE_USER")
    pwd  = os.environ.get("ORACLE_PASSWORD")
    dsn  = os.environ.get("ORACLE_DSN")
    if not (user and pwd and dsn):
        print("ERRO: defina ORACLE_USER, ORACLE_PASSWORD e ORACLE_DSN no .env")
        sys.exit(1)

    wallet_dir = os.environ.get("ORACLE_WALLET_DIR")
    wallet_pwd = os.environ.get("ORACLE_WALLET_PASSWORD") or pwd

    kwargs = dict(user=user, password=pwd, dsn=dsn)
    if wallet_dir:
        kwargs["config_dir"] = wallet_dir
        kwargs["wallet_location"] = wallet_dir
        kwargs["wallet_password"] = wallet_pwd

    print(f"Conectando em {dsn}…")
    return oracledb.connect(**kwargs)


def drop_se_existir(cur, tabela):
    try:
        cur.execute(f"DROP TABLE {tabela} CASCADE CONSTRAINTS PURGE")
        print(f"  · {tabela} dropada")
    except oracledb.DatabaseError as e:
        if "ORA-00942" not in str(e):
            raise


def criar_tabela(cur, tabela, ddl):
    try:
        cur.execute(ddl)
        print(f"  ✓ {tabela} criada")
    except oracledb.DatabaseError as e:
        if "ORA-00955" in str(e):
            print(f"  · {tabela} já existe")
        else:
            raise


def df_para_tuplas(df, cols):
    sub = df[list(cols)].copy()
    rows = []
    for tup in sub.itertuples(index=False, name=None):
        rows.append(tuple(
            None if (isinstance(v, float) and pd.isna(v)) or v is pd.NaT else v
            for v in tup
        ))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--recreate", action="store_true",
                        help="dropa as tabelas antes de recriar")
    parser.add_argument("--data-dir", default=None,
                        help="pasta com os CSVs (default: ../data)")
    args = parser.parse_args()

    data_dir = Path(args.data_dir) if args.data_dir \
        else Path(__file__).parent.parent / "data"
    print(f"Lendo CSVs de {data_dir}")

    bol_csv = pd.read_csv(data_dir / "base_boletos_fiap.csv")
    aux_csv = pd.read_csv(data_dir / "base_auxiliar_fiap.csv")
    print(f"  · {len(bol_csv):,} boletos | {len(aux_csv):,} auxiliares")

    for c in ("dt_emissao", "dt_vencimento", "dt_pagamento"):
        bol_csv[c] = pd.to_datetime(bol_csv[c], errors="coerce")

    conn = conectar()
    cur = conn.cursor()

    print("\n→ Tabelas")
    if args.recreate:
        drop_se_existir(cur, "BASE_BOLETOS_FIAP")
        drop_se_existir(cur, "BASE_AUXILIAR_FIAP")
    criar_tabela(cur, "BASE_BOLETOS_FIAP",  DDL_BOLETOS)
    criar_tabela(cur, "BASE_AUXILIAR_FIAP", DDL_AUXILIAR)
    conn.commit()

    print("\n→ Limpando dados existentes")
    cur.execute("TRUNCATE TABLE BASE_BOLETOS_FIAP")
    cur.execute("TRUNCATE TABLE BASE_AUXILIAR_FIAP")

    print("\n→ Inserindo boletos")
    cols_bol = ["id_boleto", "id_pagador", "id_beneficiario",
                "dt_emissao", "dt_vencimento", "dt_pagamento",
                "vlr_nominal", "vlr_baixa", "tipo_baixa", "tipo_especie"]
    placeholders = ", ".join(f":{i+1}" for i in range(len(cols_bol)))
    sql = f"INSERT INTO BASE_BOLETOS_FIAP ({', '.join(cols_bol)}) VALUES ({placeholders})"
    rows = df_para_tuplas(bol_csv, cols_bol)
    cur.executemany(sql, rows, batcherrors=True)
    err = cur.getbatcherrors()
    if err:
        print(f"  ! {len(err)} erros (mostrando 3): {err[:3]}")
    print(f"  ✓ {len(rows):,} boletos inseridos")

    print("\n→ Inserindo auxiliar")
    cols_aux = ["id_cnpj", "cd_cnae_prin", "uf",
                "sacado_indice_liquidez_1m", "cedente_indice_liquidez_1m",
                "score_materialidade_evolucao", "media_atraso_dias",
                "indicador_liquidez_quantitativo_3m", "share_vl_inad_pag_bol_6_a_15d",
                "score_quantidade_v2", "score_materialidade_v2"]
    placeholders = ", ".join(f":{i+1}" for i in range(len(cols_aux)))
    sql = f"INSERT INTO BASE_AUXILIAR_FIAP ({', '.join(cols_aux)}) VALUES ({placeholders})"
    rows = df_para_tuplas(aux_csv, cols_aux)
    cur.executemany(sql, rows, batcherrors=True)
    err = cur.getbatcherrors()
    if err:
        print(f"  ! {len(err)} erros (mostrando 3): {err[:3]}")
    print(f"  ✓ {len(rows):,} auxiliares inseridos")
    conn.commit()

    print("\n→ Índices")
    for sql in INDEXES:
        try:
            cur.execute(sql)
            print(f"  ✓ {sql.split()[2]} criado")
        except oracledb.DatabaseError as e:
            if "ORA-00955" in str(e) or "ORA-01408" in str(e):
                pass
            else:
                print(f"  ! erro: {e}")
    conn.commit()

    print("\n→ Smoke test")
    cur.execute("SELECT COUNT(*) FROM BASE_BOLETOS_FIAP")
    n_bol = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM BASE_AUXILIAR_FIAP")
    n_aux = cur.fetchone()[0]
    cur.execute("SELECT SUM(vlr_nominal) FROM BASE_BOLETOS_FIAP")
    total = cur.fetchone()[0]
    print(f"  · {n_bol:,} boletos no Oracle")
    print(f"  · {n_aux:,} auxiliares no Oracle")
    print(f"  · Soma vlr_nominal: R$ {float(total):,.2f}")

    cur.close()
    conn.close()
    print("\n✅ Ingestão concluída com sucesso.")


if __name__ == "__main__":
    main()
