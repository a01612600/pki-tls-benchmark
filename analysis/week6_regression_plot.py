import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/final_dataset.csv")

# Filter only extreme outliers for visualization
p99 = df["handshake_ms"].quantile(0.99)
df_plot = df[df["handshake_ms"] <= p99]

algorithms = ["ec256", "ec384", "rsa2048", "rsa4096"]

plt.figure(figsize=(10, 6))

for algo in algorithms:
    subset = df_plot[df_plot["algo"] == algo]

    plt.scatter(
        subset["cert_bytes"],
        subset["handshake_ms"],
        alpha=0.15,
        s=10,
        label=algo
    )

    z = np.polyfit(subset["cert_bytes"], subset["handshake_ms"], 1)
    p = np.poly1d(z)

    x_sorted = np.sort(subset["cert_bytes"].unique())

    plt.plot(
        x_sorted,
        p(x_sorted),
        linewidth=2
    )

plt.xlabel("Certificate Size (bytes)")
plt.ylabel("Handshake Time (ms)")
plt.title("TLS Handshake Latency vs Certificate Size (P99 Filtered)")
plt.legend()
plt.grid(alpha=0.3)

plt.savefig("analysis/week6_regression_scatter_p99.png", dpi=300, bbox_inches="tight")
plt.savefig("analysis/week6_regression_scatter_p99.pdf", bbox_inches="tight")
plt.show()