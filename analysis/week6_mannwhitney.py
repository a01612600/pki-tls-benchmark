import pandas as pd
from scipy.stats import mannwhitneyu

df = pd.read_csv("data/final_dataset.csv")

comparisons = [
    ("ec256", "rsa2048"),
    ("ec384", "rsa4096"),
    ("ec256", "ec384"),
    ("rsa2048", "rsa4096")
]

results = []

for a1, a2 in comparisons:

    g1 = df[df["algo"] == a1]["handshake_ms"]
    g2 = df[df["algo"] == a2]["handshake_ms"]

    stat, pvalue = mannwhitneyu(g1, g2, alternative="two-sided")

    results.append({
        "algo_1": a1,
        "algo_2": a2,
        "u_statistic": stat,
        "pvalue": pvalue,
        "significant": pvalue < 0.05
    })

results_df = pd.DataFrame(results)

results_df.to_csv("data/week6_mannwhitney.csv", index=False)

print(results_df)

results_df.to_latex(
    "analysis/week6_mannwhitney_table.tex",
    index=False,
    float_format="%.6f"
)