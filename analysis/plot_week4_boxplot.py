import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/week3_measurements.csv")
df.columns = df.columns.str.strip()

def filter_p95(data):
    limit = data["handshake_ms"].quantile(0.95)
    return data[data["handshake_ms"] <= limit]

def make_boxplot(family_algos, title, output_name):
    labels = []
    data = []

    for algo in family_algos:
        for depth in [1, 2, 3, 4]:
            subset = df[(df["algo"] == algo) & (df["depth"] == depth)].copy()
            subset = filter_p95(subset)

            data.append(subset["handshake_ms"])
            labels.append(f"{algo}\n{depth}")

    plt.figure(figsize=(10, 5))
    plt.boxplot(data, labels=labels, showfliers=True)

    plt.title(title)
    plt.xlabel("Algorithm and Depth")
    plt.ylabel("Handshake Time (ms)")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_name, dpi=300)
    plt.show()

make_boxplot(
    ["ec256", "ec384"],
    "Handshake Latency Distribution (Elliptic Curve, P95 Filtered)",
    "week4_ec_boxplot_clean.png"
)

make_boxplot(
    ["rsa2048", "rsa4096"],
    "Handshake Latency Distribution (RSA, P95 Filtered)",
    "week4_rsa_boxplot_clean.png"
)