# Configuração de E-mail e Telegram

## Gmail

Edite:

```text
backend\.env
```

Configure:

```env
SMTP_ENABLED=true
SMTP_USER=seuemail@gmail.com
SMTP_PASSWORD=sua_senha_de_app_google
EMAIL_TO_LIST=compras@empresa.com,financeiro@empresa.com,fiscal@empresa.com
```

Use senha de app do Google.

## Telegram

```env
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=token_do_bot
TELEGRAM_CHAT_ID=id_do_chat
```

Depois execute:

```text
POST /api/v1/agents/run-enterprise-cycle
```
