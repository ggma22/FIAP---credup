# 🎬 Roteiro do Vídeo Pitch — CredUp Sprint 4

**Duração total**: 5 minutos
**Formato**: gravação de tela do dashboard ao vivo + slides intercalados
**Equipe**: Giovanna · Adelaine · Douglas · Tiago · Victor

---

## Tabela de tempos

| Bloco | Tempo | Quem fala | O que mostra na tela |
|---|---|---|---|
| 1. Abertura e contextualização | 0:00 → 0:30 | Giovanna | Slide 1 (capa) → Slide 2 (desafio) |
| 2. Objetivo | 0:30 → 1:00 | Adelaine | Slide 3 |
| 3. Proposta + arquitetura | 1:00 → 2:00 | Douglas | Slides 4, 5 e 6 |
| 4. Demonstração ao vivo | 2:00 → 4:00 | Tiago e Victor | **Streamlit rodando** |
| 5. Benefícios | 4:00 → 4:30 | Victor | Slide 11 |
| 6. Próximos passos e encerramento | 4:30 → 5:00 | Giovanna | Slide 12 |

---

## Bloco 1 — Abertura e contextualização (0:00–0:30)

> **Giovanna** *(slide 1 → slide 2)*

"Boa tarde! Somos o grupo do projeto **CredUp**, da turma 1TSCP da FIAP.

O mercado de crédito B2B no Brasil — em especial o de duplicatas mercantis e FIDCs — movimenta bilhões por ano, mas é um mercado **opaco e fragmentado**. Cedentes não enxergam o risco real dos seus sacados, gestores de FIDC compram carteira sem visibilidade de concentração, e a inadimplência só aparece **depois** que o estrago aconteceu.

A pergunta que guiou a nossa Sprint 4 foi: e se a gente conseguisse enxergar o risco **antes** do vencimento?"

> 💡 **Dica**: olhar para a câmera nos primeiros 5 segundos da abertura ajuda a engajar.

---

## Bloco 2 — Objetivo do projeto (0:30–1:00)

> **Adelaine** *(slide 3)*

"O objetivo do CredUp é entregar uma plataforma de inteligência analítica que transforma a carteira de duplicatas mercantis em decisão acionável.

A solução é construída sobre **quatro pilares**:

1. **Visibilidade** — KPIs financeiros consolidados em tempo real
2. **Risco** — classificação automática Baixo / Médio / Alto por boleto
3. **Concentração** — quem é o cedente, qual a UF, qual o setor
4. **Decisão** — filtros interativos para apoiar precificação e cobrança

Tudo em um único painel."

---

## Bloco 3 — Proposta de solução e arquitetura (1:00–2:00)

> **Douglas** *(slides 4, 5 e 6)*

"Trabalhamos com duas bases reais que o banco parceiro nos disponibilizou: uma com **7.118 boletos transacionais** vencendo em maio de 2024, totalizando **R$ 165 milhões emitidos**, e outra com indicadores de risco de crédito de **4.612 CNPJs** — incluindo liquidez, score quantitativo e média histórica de atraso.

A arquitetura tem cinco etapas: ingestão dos CSVs, persistência em **Oracle Autonomous Database** na OCI, transformação em pandas, visualização em Streamlit, e a entrega final são filtros interativos para tomada de decisão.

O dashboard organiza os insights em **quatro abas**: visão executiva, análise temporal, risco e concentração, e detalhamento. Tudo construído em Python com Plotly. Vou passar para o Tiago demonstrar."

---

## Bloco 4 — Demonstração ao vivo (2:00–4:00) ⭐ MAIS IMPORTANTE

> **Tiago e Victor** *(Streamlit rodando — alternam a fala)*

### 4.1 — Visão Executiva (2:00–2:30) — Tiago

"Aqui está o **dashboard CredUp rodando no Streamlit, conectado ao Oracle**. Vejam que o badge no canto inferior do sidebar mostra que estamos puxando direto do banco.

No topo, dez KPIs principais. Destaques: **R$ 165 milhões emitidos**, **2,43% de inadimplência por valor**, e olhem este: **25,8% de concentração no top 1 cedente** — uma única empresa concentra um quarto de toda a carteira. Isso é um sinal de risco que normalmente não aparece em relatórios tradicionais.

Logo abaixo, a distribuição da carteira por status: **R$ 129 milhões pagos**, mas também **R$ 27 milhões cancelados pelo cedente** — quase 7 vezes a inadimplência tradicional. Outro insight invisível em relatórios convencionais."

### 4.2 — Análise Temporal (2:30–3:00) — Tiago

*(clica na aba "Análise Temporal")*

"Aqui temos a evolução mensal: barras navy mostram o emitido, linha teal o recebido. A diferença entre as duas é o capital em trânsito. E aqui à direita, a tendência de atraso ao longo do tempo — vemos picos sazonais que ajudam a ajustar a precificação do FIDC."

