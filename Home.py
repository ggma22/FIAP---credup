"""
CredUp — Plataforma de Inteligência Analítica para FIDC e FII
==============================================================
Página inicial. Comparador de FIDC e FII para o investidor pessoa física.

Posicionamento (Sprint 2):
    "Plataforma de inteligência analítica que padroniza métricas de FIDC e FII,
     simplificando comparação e análise de risco para o investidor intermediário."

Como rodar:
    pip install -r requirements.txt
    streamlit run Home.py
"""

from __future__ import annotations

import streamlit as st

from backend import carregar_dados, kpis_principais
from frontend.theme import aplicar_tema
from frontend.components import (
    hero, feature_card, kpis_executivos, fmt_milhoes,
)
from frontend.filters import renderizar_sidebar, aplicar_filtros


# =====================================================================
# Configuração
# =====================================================================
st.set_page_config(
    page_title="CredUp — FIDC e FII com a mesma régua",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)
aplicar_tema()


# =====================================================================
# Carga de dados (cacheada)
# =====================================================================
@st.cache_data(show_spinner="Carregando dados de demonstração…")
def get_dados():
    return carregar_dados()


bol, aux, df, fonte = get_dados()


# =====================================================================
# Filtros (sidebar) e máscara — afetam só as páginas analíticas
# =====================================================================
sel = renderizar_sidebar(df, fonte)
dff = aplicar_filtros(df, sel)


# =====================================================================
# HERO — fala com o investidor PF
# =====================================================================
hero(
    titulo='Compare <em>FIDC e FII</em> com a mesma régua. Decida com confiança.',
    subtitulo=(
        "O CredUp padroniza métricas de risco e retorno entre FIDC e FII, "
        "simplificando a análise comparativa para o investidor que já conhece "
        "FII e quer diversificar para crédito estruturado."
    ),
    tag="✦ CREDUP · FACILITADORA DE FIDC E FII",
)


# =====================================================================
# 3 FEATURE CARDS — alinhados com o PPT da Sprint 2
# =====================================================================
fc1, fc2, fc3 = st.columns(3)
with fc1:
    feature_card(
        "📊", "Métricas padronizadas",
        "FIDC e FII traduzidos para a mesma linguagem de risco e retorno. "
        "Compare lado a lado o que normalmente fica em formatos incompatíveis.",
    )
with fc2:
    feature_card(
        "⚡", "Análise em tempo real",
        "Indicadores recalculados sob demanda. Sem planilhas, sem prospectos "
        "longos — você vê o que importa para a sua decisão.",
    )
with fc3:
    feature_card(
        "🎯", "Otimização de portfólio",
        "Avalie como cada classe se encaixa na sua alocação. Liquidez, retorno "
        "esperado e risco apresentados com a mesma metodologia.",
    )

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================================
# SIMULADOR — simulação simples FIDC vs FII para o investidor
# =====================================================================
st.markdown('<div class="credup-section-tag">// Simulador comparativo</div>', unsafe_allow_html=True)
st.markdown("### ⚡ Quanto rende seu aporte em FIDC vs FII?")
st.caption(
    "Estimativa simples baseada em rentabilidade-alvo típica das duas classes. "
    "Resultado meramente ilustrativo — antes de investir, consulte um assessor credenciado."
)

sim_col, res_col = st.columns([1, 1])

with sim_col:
    aporte = st.slider(
        "Aporte inicial (R$)",
        min_value=1_000, max_value=500_000,
        value=50_000, step=1_000,
        format="R$ %d",
    )
    periodo = st.slider(
        "Período (meses)",
        min_value=3, max_value=60,
        value=12, step=3,
    )
    cdi = st.slider(
        "CDI anual estimado (%)",
        min_value=8.0, max_value=18.0,
        value=14.0, step=0.25,
    )

