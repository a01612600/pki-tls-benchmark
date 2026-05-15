import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "cert_sizes_base.csv"
output_path = BASE_DIR / "analysis" / "week2_chain_bytes_vs_depth.png"

df = pd.read_csv(csv_path)

plt.figure(figsize=(8, 5))

for algo in df["algo"].unique():
    subset = df[df["algo"] == algo]
    plt.plot(
        subset["depth"],
        subset["chain_bytes"],
        marker="o",
        label=algo
    )

plt.title("Week 2: Certificate Chain Size by Algorithm and Depth")
plt.xlabel("Chain Depth")
plt.ylabel("Chain Size (bytes)")
plt.xticks([1, 2, 3, 4])
plt.grid(True, alpha=0.3)
plt.legend(title="Algorithm")
plt.tight_layout()

plt.savefig(output_path, dpi=300)
plt.show()

print(f"Gráfica guardada en: {output_path}")