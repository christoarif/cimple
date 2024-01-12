import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import joblib

df = pd.read_csv("data/combineddata_cimple_v3.csv")
df = df.drop_duplicates()
df = pd.concat([df] * 100, ignore_index=True)
df_encoded = pd.get_dummies(df["input"])

X = df_encoded
y = df["target"]

model = LogisticRegression()
model.fit(X, y)

# Save the model
joblib.dump(model, "mapping_model.pkl")
