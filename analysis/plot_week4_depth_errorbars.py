import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# cargar datos
df = pd.read_csv("../data/week3_measurements.csv")

# agrupar
grouped = df.groupby(["algo", "depth"])["handshake_ms"]

summary = grouped.agg(
    median="median",
    std="std"
).reset_index()

algos = ["ec256", "ec384", "rsa2048", "rsa4096"]

plt.figure(figsize=(10,6))

for algo in algos:
    subset = summary[summary["algo"] == algo]

    plt.errorbar(
        subset["depth"],
        subset["median"],
        yerr=subset["std"],
        marker='o',
        capsize=5,
        label=algo
    )

plt.title("Handshake Latency vs Chain Depth (with Variability)")
plt.xlabel("Chain Depth")
plt.ylabel("Median Handshake Time (ms)")
plt.legend(title="Algorithm")
plt.grid(True)

plt.show()