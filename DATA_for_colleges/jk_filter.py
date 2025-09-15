import pandas as pd
import os

# Load full AISHE dataset
df = pd.read_csv("aishe_directory.csv")

# Filter for Jammu & Kashmir
jk_df = df[df["State"].str.contains("Jammu", case=False, na=False)]

# Save filtered data to CSV
jk_df.to_csv("jk_colleges.csv", index=False)

# Save filtered data to JSON
jk_df.to_json("jk_colleges.json", orient="records", indent=4)

print("✅ Jammu & Kashmir colleges saved:")
print("CSV ->", os.path.abspath("jk_colleges.csv"))
print("JSON ->", os.path.abspath("jk_colleges.json"))
