import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/final_dataset.csv")

# Filter global extreme outliers only for visualization
p99 = df["handshake_ms"].quantile(0.99)
df_plot = df[df["handshake_ms"] <= p99]

algorithms = ["ec256", "ec384", "rsa2048", "rsa4096"]
data = [df_plot[df_plot["algo"] == algo]["handshake_ms"] for algo in algorithms]

plt.figure(figsize=(10, 6))

plt.boxplot(
    data,
    labels=algorithms,
    showfliers=True
)

plt.title("Handshake Latency Distributions by Algorithm (P99 Filtered)")
plt.xlabel("Algorithm")
plt.ylabel("Handshake Time (ms)")
plt.grid(alpha=0.3)

plt.savefig("analysis/week6_mannwhitney_boxplot_p99.png", dpi=300, bbox_inches="tight")
plt.savefig("analysis/week6_mannwhitney_boxplot_p99.pdf", bbox_inches="tight")
plt.show()