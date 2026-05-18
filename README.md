# FX AI Hub AI Advanced V3

Produto SaaS para inteligência cambial industrial: coleta moedas, cria histórico, prevê tendência com IA/ML, recomenda melhor janela de compra, gera relatório Excel e envia por e-mail/Telegram.

## Principais recursos

- Coleta: USD, EUR, KRW, JPY, CNY, GBP, ARS, BTC contra BRL.
- KPW/Coreia do Norte: incluída como referência manual/alternativa.
- IA avançada leve: ensemble com Linear Regression, Random Forest e Gradient Boosting.
- Indicadores: média móvel, retorno, volatilidade, range alta/baixa.
- Backtesting: MAE, MAPE e score de confiança.
- Agentes: coleta, previsão, recomendação, relatório, e-mail, Telegram e ERP.
- Integração Smart Factory/ERP via API JSON.
- Preparado para vLLM, Transformers, LlamaIndex, LangGraph e DeepEval.

## Execução rápida no VS Code

1. Extraia o ZIP.
2. Abra a pasta no VS Code.
3. Use terminal CMD.
4. Execute:

```bat
scripts\01_setup_backend_windows.bat
scripts\02_run_backend_windows.bat
```

5. Acesse:

```text
http://127.0.0.1:8000/docs
```

## Sequência correta de teste

1. `GET /api/v1/rates/collect`
2. Repita a coleta algumas vezes para formar histórico inicial.
3. `GET /api/v1/ml/forecast-all`
4. `GET /api/v1/recommendations/all`
5. `GET /api/v1/reports/generate`
6. `POST /api/v1/agents/run-enterprise-cycle`

## Relatórios

Os relatórios ficam em:

```text
backend\reports
```

## Observação sobre KPW

KPW foi incluída como moeda monitorável, porém marcada como fonte manual/alternativa e baixa liquidez. Em produção real, valide com fonte financeira contratada.
