"""
frontend.theme
==============
Tema visual do CredUp — dark mode com glass morphism.
Inspirado na landing institucional, adaptado para Streamlit.

Paleta:  navy escuro como base + teal CredUp como accent.
Estilo:  glass cards com `backdrop-filter`, bordas em teal sutil,
         tipografia Inter, animações de hover discretas.
"""

from __future__ import annotations

import streamlit as st


# =====================================================================
# Paleta CredUp dark
# =====================================================================
NAVY        = "#0A2540"   # Background principal
NAVY_DARK   = "#061829"   # Seções alternadas
NAVY_DEEP   = "#050E1B"   # Footer / overlays
NAVY_MD     = "#143456"   # Card hover
NAVY_LT     = "#1E4972"

TEAL        = "#00BFA5"   # Accent
TEAL_LT     = "#4DDDE0"   # Hover
TEAL_DIM    = "rgba(0, 191, 165, 0.15)"

WHITE       = "#FFFFFF"
GRAY        = "#94A3B8"
GRAY_LT     = "#CBD5E1"

GREEN       = "#10B981"   # Risco baixo
GREEN_LT    = "#34D399"
GOLD        = "#F59E0B"   # Risco médio
RED         = "#EF4444"   # Risco alto
ORANGE      = "#F97316"


# Mapas de cor para gráficos
CORES_RISCO = {
    "Baixo":  GREEN,
    "Médio":  GOLD,
    "Alto":   RED,
}

CORES_STATUS = {
    "Pago":                          GREEN,
    "Liquidado pela destinatária":   GREEN_LT,
    "Cancelado":                     GRAY,
    "Em aberto":                     GOLD,
    "Vencido sem pagamento":         ORANGE,
    "Protesto":                      RED,
    "Outro":                         "#475569",
}

CORES_FAIXA_ATRASO = {
    "Em dia":   GREEN,
    "1-7d":     TEAL,
    "8-15d":    "#FCD34D",
    "16-30d":   GOLD,
    "31-60d":   ORANGE,
    "60d+":     RED,
}


# Aliases de compatibilidade (alguns módulos antigos esperam esses nomes)
COR_PRIMARIA = NAVY
COR_TEAL     = TEAL
COR_OURO     = GOLD
COR_VERMELHO = RED
COR_VERDE    = GREEN
COR_CINZA    = GRAY


# =====================================================================
# CSS — chamado uma vez por página
# =====================================================================
_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ───── Reset ───── */
*, *::before, *::after {{
    box-sizing: border-box;
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
}}

/* ───── Background da app ───── */
.stApp {{
    background: {NAVY};
    color: {WHITE};
}}

.stApp > header {{
    background: transparent !important;
}}

/* Container principal */
.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}}

/* ───── Tipografia ───── */
h1, h2, h3, h4, h5, h6 {{
    color: {WHITE} !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.5px;
}}

h1 {{ font-size: 2.4rem !important; font-weight: 800 !important; }}
h2 {{ font-size: 1.7rem !important; font-weight: 700 !important; }}
h3 {{ font-size: 1.25rem !important; font-weight: 700 !important; }}
h4, h5, h6 {{ font-weight: 600 !important; }}

p, li, label, span:not([class*="badge"]):not([class*="tag"]) {{
    color: {GRAY_LT};
}}

/* ───── Sidebar ───── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {NAVY_DEEP} 0%, {NAVY_DARK} 100%) !important;
    border-right: 1px solid rgba(0, 191, 165, 0.15);
}}

[data-testid="stSidebar"] * {{
    color: {GRAY_LT} !important;
}}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {{
    color: {WHITE} !important;
}}

[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(0, 191, 165, 0.2) !important;
}}

[data-testid="stSidebar"] [data-baseweb="select"] * {{
    color: {WHITE} !important;
}}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="input"] > div {{
    background: rgba(255, 255, 255, 0.05) !important;
    color: {WHITE} !important;
}}

/* Sidebar nav (multipage) */
[data-testid="stSidebarNav"] {{
    background: transparent;
    padding-bottom: 1rem;
}}

[data-testid="stSidebarNav"] a {{
    color: {GRAY_LT} !important;
    border-radius: 8px;
    margin-bottom: 4px;
    padding: 8px 12px !important;
    transition: background 0.2s, color 0.2s;
}}

[data-testid="stSidebarNav"] a:hover {{
    background: rgba(0, 191, 165, 0.1) !important;
    color: {TEAL} !important;
}}

