import pandas as pd
from scipy.stats import shapiro

df = pd.read_csv("data/final_dataset.csv")

results = []

for (algo, depth), group in df.groupby(["algo", "depth"]):

    stat, pvalue = shapiro(group["handshake_ms"].sample(500, random_state=42))

    normal = pvalue > 0.05

    results.append({
        "algo": algo,
        "depth": depth,
        "shapiro_stat": stat,
        "pvalue": pvalue,
        "normal_distribution": normal
    })

results_df = pd.DataFrame(results)

results_df.to_csv("data/week6_normality.csv", index=False)

print(results_df)

results_df.to_latex(
    "analysis/week6_normality_table.tex",
    index=False,
    float_format="%.6f"
)