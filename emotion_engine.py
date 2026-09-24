"""
Emotion detection and emotion -> movie genre mapping.

No heavy ML dependency is used on purpose: a small, explainable keyword
lexicon is enough for this use case, keeps the demo fast to boot, and is
easy to explain in an interview ("why didn't you just call an NLP API?").
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass


# TMDb genre IDs: https://developer.themoviedb.org/reference/genre-movie-list
GENRE_IDS = {
    "action": 28,
    "adventure": 12,
    "animation": 16,
    "comedy": 35,
    "crime": 80,
    "documentary": 99,
    "drama": 18,
    "family": 10751,
    "fantasy": 14,
    "history": 36,
    "horror": 27,
    "music": 10402,
    "mystery": 9648,
    "romance": 10749,
    "science_fiction": 878,
    "thriller": 53,
    "war": 10752,
    "western": 37,
}


@dataclass(frozen=True)
class Emotion:
    key: str
    label: str
    emoji: str
    genres: tuple[str, ...]


EMOTIONS: dict[str, Emotion] = {
    "happy": Emotion("happy", "Happy", "😄", ("comedy", "family", "music")),
    "sad": Emotion("sad", "Sad", "😢", ("drama", "romance")),
    "excited": Emotion("excited", "Excited", "🤩", ("action", "adventure", "science_fiction")),
    "angry": Emotion("angry", "Angry", "😠", ("action", "thriller", "crime")),
    "scared": Emotion("scared", "Scared", "😱", ("horror", "thriller", "mystery")),
    "romantic": Emotion("romantic", "Romantic", "🥰", ("romance", "drama")),
    "bored": Emotion("bored", "Bored", "🥱", ("adventure", "comedy", "fantasy")),
    "anxious": Emotion("anxious", "Anxious", "😰", ("comedy", "animation", "family")),
    "nostalgic": Emotion("nostalgic", "Nostalgic", "🥹", ("animation", "family", "history")),
    "relaxed": Emotion("relaxed", "Relaxed", "😌", ("documentary", "animation", "music")),
}

# A small keyword lexicon per emotion, used to score free-text mood input.
# Each entry is checked as a whole-word regex match against the lowercased text.
_KEYWORDS: dict[str, tuple[str, ...]] = {
    "happy": ("happy", "great", "good", "joyful", "cheerful", "glad", "awesome",
              "fantastic", "delighted", "upbeat", "grinning", "smiling", "yay"),
    "sad": ("sad", "down", "depressed", "blue", "heartbroken", "crying", "cry",
            "unhappy", "miserable", "lonely", "grief", "tearful", "gloomy"),
    "excited": ("excited", "pumped", "thrilled", "hyped", "stoked", "can't wait",
                "energized", "amped", "adrenaline", "buzzing"),
    "angry": ("angry", "mad", "furious", "pissed", "rage", "annoyed", "irritated",
              "frustrated", "livid", "fuming"),
    "scared": ("scared", "afraid", "terrified", "frightened", "spooked", "anxious about",
               "nervous", "creeped", "horror", "fear"),
    "romantic": ("romantic", "love", "in love", "crush", "date night", "valentine",
                 "swoon", "affectionate", "loving"),
    "bored": ("bored", "boring", "nothing to do", "restless", "meh", "dull",
              "uninterested", "listless"),
    "anxious": ("anxious", "stressed", "overwhelmed", "worried", "panicking",
                "on edge", "tense", "uneasy"),
    "nostalgic": ("nostalgic", "miss the old days", "childhood", "throwback",
                  "reminisc", "old times", "used to"),
    "relaxed": ("relaxed", "calm", "chill", "peaceful", "mellow", "cozy",
                "unwind", "laid back", "content"),
}

_WORD_RE = {
    emotion: re.compile(r"|".join(re.escape(kw) for kw in kws), re.IGNORECASE)
    for emotion, kws in _KEYWORDS.items()
}


def detect_emotion_from_text(text: str) -> tuple[str, float]:
    """
    Score free-text input against the keyword lexicon.
    Returns (emotion_key, confidence 0..1). Falls back to 'happy' with
    confidence 0.0 when nothing matches, so the API always has something
    to recommend.
    """
    if not text or not text.strip():
        return "happy", 0.0

    scores: Counter[str] = Counter()
    for emotion, pattern in _WORD_RE.items():
        matches = pattern.findall(text)
        if matches:
            scores[emotion] = len(matches)

    if not scores:
        return "happy", 0.0

    top_emotion, top_count = scores.most_common(1)[0]
    total = sum(scores.values())
    confidence = round(top_count / total, 2)
    return top_emotion, confidence


def genre_ids_for_emotion(emotion_key: str) -> list[int]:
    emotion = EMOTIONS.get(emotion_key)
    if not emotion:
        emotion = EMOTIONS["happy"]
    return [GENRE_IDS[g] for g in emotion.genres]


def genres_for_emotion(emotion_key: str) -> list[str]:
    """Genre name strings (e.g. 'comedy', 'drama') for the given emotion,
    used by the OMDb client's curated catalog lookup."""
    emotion = EMOTIONS.get(emotion_key)
    if not emotion:
        emotion = EMOTIONS["happy"]
    return list(emotion.genres)


def all_emotions() -> list[dict]:
    return [
        {"key": e.key, "label": e.label, "emoji": e.emoji}
        for e in EMOTIONS.values()
    ]
