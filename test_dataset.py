import pandas as pd

df = pd.read_csv("role_skill_mapping.csv")

# Proper table display
print("\nRole–Skill Mapping Dataset\n")
print(df.to_string(index=False))
