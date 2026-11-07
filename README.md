# Pipeline SEMS HPVMG V3

Pipeline treinado com os CSVs FusionSolar e Open-Meteo fornecidos no pacote V2. A V3 usa `GHI(t+1h)` para a energia no intervalo `[t,t+1h)` e calcula o zênite em `t+30 min`. Temperatura e vento permanecem em `t`.

## Conteúdo

- `dados/`: cópias inalteradas dos dois CSVs de entrada.
- `sgie_pipeline.py`, `executar.py` e `prever_21h.py`: preparação, treinamento e inferência.
- `config.json`: candidatos congelados, configuração e novo `run_id`.
- `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/`: logs, buscas, métricas, previsões, diagnósticos e modelos exportados.
- `comparacao_v2_v3/`: métricas pareadas, previsões nos horários comuns e reprodução de referência da V2.
- `PROTOCOLO.md`: definições temporais, filtros e limites de uso.

A execução foi concluída: 40 tarefas, sem erros. O relatório do treinamento está em `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/RESULTADOS_V3.md`; a comparação controlada por timestamps comuns está em `comparacao_v2_v3/COMPARACAO_V2_V3.md`.

## Reproduzir

Use Python 3.12.14 e instale as versões de `requirements.txt`. A partir desta pasta:

```bash
python executar.py --workers 1
```

Use `--workers 6` quando houver recursos disponíveis. O executor valida uma assinatura de código, configuração, dados e ambiente. Para uma nova execução com mudanças, altere `run_id` em `config.json` e preserve a pasta anterior.

## Inferência às 21h

`prever_21h.py` exige 25 timestamps meteorológicos ordenados, de 00h do dia-alvo até 00h do dia seguinte. Temperatura e vento são consumidos em `t`; a GHI é obtida de `t+1h`. Cada linha exige `issued_at` com fuso, não posterior à emissão. Os modelos finais estão em `resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min/FINAL/`.
