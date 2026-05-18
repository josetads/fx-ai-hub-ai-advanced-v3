# Arquitetura de IA

## Modelo atual

Ensemble leve e funcional:

- Linear Regression
- Random Forest
- Gradient Boosting

## Features usadas

- índice temporal
- cotação atual
- retorno percentual
- média móvel 3
- média móvel 5
- volatilidade 3
- volatilidade 5
- range alta/baixa

## Métricas

- MAE
- MAPE
- confiança calculada a partir do erro

## Evolução Enterprise

- vLLM para explicações executivas
- Transformers para modelo base
- LlamaIndex para RAG com contratos, políticas de compra e XMLs
- LangGraph para orquestração real dos agentes
- DeepEval para avaliar fidelidade e qualidade das respostas
