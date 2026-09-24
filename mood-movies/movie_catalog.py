"""
OMDb's free tier only supports lookups by exact title or IMDb ID — there's
no "discover movies by genre" endpoint like TMDb has. So we keep a small,
curated list of well-known titles per genre here, and use OMDb purely to
fetch live details (poster, rating, plot, year) for whichever titles we pick.
"""

CATALOG: dict[str, list[str]] = {
    "comedy": [
        "Superbad", "The Grand Budapest Hotel", "Bridesmaids",
        "Superstore", "Step Brothers", "Groundhog Day",
        "The Hangover", "Booksmart",
    ],
    "family": [
        "Paddington 2", "The Incredibles", "Up",
        "Coco", "Toy Story", "Ratatouille",
    ],
    "music": [
        "La La Land", "Whiplash", "Sing Street",
        "Once", "A Star Is Born",
    ],
    "drama": [
        "The Shawshank Redemption", "Manchester by the Sea", "Little Women",
        "Moonlight", "The Pursuit of Happyness", "Good Will Hunting",
    ],
    "romance": [
        "Pride & Prejudice", "About Time", "Notting Hill",
        "The Notebook", "Before Sunrise", "Eternal Sunshine of the Spotless Mind",
    ],
    "action": [
        "Mad Max: Fury Road", "John Wick", "Mission: Impossible - Fallout",
        "The Dark Knight", "Die Hard", "Edge of Tomorrow",
    ],
    "adventure": [
        "Indiana Jones and the Raiders of the Lost Ark", "The Princess Bride",
        "Guardians of the Galaxy", "Life of Pi", "Jumanji",
    ],
    "science_fiction": [
        "Interstellar", "Arrival", "Inception",
        "The Martian", "Blade Runner 2049",
    ],
    "thriller": [
        "Gone Girl", "Prisoners", "Se7en",
        "Parasite", "No Country for Old Men",
    ],
    "crime": [
        "The Departed", "Knives Out", "Pulp Fiction",
        "Zodiac", "The Usual Suspects",
    ],
    "horror": [
        "Get Out", "A Quiet Place", "Hereditary",
        "The Conjuring", "It Follows",
    ],
    "mystery": [
        "Knives Out", "Shutter Island", "Gone Girl",
        "The Prestige", "Zodiac",
    ],
    "fantasy": [
        "The Princess Bride", "Pan's Labyrinth", "Spirited Away",
        "The Shape of Water", "Big Fish",
    ],
    "animation": [
        "Spider-Man: Into the Spider-Verse", "Coco", "Spirited Away",
        "Inside Out", "The Iron Giant",
    ],
    "documentary": [
        "Free Solo", "My Octopus Teacher", "Won't You Be My Neighbor?",
        "13th", "Jiro Dreams of Sushi",
    ],
    "history": [
        "Hidden Figures", "Lincoln", "The Imitation Game",
        "Dunkirk", "Schindler's List",
    ],
}