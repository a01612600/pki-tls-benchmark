import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("../data/week3_measurements.csv")

summary = (
    df.groupby(["algo", "depth"], as_index=False)
      .agg(median_ms=("handshake_ms", "median"))
)

algo_order = ["ec256", "ec384", "rsa2048", "rsa4096"]

plt.figure(figsize=(9,5))

for algo in algo_order:
    subset = summary[summary["algo"] == algo]

    x = subset["depth"].values
    y = subset["median_ms"].values

    # puntos reales
    plt.scatter(x, y, s=80)

    # regresión
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
        label=f"{algo.upper()} (R²={r2:.2f})"
    )

plt.title("Handshake Latency vs Chain Depth")
plt.xlabel("Chain Depth")
plt.ylabel("Median Handshake Time (ms)")
plt.grid(alpha=0.25)
plt.legend(title="Algorithm")

plt.tight_layout()
plt.savefig("week3_depth_final.png", dpi=300)
plt.show()