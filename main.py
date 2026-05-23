from fastapi import FastAPI
import json

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


@app.get("/")
def home():
    return {"message": "UNIWA Thesis API running"}


@app.get("/theses")
def search_theses(professor: str):

    results = []

    for thesis in theses:

        if professor.lower() in thesis["professor"].lower():

            results.append(thesis)

    return {
        "professor": professor,
        "total": len(results),
        "results": results
    }