import pandas as pd
import numpy as np

df = pd.read_csv("../data/week3_measurements.csv")

summary = df.groupby(["algo", "depth"])["handshake_ms"].agg(
    mean="mean",
    std="std",
    median="median"
).reset_index()

summary["cv"] = summary["std"] / summary["mean"]

def classify(cv):
    if cv < 0.15:
        return "OK"
    elif cv < 0.20:
        return "Borderline"
    else:
        return "High Variability"

summary["status"] = summary["cv"].apply(classify)

print(summary)

summary.to_csv("../data/week4_cv_summary.csv", index=False)