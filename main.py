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

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.select("a[href*='/handle/11400/']")

        if not links:
            break

        for link in links:

            title = link.text.strip()

            if len(title) > 10:

                theses.append({
                    "title": title,
                    "url": BASE + link["href"]
                })

        offset += 20

    return theses


@app.get("/theses")
def search_theses(keyword: str):

    theses = get_all_theses()

    results = []

    for thesis in theses:

        if keyword.lower() in thesis["title"].lower():

            results.append(thesis)

    return {
        "keyword": keyword,
        "total": len(results),
        "results": results
    }