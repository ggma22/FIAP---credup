"""
Página: 💼 Investir
====================
A página principal do produto CredUp para o investidor:
  1. Comparativo FIDC × FII com a mesma régua
  2. Conteúdo educacional sobre FIDC (CVM 175, classes de cota)
  3. Links para portais oficiais onde o investidor pesquisa fundos reais

Sem recomendação de fundos específicos — propósito acadêmico.
"""

import streamlit as st

from frontend.theme import aplicar_tema
from frontend.components import hero, section_tag, disclaimer


st.set_page_config(
    page_title="CredUp · Investir em FIDC e FII",
    page_icon="💼",
    layout="wide",
)
aplicar_tema()


# =====================================================================
hero(
    titulo='Compare <em>FIDC e FII</em> e encontre fundos reais',
    subtitulo=(
        "Tudo o que você precisa saber para escolher entre as duas classes de "
        "ativos, com base nas regras vigentes da CVM e Anbima. "
        "Conteúdo educacional — não constitui recomendação de investimento."
    ),
    tag="// INVESTIR",
)


# =====================================================================
# 1. Comparativo FIDC × FII (núcleo da Sprint 2)
# =====================================================================
section_tag("// 1. FIDC × FII na mesma régua")
st.markdown("### Comparativo lado a lado")
st.caption(
    "Os pontos abaixo são fatos públicos das duas classes — base regulatória CVM, "
    "Anbima e B3. A ideia é que você veja onde cada uma se encaixa no seu portfólio."
)

c_fidc, c_fii = st.columns(2, gap="medium")