[data-testid="stSidebarNav"] a[aria-current="page"] {{
    background: {TEAL_DIM} !important;
    color: {TEAL} !important;
    font-weight: 600 !important;
}}

/* ───── Métricas (KPIs nativos) ───── */
[data-testid="stMetric"] {{
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(0, 191, 165, 0.15);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    backdrop-filter: blur(8px);
    transition: border-color 0.2s, transform 0.15s;
}}

[data-testid="stMetric"]:hover {{
    border-color: {TEAL};
    transform: translateY(-2px);
}}

[data-testid="stMetricValue"] {{
    color: {WHITE} !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.8px;
}}

[data-testid="stMetricLabel"] {{
    color: {GRAY} !important;
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    white-space: normal !important;
}}

[data-testid="stMetricLabel"] > div {{
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
}}

[data-testid="stMetricDelta"] {{
    color: {GREEN} !important;
    font-size: 0.78rem !important;
    font-weight: 600;
}}

/* ───── Botões ───── */
.stButton > button, .stDownloadButton > button, .stLinkButton > a {{
    background: {TEAL} !important;
    color: {NAVY_DEEP} !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
}}

.stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    color: {NAVY_DEEP} !important;
}}

/* ───── DataFrames ───── */
[data-testid="stDataFrame"] {{
    background: rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    border: 1px solid rgba(0, 191, 165, 0.15);
}}

/* Tabs (caso ainda use em algum lugar) */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}}

.stTabs [data-baseweb="tab"] {{
    color: {GRAY} !important;
    border-radius: 6px;
    padding: 8px 18px !important;
}}

.stTabs [aria-selected="true"] {{
    background: {TEAL} !important;
    color: {NAVY_DEEP} !important;
}}

/* ───── Sliders ───── */
.stSlider [data-baseweb="slider"] [role="slider"] {{
    background: {TEAL} !important;
    box-shadow: 0 0 10px rgba(0, 191, 165, 0.5) !important;
}}

.stSlider [data-baseweb="slider"] > div > div {{
    background: {TEAL} !important;
}}

/* ───── Inputs ───── */
.stNumberInput input,
.stTextInput input,
.stTextArea textarea {{
    background: rgba(255, 255, 255, 0.05) !important;
    color: {WHITE} !important;
    border-color: rgba(0, 191, 165, 0.2) !important;
    border-radius: 8px !important;
}}

.stSelectbox [data-baseweb="select"] > div {{
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(0, 191, 165, 0.2) !important;
}}

.stSelectbox [data-baseweb="select"] * {{
    color: {WHITE} !important;
}}

/* Multiselect tags */
.stMultiSelect [data-baseweb="tag"] {{
    background: {TEAL_DIM} !important;
    color: {TEAL} !important;
}}

/* ───── Alerts ───── */
.stAlert {{
    background: rgba(0, 191, 165, 0.06) !important;
    border-left: 3px solid {TEAL} !important;
    border-radius: 0 8px 8px 0 !important;
    color: {GRAY_LT} !important;
}}

/* ───── Componentes CredUp (custom) ───── */
.credup-hero {{
    background: linear-gradient(135deg, {NAVY_MD} 0%, {NAVY_DARK} 100%);
    border: 1px solid rgba(0, 191, 165, 0.18);
    border-radius: 14px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}}

.credup-hero::before {{
    content: "";
    position: absolute;
    top: -40%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,191,165,0.12) 0%, transparent 70%);
    pointer-events: none;
}}

.credup-hero-tag {{
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    color: {TEAL};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    background: {TEAL_DIM};
    padding: 4px 12px;
    border-radius: 20px;
}}

.credup-hero h1 {{
    color: {WHITE} !important;
    margin: 0 0 0.5rem 0 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}}

.credup-hero h1 em {{
    color: {TEAL};
    font-style: normal;
}}

.credup-hero p {{
    color: {GRAY_LT};
    margin: 0 !important;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 720px;
}}

/* Cards de feature */
.credup-card {{
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(0, 191, 165, 0.15);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    backdrop-filter: blur(8px);
    margin-bottom: 0.8rem;
    transition: border-color 0.2s, transform 0.15s;
}}

.credup-card:hover {{
    border-color: {TEAL};
    transform: translateY(-3px);
}}

.credup-card h4 {{
    color: {WHITE} !important;
    margin: 0 0 0.5rem 0 !important;
    font-size: 1rem;
    font-weight: 700;
}}

.credup-card p {{
    color: {GRAY} !important;
    margin: 0 !important;
    font-size: 0.86rem;
    line-height: 1.55;
}}

