
from fastapi import FastAPI, Query
import json
import re
import unicodedata
from pathlib import Path

app = FastAPI(
    title="UNIWA Thesis API",
    servers=[{"url": "https://thesis-api-7zdo.onrender.com"}]
)

DATA_FILE = Path(__file__).with_name("theses.json")

with DATA_FILE.open("r", encoding="utf-8") as f:
    theses = json.load(f)


def normalize_name(name: str) -> str:
    """Normalize names for matching: case, accents, punctuation and word order."""
    name = unicodedata.normalize("NFKD", name.casefold())
    name = "".join(
        char for char in name
        if not unicodedata.combining(char)
    )
    name = name.replace("||", " ").replace("//", " ")
    name = re.sub(r"[^\w\s]", " ", name, flags=re.UNICODE)
    words = name.split()
    return " ".join(sorted(words))


def name_matches(requested_name: str, candidate_name: str) -> bool:
    """Match full names exactly or single-word searches against any name part."""
    normalized_requested = normalize_name(requested_name)
    normalized_candidate = normalize_name(candidate_name)

    if normalized_requested == normalized_candidate:
        return True

    requested_words = normalized_requested.split()
    candidate_words = normalized_candidate.split()

    if len(requested_words) == 1:
        return requested_words[0] in candidate_words

    return False


@app.get("/")
def home():
    return {"message": "UNIWA Thesis API running"}


@app.get("/theses")
def search_theses(professor: str = Query(..., min_length=1)):
    requested_name = normalize_name(professor)

    if not requested_name:
        return {"professor": professor, "total": 0, "results": []}

    results = []
    seen = set()

    for thesis in theses:
        names_to_check = [thesis.get("professor", "")]
        names_to_check.extend(thesis.get("aliases", []))

        expanded_names = []
        for name in names_to_check:
            if not isinstance(name, str) or not name.strip():
                continue

            expanded_names.append(name)
            expanded_names.extend(
                part.strip()
                for part in re.split(r"\s*(?://|\|\|)\s*", name)
                if part.strip()
            )

        if any(
            name_matches(professor, name)
            for name in expanded_names
        ):
            row_key = (
                thesis.get("professor"),
                thesis.get("title"),
                thesis.get("title2")
            )

            if row_key not in seen:
                seen.add(row_key)
                results.append({
                    key: value for key, value in thesis.items()
                    if key != "aliases"
                })

    return {
        "professor": professor,
        "total": len(results),
        "results": results
    }

