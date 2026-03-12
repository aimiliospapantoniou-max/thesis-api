from fastapi import FastAPI
import json

app = FastAPI()

with open("theses.json", encoding="utf-8") as f:
    theses = json.load(f)


@app.get("/")
def home():
    return {"message": "UNIWA Thesis API running"}


@app.get("/theses")
def search_theses(keyword: str):

    results = []

    for thesis in theses:
        if keyword.lower() in thesis["title"].lower():
            results.append(thesis)

    return {
        "keyword": keyword,
        "total": len(results),
        "results": results
    }