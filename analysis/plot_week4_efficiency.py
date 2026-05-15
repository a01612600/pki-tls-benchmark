import pandas as pd
import matplotlib.pyplot as plt

# cargar datos
df = pd.read_csv("../data/week3_measurements.csv")

# agrupar
summary = (
    df.groupby(["algo", "depth", "cert_bytes"], as_index=False)
      .agg(median_ms=("handshake_ms", "median"))
)

# calcular eficiencia
summary["latency_per_kb"] = summary["median_ms"] / (summary["cert_bytes"] / 1024)

# graficar
algo_order = ["ec256", "ec384", "rsa2048", "rsa4096"]

plt.figure(figsize=(9,5))

for algo in algo_order:
    subset = summary[summary["algo"] == algo]

    plt.plot(
        subset["depth"],
        subset["latency_per_kb"],
        marker="o",
        label=algo.upper()
    )

plt.title("Handshake Efficiency (ms per KB) vs Chain Depth")
plt.xlabel("Chain Depth")
plt.ylabel("Latency per KB (ms/KB)")
plt.grid(alpha=0.3)
plt.legend(title="Algorithm")

plt.tight_layout()
plt.savefig("week4_efficiency.png", dpi=300)
plt.show()