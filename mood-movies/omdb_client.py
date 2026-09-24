"""
Thin client around the OMDb API (omdbapi.com).

OMDb has no "discover by genre" endpoint on the free tier, so the flow is:
1. Look up a handful of curated titles for the chosen genre(s) (see movie_catalog.py)
2. Fetch live details for each title from OMDb (poster, rating, plot, year)

Docs: http://www.omdbapi.com/
Free API key: http://www.omdbapi.com/apikey.aspx
"""
from __future__ import annotations

import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from movie_catalog import CATALOG

OMDB_BASE_URL = "http://www.omdbapi.com/"


class OMDbError(Exception):
    pass


def _api_key() -> str:
    key = os.getenv("OMDB_API_KEY")
    if not key:
        raise OMDbError(
            "OMDB_API_KEY is not set. Copy .env.example to .env and add your "
            "free OMDb API key (see README.md)."
        )
    return key


def _fetch_by_title(title: str, api_key: str) -> dict | None:
    params = {"apikey": api_key, "t": title, "plot": "short"}
    try:
        resp = requests.get(OMDB_BASE_URL, params=params, timeout=8)
        resp.raise_for_status()
    except requests.RequestException:
        return None

    data = resp.json()
    if data.get("Response") != "True":
        return None

    poster = data.get("Poster")
    return {
        "id": data.get("imdbID"),
        "title": data.get("Title"),
        "overview": data.get("Plot"),
        "release_date": data.get("Year"),
        "rating": _safe_float(data.get("imdbRating")),
        "poster_url": poster if poster and poster != "N/A" else None,
    }


def _safe_float(value: str | None) -> float | None:
    try:
        return float(value) if value and value != "N/A" else None
    except ValueError:
        return None


def fetch_movies_by_genres(genres: list[str], limit: int = 12) -> list[dict]:
    """
    Pull a shuffled set of curated titles across the given genre keys,
    then fetch live details for each from OMDb, in parallel.
    """
    api_key = _api_key()  # raises early if missing, before spinning up threads

    titles: list[str] = []
    for genre in genres:
        titles.extend(CATALOG.get(genre, []))

    # de-dupe while keeping order, then shuffle for variety between requests
    seen = set()
    unique_titles = []
    for t in titles:
        if t not in seen:
            seen.add(t)
            unique_titles.append(t)
    random.shuffle(unique_titles)
    unique_titles = unique_titles[:limit]

    if not unique_titles:
        return []

    movies: list[dict] = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(_fetch_by_title, t, api_key): t for t in unique_titles}
        for future in as_completed(futures):
            result = future.result()
            if result:
                movies.append(result)

    return movies