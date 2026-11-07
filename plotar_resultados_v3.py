from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
COMP = ROOT / "comparacao_v2_v3"
RES = ROOT / "resultados/robusto_v3_ghi_tmais1h_zenite_tmais30min"
OUT = ROOT / "graficos"
OUT.mkdir(exist_ok=True)

# Comparação pareada: mesmos timestamps para V2 e V3.
df = pd.read_csv(COMP / "metricas_lomo_pareadas.csv")
models = df["modelo"].tolist()
for metric, title, fname in [("RMSE", "RMSE pareado por modelo", "comparacao_rmse_pareada.png"), ("MAE", "MAE pareado por modelo", "comparacao_mae_pareada.png")]:
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    x = range(len(models)); width = .36
    ax.bar([i-width/2 for i in x], df[f"{metric}_V2_kWh"], width, label="V2", color="#8293a5")
    ax.bar([i+width/2 for i in x], df[f"{metric}_V3_kWh"], width, label="V3", color="#168c83")
    ax.set_xticks(list(x), models); ax.set_ylabel(f"{metric} (kWh)"); ax.set_title(title + " (2.744 horários comuns)")
    ax.grid(axis="y", alpha=.25); ax.legend(frameon=False); fig.tight_layout(); fig.savefig(OUT/fname, dpi=180); plt.close(fig)

metrics = pd.read_csv(RES / "metricas_lomo_agrupadas.csv")
fig, ax = plt.subplots(figsize=(8.4, 4.8))
ax.bar(metrics["modelo"], metrics["RMSE_kWh"], color="#168c83", label="Modelo V3")
ax.axhline(metrics["RMSE_persistencia_kWh"].iloc[0], color="#d97706", ls="--", label="Persistência 24 h")
ax.set_ylabel("RMSE (kWh)"); ax.set_title("LOMO V3 agrupado (2.823 horários)"); ax.grid(axis="y", alpha=.25); ax.legend(frameon=False); fig.tight_layout(); fig.savefig(OUT/"rmse_lomo_v3.png", dpi=180); plt.close(fig)

monthly = pd.read_csv(RES / "metricas_lomo_mensais.csv")
pivot = monthly.pivot(index="mes", columns="modelo", values="RMSE_kWh")
fig, ax = plt.subplots(figsize=(10, 5.3))
pivot.plot(ax=ax, marker="o", linewidth=1.7); ax.set_ylabel("RMSE (kWh)"); ax.set_xlabel("Mês retido"); ax.set_title("RMSE mensal por modelo, validação LOMO V3"); ax.grid(alpha=.25); ax.legend(frameon=False, ncol=2); fig.tight_layout(); fig.savefig(OUT/"rmse_mensal_lomo_v3.png", dpi=180); plt.close(fig)
print(f"Gráficos salvos em {OUT}")
