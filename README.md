# Mood → Movies

A small full-stack app that recommends movies based on how you're feeling — pick an emotion or just type it in free text, and it pulls real movie details from [OMDb](https://www.omdbapi.com/).

Built to replace a scraping-based script with a proper client/server architecture: a typed FastAPI backend, a real third-party API integration, lightweight NLP for free-text mood detection, and a clean frontend.

## Stack

- **Backend:** FastAPI (Python), Pydantic models, REST endpoints
- **Data source:** OMDb API (no scraping — a real, documented API). Since OMDb has no genre-discovery endpoint, a small curated title catalog (`movie_catalog.py`) maps each mood to a handful of well-known titles per genre, and OMDb is used to fetch live details (poster, rating, plot) for those titles in parallel.
- **NLP:** small keyword-lexicon sentiment/emotion matcher (see `emotion_engine.py`)
- **Frontend:** vanilla HTML/CSS/JS, no build step needed

## Setup

1. **Get a free OMDb API key**
   - Go to http://www.omdbapi.com/apikey.aspx
   - Select the FREE tier, submit your email/name, then activate via the confirmation email
   - Copy your API key

2. **Install dependencies**
```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
```

3. **Configure your API key**
   Create a `.env` file in the project root:
   OMDB_API_KEY=441b5b26

4. **Run it**
```bash
   uvicorn main:app --reload
```
   Open http://localhost:8000

## How it works

1. User picks an emotion button *or* types free text ("had a rough day, feeling drained").
2. If free text: `emotion_engine.detect_emotion_from_text()` scores the text against a keyword lexicon per emotion and picks the best match, with a confidence score.
3. The detected emotion maps to 2–3 genres (e.g. Sad → Drama, Romance) via `emotion_engine.genres_for_emotion()`.
4. `omdb_client.fetch_movies_by_genres()` pulls a shuffled set of curated titles for those genres from `movie_catalog.py`, then fetches live details for each from OMDb in parallel using a thread pool.
5. Results are rendered as poster cards in the frontend.

## Project structure

\`\`\`
mood-movies/
├── main.py              # FastAPI app + routes
├── emotion_engine.py    # emotion definitions + text-based detection
├── omdb_client.py        # OMDb API wrapper
├── movie_catalog.py      # curated title lists per genre
├── requirements.txt
├── .gitignore
└── static/
    ├── index.html
    ├── style.css
    └── script.js
\`\`\`
