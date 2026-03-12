from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

BASE = "https://polynoe.lib.uniwa.gr"
COLLECTION = "https://polynoe.lib.uniwa.gr/xmlui/handle/11400/52"


def get_all_theses():

    offset = 0
    theses = []

    while True:

        url = f"{COLLECTION}?offset={offset}"

        r = requests.get(url)

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