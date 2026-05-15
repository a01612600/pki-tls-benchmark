import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/week3_measurements.csv")

summary = (
    df.groupby(["algo", "depth"], as_index=False)
      .agg(median_ms=("handshake_ms", "median"))
)

pivot = summary.pivot(index="depth", columns="algo", values="median_ms")

pivot = pivot[["ec256", "ec384", "rsa2048", "rsa4096"]]

pivot.plot(
    kind="bar",
    figsize=(9,5),
    edgecolor='black',
    linewidth=0.5,
    width=0.8
)

plt.title("Handshake Latency by Algorithm and Chain Depth")
plt.xlabel("Chain Depth")
plt.ylabel("Median Handshake Time (ms)")
ax = plt.gca()  # obtener el eje actual

for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.2f}",
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='bottom',
        fontsize=8
    )
    
plt.xticks(rotation=0)
plt.grid(axis="y", alpha=0.85)
plt.legend(title="Algorithm")

plt.tight_layout()
plt.savefig("week3_bar.png", dpi=300)
plt.show()