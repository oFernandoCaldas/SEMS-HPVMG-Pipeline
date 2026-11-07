# Resultados do treinamento V3

## Protocolo executado

- Dados: FusionSolar e Open-Meteo fornecidos no pacote V2, sem alterações nos CSVs originais.
- Período avaliado: 01/08/2024 a 31/03/2025, fuso `America/Sao_Paulo`, 5.832 linhas horárias.
- Hipótese aplicada: `SystemProduction(t)` representa [t,t+1h); a feature de irradiância é `GHI(t+1h)`.
- Zênite: recalculado para o ponto médio, `t+30 min`; filtro mantido em zênite ≤90°.
- Temperatura e vento: mantidos em `t`, sem deslocamento nesta versão.
- Registros positivos com GHI original zero: 185 marcados como zeros virtuais e excluídos sem inspeção individual ou alteração dos dados-fonte.
- Borda do conjunto: 1 intervalo final sem GHI em 01/04/2025 00h, excluído da população elegível.
- Amostras V3: 2.881 elegíveis para ajuste e 2.823 para métricas com persistência 24 h disponível.
- Execução: 40 tarefas concluídas, sem erros; tempo total reportado pelo executor: 490,39 s. Ambiente: Python 3.12.14, scikit-learn 1.8.0, XGBoost 3.0.5, pvlib 0.15.2.

## LOMO agrupado

Cada hora é avaliada no mês retido pela validação LOMO. O protocolo é retrospectivo e pode usar meses posteriores no treino das dobras. Os números abaixo são métricas de teste agrupadas, não o desempenho dos modelos finais reajustados em todos os dados.

| modelo | n | RMSE_kWh | MAE_kWh | R2 | Skill_pct | MBE_kWh |
| --- | --- | --- | --- | --- | --- | --- |
| KRR | 2823 | 0.9978 | 0.6970 | 0.7984 | 40.9401 | -0.0120 |
| MLP | 2823 | 0.9987 | 0.6997 | 0.7980 | 40.8903 | 0.0111 |
| SVR | 2823 | 1.0019 | 0.6844 | 0.7967 | 40.7006 | 0.0220 |
| XGBoost | 2823 | 1.0164 | 0.7235 | 0.7908 | 39.8438 | 0.0028 |
| Persistencia24h | 2823 | 1.6895 | 1.1602 | 0.4219 | 0.0000 | -0.0033 |

A persistência de 24 h teve RMSE de 1,6895 kWh e MAE de 1,1602 kWh nesta população. KRR obteve o menor RMSE entre os modelos (0,9978 kWh), enquanto SVR teve o menor MAE (0,6844 kWh). Não há vencedor único em todas as métricas.

## Resultados por mês

| mes | modelo | n | RMSE_kWh | MAE_kWh | R2 | Skill_pct |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-08 | KRR | 298 | 0.8771 | 0.6337 | 0.6832 | 30.1688 |
| 2024-08 | MLP | 298 | 0.8651 | 0.6272 | 0.6918 | 31.1207 |
| 2024-08 | SVR | 298 | 0.8726 | 0.6142 | 0.6865 | 30.5263 |
| 2024-08 | XGBoost | 298 | 0.9049 | 0.6611 | 0.6628 | 27.9496 |
| 2024-09 | KRR | 287 | 0.8478 | 0.6090 | 0.7993 | 55.0627 |
| 2024-09 | MLP | 287 | 0.8491 | 0.6062 | 0.7987 | 54.9959 |
| 2024-09 | SVR | 287 | 0.8539 | 0.6095 | 0.7964 | 54.7436 |
| 2024-09 | XGBoost | 287 | 0.8526 | 0.6153 | 0.7970 | 54.8084 |
| 2024-10 | KRR | 364 | 0.8474 | 0.6157 | 0.8344 | 49.1992 |
| 2024-10 | MLP | 364 | 0.8465 | 0.6197 | 0.8348 | 49.2562 |
| 2024-10 | SVR | 364 | 0.8535 | 0.6100 | 0.8320 | 48.8335 |
| 2024-10 | XGBoost | 364 | 0.8602 | 0.6236 | 0.8294 | 48.4330 |
| 2024-11 | KRR | 377 | 0.9770 | 0.6919 | 0.7842 | 43.5179 |
| 2024-11 | MLP | 377 | 0.9799 | 0.6998 | 0.7829 | 43.3512 |
| 2024-11 | SVR | 377 | 0.9958 | 0.6982 | 0.7758 | 42.4306 |
| 2024-11 | XGBoost | 377 | 1.0050 | 0.7285 | 0.7716 | 41.8985 |
| 2024-12 | KRR | 401 | 1.2171 | 0.8634 | 0.7309 | 39.7491 |
| 2024-12 | MLP | 401 | 1.2087 | 0.8627 | 0.7346 | 40.1643 |
| 2024-12 | SVR | 401 | 1.2232 | 0.8453 | 0.7282 | 39.4479 |
| 2024-12 | XGBoost | 401 | 1.2248 | 0.8945 | 0.7275 | 39.3675 |
| 2025-01 | KRR | 407 | 1.2404 | 0.8426 | 0.7180 | 22.7552 |
| 2025-01 | MLP | 407 | 1.2466 | 0.8459 | 0.7152 | 22.3702 |
| 2025-01 | SVR | 407 | 1.2457 | 0.8341 | 0.7156 | 22.4264 |
| 2025-01 | XGBoost | 407 | 1.2460 | 0.8684 | 0.7154 | 22.4064 |
| 2025-02 | KRR | 330 | 0.8910 | 0.6372 | 0.8398 | 48.8676 |
| 2025-02 | MLP | 330 | 0.9106 | 0.6608 | 0.8327 | 47.7451 |
| 2025-02 | SVR | 330 | 0.8874 | 0.6083 | 0.8411 | 49.0769 |
| 2025-02 | XGBoost | 330 | 0.9503 | 0.6913 | 0.8178 | 45.4652 |
| 2025-03 | KRR | 359 | 0.8699 | 0.6115 | 0.8173 | 39.3063 |
| 2025-03 | MLP | 359 | 0.8684 | 0.6038 | 0.8180 | 39.4104 |
| 2025-03 | SVR | 359 | 0.8624 | 0.5843 | 0.8205 | 39.8307 |
| 2025-03 | XGBoost | 359 | 0.8859 | 0.6323 | 0.8106 | 38.1935 |

