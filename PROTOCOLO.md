# Protocolo V3: alinhamento temporal de GHI

## Hipótese temporal aplicada

Esta versão implementa a hipótese definida para a análise: cada `SystemProduction` em t representa a energia do intervalo [t,t+1h), e `shortwave_radiation` do Open-Meteo é associado ao intervalo pela marca temporal final. Assim, a entrada de irradiância usada para prever y(t) é GHI(t+1h). Temperatura e vento permanecem no timestamp t, conforme o pacote atual; o alinhamento próprio dessas variáveis não foi alterado nem validado nesta versão.

O zênite é recalculado no ponto médio do intervalo-alvo, t+30 min. O filtro solar continua sendo zênite ≤90°. A implementação registra `GHI_original_same_timestamp`, `GHI_source_timestamp` e `zenite_timestamp` na tabela horária de auditoria.

## Tratamento dos registros acordados

Os dados-fonte FusionSolar e Open-Meteo são mantidos sem alteração. Registros com geração positiva e GHI original igual a zero no mesmo timestamp são marcados como `zero_virtual_ghi_original_zero` e excluídos do ajuste, das métricas e da persistência. Não são reescritos como zero no CSV original. Zeros de geração continuam excluídos conforme a regra da V2.

O CSV Open-Meteo disponível termina em 31/03/2025 às 23h. Como GHI(t+1h) exige 01/04/2025 às 00h para o intervalo final, essa linha fica marcada com GHI alinhada ausente e não participa do ajuste ou das métricas. O restante do conjunto não é deslocado nem descartado por esse limite.

## Treinamento e avaliação

A busca de hiperparâmetros, modelos (KRR, MLP, SVR e XGBoost), sementes, normalização e divisões temporais são herdados da V2. Os resultados da V2 não são carregados nem reutilizados no treinamento V3. A V3 foi executada com novo `run_id`: 40 tarefas concluídas, sem erros. Métricas, previsões, diagnósticos, buscas e modelos exportados estão no diretório `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/`.

O LOMO continua retrospectivo e pode usar meses posteriores ao mês testado. A avaliação cronológica complementar já foi inspecionada anteriormente e não é um conjunto intocado. Dados históricos Open-Meteo não equivalem a previsões meteorológicas arquivadas disponíveis às 21h.

## Contrato da previsão às 21h

Para prever as 24 horas do dia seguinte, `prever_21h.py` exige 25 linhas meteorológicas ordenadas: de 00h do dia-alvo até 00h do dia posterior. Temperatura e vento são lidos em t; GHI é lido em t+1h. Todas as linhas devem conter `issued_at` com fuso e horário não posterior à emissão. A linha adicional fornece a GHI do último intervalo do dia previsto.

## Execução

Use o Python e dependências listadas em `requirements.txt`. A partir desta pasta:

```bash
python executar.py --workers 1
```

Use `--workers 6` se o hardware comportar essa quantidade. A saída é gravada em `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/`. A assinatura registra hashes de dados, configuração e código. A comparação pareada com a V2 reproduzida está documentada em `comparacao_v2_v3/COMPARACAO_V2_V3.md`; o conjunto de horários comuns e as tabelas de métricas acompanham o pacote.
