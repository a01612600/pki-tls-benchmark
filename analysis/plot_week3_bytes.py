import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
df = pd.read_csv("../data/week3_measurements.csv")

# Agrupar para obtener mediana por escenario
summary = (
    df.groupby(["algo", "depth", "cert_bytes"], as_index=False)
      .agg(median_ms=("handshake_ms", "median"))
)

# Orden lógico de algoritmos
algo_order = ["ec256", "ec384", "rsa2048", "rsa4096"]

plt.figure(figsize=(9, 5))

for algo in algo_order:
    subset = summary[summary["algo"] == algo]

    x = subset["cert_bytes"].values
    y = subset["median_ms"].values

    # Scatter (datos reales)
    plt.scatter(
        x,
        y,
        s=80,
        alpha=0.85
    )

    # Regresión lineal
    m, b = np.polyfit(x, y, 1)
    x_line = np.linspace(min(x), max(x), 100)
    y_line = m * x_line + b

    # R²
    y_pred = m * x + b
    r2 = 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))

    plt.plot(
        x_line,
        y_line,
        linestyle="--",
        linewidth=2,
        label=f"{algo.upper()}  (R²={r2:.2f})"
    )

# Estética final
plt.title("Handshake Latency vs Certificate Chain Size", fontsize=14)
plt.xlabel("Certificate Chain Size (bytes)")
plt.ylabel("Median Handshake Time (ms)")
plt.grid(alpha=0.25)

plt.legend(title="Algorithm", frameon=True)

plt.tight_layout()
plt.savefig("week3_bytes_final.png", dpi=300)
plt.show()