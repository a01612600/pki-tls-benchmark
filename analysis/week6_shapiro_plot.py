import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("data/final_dataset.csv")

conditions = [
    ("ec256", 1),
    ("ec384", 4),
    ("rsa2048", 4),
    ("rsa4096", 4),
]

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

for ax, (algo, depth) in zip(axes, conditions):
    subset = df[(df["algo"] == algo) & (df["depth"] == depth)]["handshake_ms"]

    stats.probplot(subset, dist="norm", plot=ax)
    ax.set_title(f"Q-Q Plot: {algo}, depth {depth}")
    ax.grid(alpha=0.3)

plt.suptitle("Normality Check Using Q-Q Plots")
plt.tight_layout()

plt.savefig("analysis/week6_shapiro_qqplots.png", dpi=300, bbox_inches="tight")
plt.savefig("analysis/week6_shapiro_qqplots.pdf", bbox_inches="tight")
plt.show()