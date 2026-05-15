import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar resumen CV
df = pd.read_csv("../data/week4_cv_summary.csv")

# Pivot para heatmap
pivot = df.pivot(index="algo", columns="depth", values="cv")

plt.figure(figsize=(8,5))

sns.heatmap(
    pivot,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    cbar_kws={"label": "Coefficient of Variation (CV)"}
)

plt.title("CV Heatmap by Algorithm and Chain Depth")
plt.xlabel("Chain Depth")
plt.ylabel("Algorithm")

plt.tight_layout()
plt.show()