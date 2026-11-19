from fastapi import FastAPI
import json
import re
import unicodedata

app = FastAPI(
    title="UNIWA Thesis API",
    servers=[
        {
            "url": "https://thesis-api-7zdo.onrender.com"
        }
    ]
)

with open("theses.json", "r", encoding="utf-8") as f:
    theses = json.load(f)


def normalize_name(name: str) -> str:
    name = name.lower().strip()

    # Αφαίρεση τόνων και διακριτικών
    name = unicodedata.normalize("NFKD", name)
    name = "".join(
        char for char in name
        if not unicodedata.combining(char)
    )

    # Αντικατάσταση σημείων στίξης με κενά
    name = re.sub(r"[^\w\s]", " ", name)

    # Κανονικοποίηση κενών
    words = name.split()

    # Ίδια σειρά λέξεων ανεξάρτητα από τη σειρά εισαγωγής
    return " ".join(sorted(words))


@app.get("/")
def home():
    return {"message": "UNIWA Thesis API running"}


@app.get("/theses")
def search_theses(professor: str):

    results = []

    requested_name = normalize_name(professor)

    for thesis in theses:

        stored_name = normalize_name(thesis["professor"])

        if requested_name == stored_name:
            results.append(thesis)

    return {
        "professor": professor,
        "total": len(results),
        "results": results
    }
