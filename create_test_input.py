import pandas as pd

source_file = "artifacts/feature_store/validated/validated_test.csv"
output_file = "data/test_input.csv"

df = pd.read_csv(source_file)

# Remove the actual answer.
if "result" in df.columns:
    df = df.drop(columns=["result"])

# Use only 5 records for testing.
df = df.head(5)

df.to_csv(output_file, index=False)

print("Test input created successfully.")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df)