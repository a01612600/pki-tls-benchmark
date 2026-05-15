import pandas as pd
import matplotlib.pyplot as plt

# Leer datos
df = pd.read_csv("../data/cert_sizes_base.csv")

# Calcular eficiencia (bytes por nivel)
df["bytes_per_depth"] = df["chain_bytes"] / df["depth"]
max_row = df.loc[df["bytes_per_depth"].idxmax()]

# Plot
plt.figure(figsize=(8,5))

for algo in df["algo"].unique():
    subset = df[df["algo"] == algo]
    plt.plot(
        subset["depth"],
        subset["bytes_per_depth"],
        marker="o",
        linewidth=2,
        label=algo.upper()
    )

plt.title("Week 2: Chain Size per Depth (Efficiency)")
plt.xlabel("Chain Depth")
plt.ylabel("Average Bytes per Certificate in Chain")
plt.legend()
plt.grid(alpha=0.3)

# Guardar
plt.ylim(550, 1900)
plt.annotate(
    "Highest cost\n(RSA-4096)",
    xy=(max_row["depth"], max_row["bytes_per_depth"]),
    xytext=(max_row["depth"] - 1.0, max_row["bytes_per_depth"] - 120),
    arrowprops=dict(arrowstyle="->"),
    fontsize=10
)
plt.savefig("week2_efficiency.png", dpi=300)
plt.show()