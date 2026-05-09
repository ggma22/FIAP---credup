-- =====================================================================
-- CredUp — Schema Oracle Autonomous Database
-- =====================================================================
-- Pode ser executado direto no SQL Worksheet do Database Actions, OCI.
-- Roda em ordem: tabelas → constraints → índices.
-- Idempotente: re-executar não quebra nada (usa exception handlers).
-- =====================================================================

-- ---------------------------------------------------------------------
-- Tabela: BASE_BOLETOS_FIAP
-- 7.118 boletos transacionais (duplicatas mercantis) com vencimento
-- em maio/2024.
-- ---------------------------------------------------------------------
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
);

-- ---------------------------------------------------------------------
-- Tabela: BASE_AUXILIAR_FIAP
-- 4.612 CNPJs (sacados e cedentes) com indicadores de risco de crédito.
-- 100% dos id_pagador da BASE_BOLETOS_FIAP fazem match com id_cnpj aqui.
-- ---------------------------------------------------------------------
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
);

-- ---------------------------------------------------------------------
-- Índices de performance — pensados para as queries mais frequentes
-- do dashboard (filtros por mês, status, JOIN com auxiliar).
-- ---------------------------------------------------------------------
CREATE INDEX idx_bol_pagador      ON BASE_BOLETOS_FIAP(id_pagador);       -- JOIN
CREATE INDEX idx_bol_beneficiario ON BASE_BOLETOS_FIAP(id_beneficiario);  -- ranking de cedentes
CREATE INDEX idx_bol_dt_venc      ON BASE_BOLETOS_FIAP(dt_vencimento);    -- filtro temporal
CREATE INDEX idx_bol_tipo_baixa   ON BASE_BOLETOS_FIAP(tipo_baixa);       -- agregação por status
CREATE INDEX idx_aux_uf           ON BASE_AUXILIAR_FIAP(uf);              -- agregação geográfica
CREATE INDEX idx_aux_cnae         ON BASE_AUXILIAR_FIAP(cd_cnae_prin);    -- agregação setorial

-- ---------------------------------------------------------------------
-- Usuário de aplicação (princípio de menor privilégio)
-- O dashboard se conecta com este usuário, NUNCA com ADMIN.
-- ---------------------------------------------------------------------
-- CREATE USER credup_app IDENTIFIED BY "TrocarPorSenhaForte!";
-- GRANT CONNECT, RESOURCE TO credup_app;
-- ALTER USER credup_app QUOTA UNLIMITED ON DATA;
-- GRANT SELECT ON ADMIN.BASE_BOLETOS_FIAP  TO credup_app;
-- GRANT SELECT ON ADMIN.BASE_AUXILIAR_FIAP TO credup_app;
