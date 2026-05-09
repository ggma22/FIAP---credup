# 🚀 Deploy no Streamlit Community Cloud

Guia passo a passo para publicar o CredUp em um link público (`https://[nome].streamlit.app`) conectado ao Oracle Autonomous Database. Tempo estimado: **~15 minutos**.

---

## Pré-requisitos

- Conta GitHub
- Conta Streamlit Community Cloud (gratuita, login com GitHub) — [share.streamlit.io](https://share.streamlit.io)
- Wallet do Oracle Autonomous Database em formato `.zip`
- As tabelas `CREDUP_BOLETOS` e `CREDUP_AUXILIAR` já populadas via `setup_oracle.py`

---

## Passo 1 — Criar o repositório GitHub

```bash
cd EC_Sprint_4_1TSCP_solucaofinal
git init
git add .
git commit -m "Sprint 4 - solução final CredUp"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/credup.git
git push -u origin main
```

> ⚠️ **Antes de fazer push**, confirme que o `.gitignore` está bloqueando `.env`, `secrets.toml` e a wallet:
> ```bash
> git status     # verificar que NÃO aparecem .env / secrets.toml / wallet/
> ```

---

## Passo 2 — Configurar o ACL do Oracle Autonomous DB

O Streamlit Cloud roda em servidores AWS. Você precisa permitir conexões de qualquer IP no Autonomous DB:

**OCI Console** → **Oracle Database** → **Autonomous Database** → seu DB → **More actions** → **Access Control List** → **Edit** → **Allow secure access from everywhere**

> Em produção real, você restringiria por CIDR. Para uso acadêmico, "everywhere" é aceitável e não compromete a segurança porque o acesso ainda exige usuário, senha e wallet.

---

## Passo 3 — Codificar a wallet em base64

A wallet precisa ser embarcada nos secrets do Streamlit. **Mantenha o arquivo `.zip` original**, não o descompacte.

### Linux

```bash
base64 -w 0 wallet_credup.zip > wallet_b64.txt
cat wallet_b64.txt | xclip -selection clipboard   # copia pro clipboard
```

### macOS

```bash
base64 -i wallet_credup.zip | tr -d '\n' | pbcopy
```

### Windows PowerShell

```powershell
$b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("wallet_credup.zip"))
$b64 | Set-Clipboard
```

---

## Passo 4 — Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. **New app** → **From existing repo**
3. Preencha:
   - **Repository**: `SEU_USUARIO/credup`
   - **Branch**: `main`
   - **Main file path**: `dashboard/app.py`
   - **App URL**: escolha um slug (ex: `credup-fiap`) → `https://credup-fiap.streamlit.app`

4. Clique em **Advanced settings** antes de fazer deploy.

---

## Passo 5 — Configurar os Secrets

Em **Advanced settings → Secrets**, cole:

```toml
[oracle]
ORACLE_USER = "ADMIN"
ORACLE_PASSWORD = "SuaSenhaForteAqui_123"
ORACLE_DSN = "credup_medium"
ORACLE_WALLET_PASSWORD = "SenhaDaWallet_456"

# Cole o base64 da wallet aqui (string única, gigantesca):
ORACLE_WALLET_B64 = "PKHcN3YAA...COLE_AQUI..."
```

> O conteúdo dos secrets fica armazenado **apenas no servidor do Streamlit** e nunca é exposto no repositório nem nos logs públicos.

Clique em **Save** e depois **Deploy**.

---

## Passo 6 — Aguardar o build

O primeiro build leva ~3 minutos (instala todas as dependências do `requirements.txt`). Acompanhe pelos logs.

Se tudo der certo, você verá:
- ✅ App URL ativa
- 🟢 Badge "Oracle Autonomous DB" no sidebar do app

---

## Passo 7 — Verificar a publicação

Acesse a URL pública e confirme:
- [ ] App carrega em < 5 segundos
- [ ] Sidebar mostra **🟢 Oracle Autonomous DB** (e não 📄 CSV)
- [ ] KPIs estão preenchidos (`R$ 165,8 mi`, `7.118 boletos`, etc.)
- [ ] Filtros funcionam (selecione um único status e veja KPIs mudarem)
- [ ] Tab "Detalhamento" mostra a tabela completa

---

## Troubleshooting

### O app sobe em modo CSV (badge cinza), e não Oracle

Verifique nos logs (botão **Manage app → Logs**) se aparece algum erro relacionado a `oracledb`. Causas comuns:

- **Wallet inválida**: a string base64 estourou o limite de tamanho dos secrets ou foi colada com quebras de linha. Use `tr -d '\n'` na geração.
- **DSN errado**: o nome do serviço deve ser exatamente como aparece no `tnsnames.ora` da wallet (ex: `credup_medium`, não `credup`).
- **ACL bloqueando**: revise o passo 2.
- **Senha da wallet errada**: ela é a senha que você definiu **ao baixar a wallet** no OCI, não a senha do usuário do banco.

### `oracledb.DatabaseError: ORA-12506`

Endpoints do Autonomous DB são pausados após inatividade no Free Tier. Acesse o OCI Console e clique em **Start** no Autonomous Database.

### `ModuleNotFoundError: No module named 'oracledb'`

O Streamlit Cloud só instala o que está em `requirements.txt`. Confirme que `oracledb>=2.0` está lá.

### Build estoura limite de memória

O Streamlit Free tier tem 1 GB de RAM. Para 7.118 linhas, isso é mais que suficiente. Se aparecer OOM, simplifique os filtros e remova `st.cache_data` temporariamente para diagnóstico.

---

## Atualizações futuras

Cada `git push` para a branch `main` dispara um redeploy automático em ~1 minuto. Os secrets são preservados.

Para mudar secrets sem redeployar: **Manage app → Settings → Secrets**.