### 4.3 — Risco e Concentração (3:00–3:30) — Victor

*(clica na aba "Risco & Concentração")*

"Esta é a aba mais analítica. **Top 10 cedentes** com o volume em barra azul e o em aberto em vermelho — dá pra ver instantaneamente quem é grande e quem traz risco proporcional.

E aqui embaixo, a **matriz de risco**: cada bolha é um boleto, posicionado pela liquidez do sacado no eixo X e pelo score quantitativo no Y. Tamanho da bolha = valor. Cores: verde = risco baixo, dourado = médio, vermelho = alto. O quadrante inferior esquerdo concentra os boletos que devem ser priorizados na cobrança."

### 4.4 — Filtros e Detalhamento (3:30–4:00) — Victor

*(usa um filtro no sidebar — ex: marca só "Risco Alto")*

"E todos os filtros são **dinâmicos**. Se eu marco apenas risco alto…" *(seleciona)* "…vejam como os KPIs e gráficos se atualizam instantaneamente. Posso filtrar por UF, mês, status, faixa de valor.

E na última aba, **Detalhamento**, o usuário pode navegar boleto a boleto e exportar o recorte filtrado em CSV — entregando autonomia analítica para o gestor."

---

## Bloco 5 — Benefícios gerados (4:00–4:30)

> **Victor** *(slide 11)*

"Os benefícios práticos: **visão única** da carteira combinando transação e risco; **inadimplência identificada antes** do vencimento; **concentração explícita** por cedente, UF e CNAE; e **apoio direto à precificação** de FIDC e priorização de cobrança.

Para uma PME originadora, isso significa decidir quais clientes cobrar primeiro. Para um gestor de FIDC, significa precificar carteira com base em dados reais, não em intuição."

---

## Bloco 6 — Próximos passos e encerramento (4:30–5:00)

> **Giovanna** *(slide 12)*

"Como próximos passos, queremos evoluir a classificação determinística atual para um **modelo preditivo XGBoost** treinado em histórico de defaults, automatizar a ingestão com Airflow para receber lotes diários do CIP, e adicionar alertas automáticos quando a concentração ultrapassar limites pré-definidos.

O CredUp foi construído sobre uma ideia simples: **inteligência analítica que enxerga risco antes do vencimento**. O dashboard está disponível no link da apresentação, o código-fonte é aberto no GitHub, e o vídeo está aqui no YouTube.

**Obrigado pela atenção, e estamos abertos a perguntas da banca.**"

---

## ⚙️ Notas de produção

### Equipamento

- **Microfone**: qualquer mic USB decente (Blue Yeti, Razer Seiren, ou até fone com microfone funciona). Evite microfone embutido do notebook.
- **Captura**: OBS Studio (gratuito) ou Loom. Loom é mais rápido para uploar direto no YouTube.
- **Resolução**: 1080p mínimo.

### Antes de gravar

- [ ] Testar o dashboard rodando no link público (ou local) **15 minutos antes**.
- [ ] Fazer um filtro no Streamlit ANTES de gravar para "esquentar" o cache.
- [ ] Fechar abas, notificações, Slack, e-mail.
- [ ] Tela cheia (F11 no navegador).
- [ ] Ensaiar 2× completos cronometrando.

### Edição

- Use o **PPT como abertura** (slides 1–6) → corte para **Streamlit ao vivo** (bloco 4) → volta para **PPT** (slides 11–12).
- Música de fundo opcional, suave, sem letra (YouTube Audio Library tem opções gratuitas).
- Legenda em PT-BR ajuda na avaliação da banca.

### Upload no YouTube

- **Privacidade**: "Não listado" (qualquer pessoa com o link assiste, mas não aparece em buscas).
- **Título**: `CredUp — Inteligência Analítica para Crédito B2B (FIAP Sprint 4)`
- **Descrição**: copiar o "Objetivo do projeto" do README + link do dashboard + link do GitHub.
- Após uplodar, **colar o link no slide 12** do PPT antes de exportar a versão final.

---

## ⏱️ Cronômetro de ensaio

Imprima esta tabela e use de guia ao gravar:

```
0:00 ────  abertura          (Giovanna)
0:30 ────  objetivo           (Adelaine)
1:00 ────  proposta + arq.    (Douglas)
2:00 ────  DEMO Visão         (Tiago)
2:30 ────  DEMO Temporal      (Tiago)
3:00 ────  DEMO Risco         (Victor)
3:30 ────  DEMO Filtros       (Victor)
4:00 ────  benefícios         (Victor)
4:30 ────  próximos + close   (Giovanna)
5:00 ────  fim
```

Se passar de 5:00, corte o bloco temporal (3.2) — é o mais sacrificável.
