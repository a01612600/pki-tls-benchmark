import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/final_dataset.csv")

algorithms = ["ec256", "ec384", "rsa2048", "rsa4096"]

p99 = df["handshake_ms"].quantile(0.99)

df = df[df["handshake_ms"] <= p99]

plt.figure(figsize=(10,6))

for algo in algorithms:

    subset = df[df["algo"] == algo]

    plt.scatter(
        subset["cert_bytes"],
        subset["handshake_ms"],
        alpha=0.25,
        s=15,
        label=algo
    )
    z = np.polyfit(
    subset["cert_bytes"],
    subset["handshake_ms"],
    1)

    p = np.poly1d(z)

    plt.plot(
    subset["cert_bytes"],
    p(subset["cert_bytes"]),
    linewidth=2
    )

plt.xlabel("Certificate Size (bytes)")
plt.ylabel("Handshake Time (ms)")
plt.title("TLS Handshake Latency vs Certificate Size by Algorithm")

plt.legend()
plt.grid(True)

plt.savefig(
    "analysis/week6_latency_vs_certbytes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "analysis/week6_latency_vs_certbytes.pdf",
    bbox_inches="tight"
)

plt.savefig(
    "analysis/week6_latency_vs_certbytes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()