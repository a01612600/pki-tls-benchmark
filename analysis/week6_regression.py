import pandas as pd
import statsmodels.formula.api as smf

# cargar dataset
df = pd.read_csv("data/final_dataset.csv")

# regresión lineal
model = smf.ols(
    formula="handshake_ms ~ C(algo) + depth",
    data=df
).fit()

# guardar resumen
with open("analysis/week6_regression_summary.txt", "w") as f:
    f.write(model.summary().as_text())

print(model.summary())