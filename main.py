import pandas as pd

# Citește un fișier Excel
df = pd.read_excel("./abstracts.xlsx")

for _, row in df.iterrows():
    title = row["Title"]
    text = row["Abstract"]
    print(text)
    break