with c_fidc:
    st.markdown(
        """
        <div class="credup-card" style="border-left: 4px solid #00BFA5;">
            <div class="credup-icon" style="background: rgba(0,191,165,0.15);">📑</div>
            <h4 style="color: #00BFA5 !important;">FIDC — Fundo de Direitos Creditórios</h4>
            <p style="color: #CBD5E1 !important; margin-bottom: 12px !important;">
                Compra direitos creditórios (duplicatas, contratos, recebíveis).
                A rentabilidade vem do recebimento desses créditos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### Características")
    st.markdown(
        """
        - **Lastro:** direitos creditórios (recebíveis B2B)
        - **Rentabilidade-alvo típica:** CDI + 3% a CDI + 6% a.a. (cotas sênior)
        - **Tributação PF:** tabela regressiva de IR (15% a 22,5%)
        - **FGC:** **não cobre**
        - **Liquidez:** baixa (FIDCs fechados sem resgate; abertos com prazo)
        - **Volatilidade:** baixa (não tem cotação em bolsa)
        - **Acesso para varejo:** liberado desde a Resolução CVM 175 (out/2023),
          apenas em **cotas sênior**
        - **Risco principal:** inadimplência da carteira de recebíveis
        """
    )

with c_fii:
    st.markdown(
        """
        <div class="credup-card" style="border-left: 4px solid #F59E0B;">
            <div class="credup-icon" style="background: rgba(245,158,11,0.15);">🏢</div>
            <h4 style="color: #F59E0B !important;">FII — Fundo de Investimento Imobiliário</h4>
            <p style="color: #CBD5E1 !important; margin-bottom: 12px !important;">
                Investe em imóveis físicos, CRIs ou cotas de outros FIIs.
                A rentabilidade vem de aluguéis e ganho de capital.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### Características")
    st.markdown(
        """
        - **Lastro:** imóveis físicos, CRIs ou cotas de outros FIIs
        - **Rentabilidade-alvo típica:** Dividend Yield ~8% a 12% a.a. + ganho de capital
        - **Tributação PF:** dividendos **isentos de IR**; ganho na venda 20%
        - **FGC:** **não cobre**
        - **Liquidez:** alta (negociado em bolsa, B3)
        - **Volatilidade:** média a alta (cota oscila no mercado)
        - **Acesso para varejo:** livre desde sempre
        - **Risco principal:** vacância, queda de aluguel, oscilação de preço
        """
    )

st.divider()


# Tabela síntese
st.markdown("##### Síntese — quando faz mais sentido cada classe")

st.markdown(
    """
    <table style="width: 100%; border-collapse: collapse; margin-top: 1rem;
                  background: rgba(255,255,255,0.04); border-radius: 10px; overflow: hidden;">
        <thead>
            <tr style="background: rgba(0,191,165,0.1); border-bottom: 1px solid rgba(0,191,165,0.3);">
                <th style="padding: 12px; text-align: left; color: #00BFA5; font-size: 0.85rem;
                           text-transform: uppercase; letter-spacing: 1px;">Critério</th>
                <th style="padding: 12px; text-align: left; color: #00BFA5; font-size: 0.85rem;">FIDC</th>
                <th style="padding: 12px; text-align: left; color: #F59E0B; font-size: 0.85rem;">FII</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px 12px; color: #CBD5E1;">Foco em renda recorrente</td>
                <td style="padding: 10px 12px; color: white;">Sim, com previsibilidade alta</td>
                <td style="padding: 10px 12px; color: white;">Sim, com volatilidade no preço</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px 12px; color: #CBD5E1;">Liquidez para resgate</td>
                <td style="padding: 10px 12px; color: white;">Baixa</td>
                <td style="padding: 10px 12px; color: white;">Alta (B3)</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px 12px; color: #CBD5E1;">Isenção de IR (PF)</td>
                <td style="padding: 10px 12px; color: white;">Não (tabela regressiva)</td>
                <td style="padding: 10px 12px; color: white;">Sim, sobre dividendos</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px 12px; color: #CBD5E1;">Diversificação dentro de RF</td>
                <td style="padding: 10px 12px; color: white;">Excelente — descorrelaciona de Selic/CDI</td>
                <td style="padding: 10px 12px; color: white;">Não é renda fixa</td>
            </tr>
            <tr>
                <td style="padding: 10px 12px; color: #CBD5E1;">Sensibilidade a juros</td>
                <td style="padding: 10px 12px; color: white;">Pós-fixado (acompanha CDI)</td>
                <td style="padding: 10px 12px; color: white;">Inversa (sobe quando juros caem)</td>
            </tr>
        </tbody>
    </table>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

st.info(
    "💡 **Insight CredUp:** as duas classes não competem — se complementam. "
    "Investidores intermediários costumam usar FII para renda mensal recorrente "
    "(via dividendos isentos) e FIDC para diversificar risco em ciclos de juros altos "
    "(rentabilidade-alvo acima do CDI sem volatilidade de mercado)."
)

st.divider()


# =====================================================================
# 2. Educacional sobre FIDC — estrutura de cotas
# =====================================================================
col_a, col_b = st.columns(2, gap="large")

with col_a:
    section_tag("// 2. Estrutura de cotas do FIDC")
    st.markdown("### Como um FIDC organiza investidores")
    st.caption(
        "Um FIDC divide os investidores em classes com prioridades diferentes "
        "no recebimento e absorção de perdas:"
    )

    st.markdown(
        """
        <div class="quota-row">
            <div class="quota-tier tier-low">SÊNIOR</div>
            <div class="quota-info">
                <h5>Cota sênior</h5>
                <p>Maior prioridade no recebimento. Menor risco.
                <strong>Investidor pessoa física só pode adquirir esta classe</strong>,
                segundo a Resolução CVM 175.</p>
            </div>
        </div>
        <div class="quota-row">
            <div class="quota-tier tier-med">MEZANINO</div>
            <div class="quota-info">
                <h5>Cota mezanino</h5>
                <p>Risco intermediário. Restrita a investidores qualificados
                (patrimônio investido ≥ R$ 1 milhão).</p>
            </div>
        </div>
        <div class="quota-row">
            <div class="quota-tier tier-high">SUBORDINADA</div>
            <div class="quota-info">
                <h5>Cota subordinada (júnior)</h5>
                <p>Primeira a absorver perdas da carteira. Maior potencial de retorno
                e maior risco. Geralmente retida pelo originador.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    section_tag("// 3. Enquadramento")
    st.markdown("### Quem pode investir hoje")
    st.caption(
        "A **Resolução CVM 175** (out/2023) abriu FIDCs para o público geral, "
        "desde que cumpridos requisitos estruturais."
    )

    st.markdown(
        """
        - **Investidor de varejo** — pessoa física comum. Pode investir
        nas cotas **sênior** de FIDCs estruturados sob a CVM 175.
        - **Investidor qualificado** — patrimônio investido ≥ R$ 1 milhão.
        Acesso a cotas mezanino.
        - **Investidor profissional** — patrimônio investido ≥ R$ 10 milhões.
        Acesso a todas as classes, incluindo subordinada.
        """
    )

    st.markdown("##### Antes de investir, avalie:")
    st.markdown(
        """
        - Tipo de **recebível** (duplicata, cartão, contratos, agro)
        - **Concentração** dos cedentes na carteira
        - **Subordinação mínima** e provisão para devedores duvidosos (PDD)
        - **Histórico de inadimplência** da carteira
        - **Taxa de administração** e taxa de performance
        - **Liquidez** (FIDC aberto vs fechado)
        """
    )

st.divider()


# =====================================================================
# 4. Onde pesquisar (portais oficiais)
# =====================================================================
section_tag("// 4. Pesquisar fundos disponíveis")
st.markdown("### Portais oficiais e públicos")
st.caption(
    "O CredUp **não recomenda fundos específicos** — somos uma plataforma analítica acadêmica, "
    "não uma corretora. Use os portais abaixo para pesquisar FIDCs e FIIs reais:"
)

p1, p2, p3, p4 = st.columns(4, gap="medium")

with p1:
    st.markdown(
        """
        <a href="https://fidc.com.br/" target="_blank" rel="noopener" class="invest-link-card">
            <div class="invest-link-tag">PORTAL</div>
            <h5>Portal dos FIDCs</h5>
            <p>Conteúdo educacional e listagem geral do mercado de FIDC.</p>
            <span class="invest-link-arrow">fidc.com.br →</span>
        </a>
        """,
        unsafe_allow_html=True,
    )

with p2:
    st.markdown(
        """
        <a href="https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimentos-imobiliarios-fii.htm" target="_blank" rel="noopener" class="invest-link-card">
            <div class="invest-link-tag">B3</div>
            <h5>Listagem de FIIs (B3)</h5>
            <p>Todos os FIIs negociados na B3, com cotações e estatísticas.</p>
            <span class="invest-link-arrow">b3.com.br →</span>
        </a>
        """,
        unsafe_allow_html=True,
    )

with p3:
    st.markdown(
        """
        <a href="https://www.gov.br/cvm/pt-br" target="_blank" rel="noopener" class="invest-link-card">
            <div class="invest-link-tag">CVM</div>
            <h5>Comissão de Valores Mobiliários</h5>
            <p>Regulamento, Resolução 175 e consulta pública de fundos.</p>
            <span class="invest-link-arrow">gov.br/cvm →</span>
        </a>
        """,
        unsafe_allow_html=True,
    )

with p4:
    st.markdown(
        """
        <a href="https://www.anbima.com.br/" target="_blank" rel="noopener" class="invest-link-card">
            <div class="invest-link-tag">ANBIMA</div>
            <h5>Anbima</h5>
            <p>Estatísticas oficiais do mercado de FIDCs e FIIs no Brasil.</p>
            <span class="invest-link-arrow">anbima.com.br →</span>
        </a>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

disclaimer(
    "⚠ <strong>Importante:</strong> esta é uma plataforma acadêmica desenvolvida no contexto do "
    "Challenge FIAP 2025. Não constitui recomendação de investimento. Consulte um assessor "
    "de investimentos credenciado pela CVM antes de aplicar capital. FIDCs envolvem risco de "
    "crédito, FIIs envolvem risco de mercado, e ambos não são cobertos pelo FGC."
)
