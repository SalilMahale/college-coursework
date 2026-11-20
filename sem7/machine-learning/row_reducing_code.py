import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

INPUT_FILE = r"diabetes_binary_5050split_health_indicators_BRFSS2021.csv"
OUTPUT_FILE = "diabetes_clean_10000.csv"

TARGET = "Diabetes_binary"
TOTAL_ROWS = 10000
RANDOM_STATE = 42

df = pd.read_csv(INPUT_FILE)
print("Original shape:", df.shape)

df = df.drop_duplicates().copy()
df = df.dropna().copy()
df = df[df[TARGET].isin([0, 1])].copy()

valid_ranges = {
    "BMI": (10, 100),
    "MentHlth": (0, 30),
    "PhysHlth": (0, 30),
    "GenHlth": (1, 5),
    "Age": (1, 13),
    "Education": (1, 6),
    "Income": (1, 11),
}

for col, (low, high) in valid_ranges.items():
    if col in df.columns:
        df = df[df[col].between(low, high)]

binary_columns = [
    "HighBP","HighChol","CholCheck","Smoker","Stroke","HeartDiseaseorAttack",
    "PhysActivity","Fruits","Veggies","HvyAlcoholConsump","AnyHealthcare",
    "NoDocbcCost","DiffWalk","Sex",
]

for col in binary_columns:
    if col in df.columns:
        df = df[df[col].isin([0, 1])]

feature_cols = [c for c in df.columns if c != TARGET]
conflicting = df.groupby(feature_cols, dropna=False)[TARGET].nunique()
conflicting_keys = conflicting[conflicting > 1].index

if len(conflicting_keys) > 0:
    conflict_index = pd.MultiIndex.from_frame(df[feature_cols]).isin(conflicting_keys)
    df = df.loc[~conflict_index].copy()

df["BMI_bin"] = pd.cut(df["BMI"], bins=[0,18.5,25,30,35,40,np.inf], labels=False, include_lowest=True)
df["Age_bin"] = pd.cut(df["Age"], bins=[0,3,6,9,12,13], labels=False, include_lowest=True)

df["strata"] = (
    df[TARGET].astype(str) + "_" +
    df["BMI_bin"].astype(str) + "_" +
    df["Age_bin"].astype(str) + "_" +
    df["GenHlth"].astype(str) + "_" +
    df["HighBP"].astype(str) + "_" +
    df["HighChol"].astype(str)
)

strata_counts = df["strata"].value_counts()
valid_strata = strata_counts[strata_counts >= 2].index
df = df[df["strata"].isin(valid_strata)].copy()

samples = []
for class_value in [0, 1]:
    class_df = df[df[TARGET] == class_value].copy()
    sampled_class = (
        class_df.groupby("strata", group_keys=False)
        .apply(lambda x: x.sample(
            n=max(1, round(len(x)/len(class_df)*(TOTAL_ROWS//2))) if len(x)>1 else x,
            random_state=RANDOM_STATE
        ))
    )
    target_n = TOTAL_ROWS // 2
    if len(sampled_class) > target_n:
        sampled_class = sampled_class.sample(n=target_n, random_state=RANDOM_STATE)
    elif len(sampled_class) < target_n:
        remaining = class_df.drop(sampled_class.index)
        extra = remaining.sample(n=target_n-len(sampled_class), random_state=RANDOM_STATE)
        sampled_class = pd.concat([sampled_class, extra])
    samples.append(sampled_class)

final_df = pd.concat(samples, ignore_index=True)
final_df = final_df.drop(columns=["BMI_bin","Age_bin","strata"], errors="ignore")
final_df = final_df.sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)

print("\nFinal shape:", final_df.shape)
print("\nClass distribution:")
print(final_df[TARGET].value_counts())
print("\nClass proportions:")
print(final_df[TARGET].value_counts(normalize=True))
print("\nDuplicate rows:", final_df.duplicated().sum())
print("\nMissing values:")
print(final_df.isnull().sum().sum())

final_df.to_csv(OUTPUT_FILE, index=False)
print("\nSaved:", OUTPUT_FILE)
