from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()  # must run before tmdb_client reads TMDB_API_KEY

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from emotion_engine import (
    all_emotions,
    detect_emotion_from_text,
    genres_for_emotion,
    EMOTIONS,
)
from omdb_client import fetch_movies_by_genres, OMDbError

app = FastAPI(title="Mood → Movies", version="1.0.0")


class RecommendRequest(BaseModel):
    emotion: str | None = Field(default=None, description="A key from /api/emotions, e.g. 'happy'")
    text: str | None = Field(default=None, description="Free-text description of how the user feels")


class RecommendResponse(BaseModel):
    detected_emotion: str
    emotion_label: str
    emoji: str
    confidence: float
    source: str  # "button" or "text"
    movies: list[dict]


@app.get("/api/emotions")
def get_emotions():
    return {"emotions": all_emotions()}


@app.post("/api/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    if req.emotion and req.emotion in EMOTIONS:
        emotion_key = req.emotion
        confidence = 1.0
        source = "button"
    elif req.text:
        emotion_key, confidence = detect_emotion_from_text(req.text)
        source = "text"
    else:
        raise HTTPException(status_code=400, detail="Provide either 'emotion' or 'text'.")

    genres = genres_for_emotion(emotion_key)

    try:
        movies = fetch_movies_by_genres(genres)
    except OMDbError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    emotion = EMOTIONS[emotion_key]
    return RecommendResponse(
        detected_emotion=emotion_key,
        emotion_label=emotion.label,
        emoji=emotion.emoji,
        confidence=confidence,
        source=source,
        movies=movies,
    )


# --- Static frontend -------------------------------------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")
