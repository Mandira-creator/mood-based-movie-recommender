# Mood → Movies

A small full-stack app that recommends movies based on how you're feeling —
pick an emotion or just type it in free text, and it pulls real, well-rated
recommendations from [TMDb](https://www.themoviedb.org/).

Built to replace a scraping-based script with a proper client/server
architecture: a typed FastAPI backend, a real third-party API integration,
lightweight NLP for free-text mood detection, and a clean frontend.

## Stack

- **Backend:** FastAPI (Python), Pydantic models, REST endpoints
- **Data source:** TMDb Discover API (no scraping — a real, documented API)
- **NLP:** small keyword-lexicon sentiment/emotion matcher (see `emotion_engine.py`)
- **Frontend:** vanilla HTML/CSS/JS, no build step needed

## Setup

1. **Get a free TMDb API key**
   - Create an account at https://www.themoviedb.org/
   - Go to Settings → API → request an API key (choose "Developer")
   - Copy the "API Key (v3 auth)" value

2. **Install dependencies**
   ```bash
   cd mood-movies
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # then edit .env and paste your key:
   # TMDB_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. **Run it**
   ```bash
   uvicorn main:app --reload
   ```
   Open http://localhost:8000

## How it works

1. User picks an emotion button *or* types free text ("had a rough day, feeling drained").
2. If free text: `emotion_engine.detect_emotion_from_text()` scores the text
   against a keyword lexicon per emotion and picks the best match, with a
   confidence score.
3. The detected emotion maps to 2–3 TMDb genre IDs (e.g. Sad → Drama, Romance).
4. `tmdb_client.fetch_movies_by_genres()` calls TMDb's `/discover/movie`
   endpoint, filtered to popular, well-rated titles.
5. Results are rendered as poster cards in the frontend.

## Project structure

```
mood-movies/
├── main.py              # FastAPI app + routes
├── emotion_engine.py     # emotion definitions + text-based detection
├── tmdb_client.py         # TMDb API wrapper
├── requirements.txt
├── .env.example
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

## Talking points for interviews / resume

- Replaced brittle HTML scraping with a documented third-party REST API
  (handles auth, rate limits, and structured JSON instead of parsing HTML).
- Clean separation of concerns: API client, NLP/matching logic, and web
  layer are in separate modules, each independently testable.
- Typed request/response models with Pydantic — the API is self-documenting
  at `/docs` (FastAPI's auto-generated Swagger UI).
- Graceful error handling: missing API key, upstream API failures, and
  empty results all degrade gracefully instead of crashing.

## Possible extensions

- Swap the keyword lexicon for a real sentiment model (e.g. a small
  HuggingFace transformer) and compare accuracy/latency trade-offs.
- Add a "watchlist" with a database (SQLite) and user accounts.
- Deploy (Render/Fly.io/Railway) and add the live link to your resume.
- Add automated tests (pytest) for `emotion_engine.py` and API routes.