with res_col:
    # FIDC sênior típico: CDI + 3 a 5% a.a. — usamos CDI + 4% como base
    fidc_aa = (cdi + 4) / 100
    fidc_meses = (1 + fidc_aa) ** (periodo / 12) - 1
    fidc_total = aporte * (1 + fidc_meses)
    fidc_renda = fidc_total - aporte

    # FII médio: dividend yield ~10% a.a. — apenas distribuição (sem volatilidade)
    fii_aa = 0.10
    fii_renda_acumulada = aporte * fii_aa * (periodo / 12)
    fii_total = aporte + fii_renda_acumulada

    # Formata números no padrão brasileiro (separador de milhar = ".")
    def br(v: float) -> str:
        return f"{v:,.0f}".replace(",", ".")

    fidc_total_br = br(fidc_total)
    fidc_renda_br = br(fidc_renda)
    fidc_pct_br   = f"{fidc_meses*100:.1f}".replace(".", ",")
    fii_total_br  = br(fii_total)
    fii_renda_br  = br(fii_renda_acumulada)

    st.markdown(
        f"""
        <div style="background: rgba(0,191,165,0.08); border: 1px solid rgba(0,191,165,0.3);
                    border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;">
            <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase;
                        letter-spacing: 1px; margin-bottom: 4px;">FIDC sênior · CDI + 4% a.a.</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #00BFA5;">
                R$ {fidc_total_br} <span style="font-size: 0.85rem; color: #94A3B8; font-weight: 600;">total</span>
            </div>
            <div style="font-size: 0.85rem; color: #CBD5E1; margin-top: 4px;">
                Rendimento: <strong>R$ {fidc_renda_br}</strong> ({fidc_pct_br}% no período)
            </div>
        </div>
        <div style="background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.3);
                    border-radius: 10px; padding: 1rem 1.2rem;">
            <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase;
                        letter-spacing: 1px; margin-bottom: 4px;">FII · DY 10% a.a. (ilustrativo)</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #F59E0B;">
                R$ {fii_total_br} <span style="font-size: 0.85rem; color: #94A3B8; font-weight: 600;">total</span>
            </div>
            <div style="font-size: 0.85rem; color: #CBD5E1; margin-top: 4px;">
                Rendimento: <strong>R$ {fii_renda_br}</strong> · isento de IR para PF
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "💡 **Importante:** os percentuais são premissas didáticas, não garantias. "
    "FIDCs sênior costumam pagar entre CDI + 3% e CDI + 6% conforme o risco da carteira; "
    "FIIs têm dividend yield variável e o preço da cota oscila no mercado. "
    "Use isso só pra ter ordem de grandeza."
)

st.divider()


# =====================================================================
# DEMONSTRAÇÃO DA METODOLOGIA — usando a base real
# =====================================================================
st.markdown('<div class="credup-section-tag">// Metodologia em ação</div>', unsafe_allow_html=True)
st.markdown("### 🔬 Como o CredUp avalia o risco de um FIDC")

st.markdown(
    """
    Quando você analisa um FIDC pelo CredUp, nós abrimos a carteira de
    direitos creditórios que dá lastro ao fundo e medimos:

    - **Quem paga** — taxa de inadimplência por status do boleto
    - **Quanto demora** — distribuição de atraso e seu impacto financeiro
    - **De onde vem o risco** — concentração por cedente, UF e setor (CNAE)
    - **O perfil dos sacados** — liquidez e score de cada empresa devedora

    Para você ver isso funcionando, abaixo aplicamos a metodologia em uma
    **carteira-exemplo de 7.118 boletos** (R$ 165,8 milhões em duplicatas mercantis).
    Os números abaixo são reais e calculados em tempo real a partir da base.
    """
)

st.markdown("<br>", unsafe_allow_html=True)

k = kpis_principais(dff) if len(dff) else {}
kpis_executivos(k)

st.markdown("<br>", unsafe_allow_html=True)


# =====================================================================
# Cards de navegação para as páginas
# =====================================================================
st.markdown('<div class="credup-section-tag">// Explore a metodologia</div>', unsafe_allow_html=True)
st.markdown("### Navegue pelas análises")
st.caption(
    "Cada página aprofunda em uma camada diferente da carteira-exemplo. "
    "É exatamente esse nível de detalhe que aparece quando você analisa um FIDC real pelo CredUp."
)

n1, n2 = st.columns(2)
with n1:
    feature_card(
        "📊", "Visão Executiva",
        "KPIs consolidados, distribuição da carteira por status e classificação de risco.",
    )
    feature_card(
        "⚠️", "Risco & Concentração",
        "Top cedentes, UF, segmento CNAE e matriz de risco — onde mora o risco oculto.",
    )

with n2:
    feature_card(
        "📅", "Análise Temporal",
        "Curva de emissão × pagamento e tendência de atraso ao longo do tempo.",
    )
    feature_card(
        "🔎", "Detalhamento",
        "Tabela navegável de boletos com filtros aplicados e export CSV.",
    )

st.markdown("<br>", unsafe_allow_html=True)

# CTA principal — Investir
st.markdown(
    """
    <div style="background: linear-gradient(135deg, rgba(0,191,165,0.12), rgba(0,191,165,0.04));
                border: 1px solid rgba(0,191,165,0.3); border-radius: 14px;
                padding: 1.8rem 2rem; margin-top: 1rem;">
        <div style="font-size: 0.72rem; color: #00BFA5; letter-spacing: 1.5px;
                    text-transform: uppercase; font-weight: 700; margin-bottom: 8px;">
            // PRONTO PARA INVESTIR?
        </div>
        <h3 style="color: white !important; margin: 0 0 8px 0 !important;">
            Compare FIDC e FII e encontre fundos disponíveis no mercado
        </h3>
        <p style="color: #CBD5E1; margin: 0 !important; font-size: 0.95rem; line-height: 1.6;">
            A página <strong style="color: #00BFA5;">Investir</strong> traz o comparativo completo
            FIDC × FII, conteúdo educacional sobre Resolução CVM 175 e links para os portais
            oficiais (B3, CVM, Anbima) onde você pesquisa fundos reais.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================================
# Rodapé
# =====================================================================
st.divider()
st.markdown(
    """
    <div style="text-align: center; padding: 1.5rem 0; color: #94A3B8; font-size: 0.85rem;">
        <strong style="color: #FFFFFF;">CredUp</strong> · FIAP 1TSCP · Challenge 2025 ·
        Plataforma acadêmica de inteligência analítica para FIDC e FII
    </div>
    """,
    unsafe_allow_html=True,
)