## Teste cronológico complementar

Treino até janeiro/2025 e teste em fevereiro e março/2025, sem atualização dos pesos durante o teste. Este recorte já foi inspecionado anteriormente e é exploratório, não um conjunto externo intocado. Também utiliza meteorologia histórica, não boletins arquivados disponíveis às 21h.

| modelo | n | RMSE_kWh | MAE_kWh | R2 | Skill_pct |
| --- | --- | --- | --- | --- | --- |
| KRR | 689 | 0.8867 | 0.6462 | 0.8285 | 44.1964 |
| MLP | 689 | 0.9038 | 0.6460 | 0.8218 | 43.1200 |
| SVR | 689 | 0.8754 | 0.6040 | 0.8328 | 44.9038 |
| XGBoost | 689 | 0.9251 | 0.6896 | 0.8133 | 41.7765 |
| Persistencia24h | 689 | 1.5889 | 1.0636 | 0.4492 | 0.0000 |

## Estabilidade das sementes

MLP e XGBoost foram reajustados com sementes 17 e 73, mantendo os hiperparâmetros selecionados. As sementes não foram usadas para escolher o melhor resultado.

| modelo | semente | n | RMSE_kWh | MAE_kWh | R2 |
| --- | --- | --- | --- | --- | --- |
| MLP | 42 | 2823 | 0.9987 | 0.6997 | 0.7980 |
| MLP | 17 | 2823 | 1.0033 | 0.7038 | 0.7961 |
| MLP | 73 | 2823 | 1.0052 | 0.7143 | 0.7954 |
| XGBoost | 42 | 2823 | 1.0164 | 0.7235 | 0.7908 |
| XGBoost | 17 | 2823 | 1.0154 | 0.7219 | 0.7912 |
| XGBoost | 73 | 2823 | 1.0174 | 0.7247 | 0.7904 |

## Modelos finais exportados

Os arquivos `.joblib` estão em `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/FINAL/`. `RMSE_treino_kWh` e `MAE_treino_kWh` abaixo descrevem o reajuste final e não são estimativas independentes de generalização. A seleção de hiperparâmetros usa RMSE de validação interna.

| modelo | candidato | RMSE_validacao_interna_kWh | n_treino_final | RMSE_treino_kWh | MAE_treino_kWh |
| --- | --- | --- | --- | --- | --- |
| KRR | 3 | 1.0499 | 2823 | 0.9922 | 0.6874 |
| MLP | 47 | 1.0486 | 2823 | 0.9937 | 0.6919 |
| SVR | 30 | 1.0281 | 2823 | 0.9980 | 0.6787 |
| XGBoost | 157 | 1.0958 | 2823 | 0.9866 | 0.7014 |

Os hiperparâmetros completos estão no `concluido.json` de cada modelo final.

## Artefatos gerados

O diretório do `run_id` contém métricas agrupadas e mensais, previsões por timestamp, cobertura mensal, divisões, busca de hiperparâmetros, diagnósticos, hashes e modelos das rodadas LOMO, cronológica e final. O arquivo `status.json` registra conclusão integral e zero erros.
