import pandas as pd
import json

# διάβασμα excel
df = pd.read_excel("theses.xlsx")

data = []

for _, row in df.iterrows():

    data.append({
        "professor": str(row["advisor/professor"]),
        "title": str(row["title"]),
        "title2": str(row["title2"])
    })

# αποθήκευση json
with open("theses.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON created successfully")