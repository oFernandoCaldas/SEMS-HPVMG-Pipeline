# Pipeline de treinamento SGIE V3

## Conteúdo do pacote

- `executar.py`, `sgie_pipeline.py`, `sgie_estimators.py`, `config.json` e `requirements.txt`: código e configuração para reproduzir o pipeline.
- `dados/`: os mesmos arquivos FusionSolar e Open-Meteo fornecidos no pacote V2.
- `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/`: métricas, previsões, diagnósticos, buscas e modelos exportados.
- `comparacao_v2_v3/`: reprodução do resultado V2, previsões em timestamps comuns, comparação pareada e intervalos de confiança.
- `Pipeline_SGIE_ROBUSTO_V3.ipynb`: resumo reprodutível e gráficos da análise.
- `graficos/`: figuras estáticas prontas para consulta e apresentação.

## Principais correções metodológicas

A produção horária registrada em `t` foi interpretada como energia do intervalo `[t,t+1h)`. A feature de GHI passou a usar `GHI(t+1h)` e o zênite solar foi recalculado para `t+30 min`. Temperatura e vento permaneceram em `t`. Os 185 registros acordados como zeros virtuais foram excluídos sem inspeção linha a linha ou alteração dos CSVs originais. A última observação, sem GHI correspondente em 01/04/2025 00h, foi excluída.

## Resultados e interpretação

Consulte `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/RESULTADOS_V3.md` e `comparacao_v2_v3/COMPARACAO_V2_V3.md`. A comparação principal é pareada por timestamp e modelo (2.744 horários). O RMSE foi menor na V3 para os quatro modelos, com diferenças V3−V2 entre −0,3189 e −0,3392 kWh; o MAE também diminuiu. A alteração conjunta inclui alinhamento GHI, zênite de ponto médio e regra explícita para zeros virtuais. Portanto, não se atribui isoladamente o ganho ao deslocamento de GHI. LOMO é retrospectivo e não valida previsões day-ahead com meteorologia arquivada disponível no horário de emissão.

## Modelos exportados

Os modelos finais estão em `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/FINAL/{KRR,MLP,SVR,XGBoost}/modelo.joblib`. O exemplo `prever_21h.py` demonstra carregamento e inferência. Para compatibilidade, use o ambiente indicado em `requirements.txt`; os objetos joblib dependem das versões das bibliotecas registradas em `ambiente.json`.

## Execução

Instale as dependências declaradas e execute `python executar.py`. Os resultados desta entrega foram gerados com os dados e parâmetros registrados no pacote. O manifesto `MANIFEST_SHA256_V3.json` lista hashes dos arquivos incluídos.