.credup-icon {{
    width: 42px;
    height: 42px;
    background: {TEAL_DIM};
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
}}

/* Section header com tag */
.credup-section-tag {{
    font-size: 0.75rem;
    font-weight: 700;
    color: {TEAL};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-family: 'Inter', monospace;
}}

/* Badge de fonte */
.credup-badge-fonte {{
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(0, 191, 165, 0.2);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.78rem;
    text-align: center;
    font-weight: 600;
}}

.credup-badge-fonte.oracle {{
    background: rgba(16, 185, 129, 0.12);
    border-color: rgba(16, 185, 129, 0.3);
    color: {GREEN};
}}

.credup-badge-fonte.csv {{
    background: rgba(148, 163, 184, 0.1);
    border-color: rgba(148, 163, 184, 0.25);
    color: {GRAY_LT};
}}

/* Quota row (página Investir) */
.quota-row {{
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}}

.quota-row:last-of-type {{ border-bottom: none; }}

.quota-tier {{
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 1px;
    padding: 6px 12px;
    border-radius: 6px;
    min-width: 100px;
    text-align: center;
    flex-shrink: 0;
}}

.tier-low  {{ background: rgba(16, 185, 129, 0.18); color: {GREEN}; }}
.tier-med  {{ background: rgba(245, 158, 11, 0.18); color: {GOLD}; }}
.tier-high {{ background: rgba(239, 68, 68, 0.18); color: {RED}; }}

.quota-info h5 {{
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0 0 4px 0 !important;
    color: {WHITE} !important;
}}

.quota-info p {{
    font-size: 0.85rem;
    color: {GRAY} !important;
    margin: 0 !important;
    line-height: 1.55;
}}

/* Link cards (portais) */
.invest-link-card {{
    background: {NAVY_MD};
    border: 1px solid rgba(0, 191, 165, 0.2);
    border-radius: 10px;
    padding: 1.2rem;
    text-decoration: none;
    display: block;
    transition: border-color 0.2s, transform 0.15s;
    height: 100%;
}}

.invest-link-card:hover {{
    border-color: {TEAL};
    transform: translateY(-3px);
}}

.invest-link-tag {{
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 4px;
    background: {TEAL_DIM};
    color: {TEAL};
    margin-bottom: 10px;
}}

.invest-link-card h5 {{
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0 0 4px 0 !important;
    color: {WHITE} !important;
}}

.invest-link-card p {{
    font-size: 0.78rem;
    color: {GRAY} !important;
    line-height: 1.5;
    margin: 0 0 10px 0 !important;
}}

.invest-link-arrow {{
    font-size: 0.74rem;
    font-weight: 700;
    color: {TEAL};
}}

/* Disclaimer */
.credup-disclaimer {{
    font-size: 0.84rem;
    color: {GRAY} !important;
    background: rgba(245, 158, 11, 0.06);
    border-left: 3px solid {GOLD};
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    line-height: 1.6;
    margin-top: 1rem;
}}

/* Code/markdown */
code {{
    background: rgba(0, 191, 165, 0.12) !important;
    color: {TEAL} !important;
    padding: 2px 8px !important;
    border-radius: 4px !important;
    font-family: 'Consolas', monospace !important;
    font-size: 0.88em !important;
}}

/* Divider */
hr {{
    border-color: rgba(0, 191, 165, 0.15) !important;
    margin: 2rem 0 !important;
}}

/* ───── Responsivo ───── */
@media (max-width: 768px) {{
    .block-container {{ padding-left: 0.5rem !important; padding-right: 0.5rem !important; }}
    .credup-hero {{ padding: 1.4rem 1.4rem; }}
    .credup-hero h1 {{ font-size: 1.4rem !important; }}
    .credup-hero p {{ font-size: 0.88rem; }}
    [data-testid="stMetricValue"] {{ font-size: 1.3rem !important; }}
    h2 {{ font-size: 1.3rem !important; }}
}}

/* Esconder o "Made with Streamlit" e header padrão */
footer {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="stHeader"] {{ display: none !important; height: 0 !important; }}
.stDeployButton {{ display: none !important; }}
#MainMenu {{ visibility: hidden; }}
.stApp > header[data-testid="stHeader"] {{
    background: {NAVY} !important;
    height: 0 !important;
}}
</style>
"""


def aplicar_tema() -> None:
    """Injeta o CSS global. Chamar logo após `st.set_page_config()` em cada página."""
    st.markdown(_CSS, unsafe_allow_html=True)
