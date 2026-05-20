from fastapi import FastAPI
import json

app = FastAPI()

with open("theses.json", encoding="utf-8") as f:
    theses = json.load(f)


@app.get("/")
def home():
    return {"message": "UNIWA Thesis API running"}


@app.get("/theses")
def search_theses(professor: str):

    results = []

    for thesis in theses:

        if professor.lower() in str(thesis.get("professor", "")).lower():

            results.append(thesis)

    return {
        "professor": professor,
        "total": len(results),
        "results": results
    }