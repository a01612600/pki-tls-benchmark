import pandas as pd

# cargar dataset final
df = pd.read_csv("data/final_dataset.csv")

# resumen estadístico por condición
summary = (
    df.groupby(["algo", "depth"])["handshake_ms"]
    .agg(
        mean="mean",
        median="median",
        std="std",
        p95=lambda x: x.quantile(0.95),
        p99=lambda x: x.quantile(0.99),
        minimum="min",
        maximum="max",
        count="count"
    )
    .reset_index()
)

# coeficiente de variación
summary["cv"] = summary["std"] / summary["mean"]

# redondear
summary = summary.round(4)

# guardar csv
summary.to_csv("data/week6_summary_stats.csv", index=False)

print(summary)

summary.to_latex(
    "analysis/week6_summary_table.tex",
    index=False,
    float_format="%.4f"
)