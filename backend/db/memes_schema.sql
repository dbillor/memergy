-- Filename: memes_schema.sql

CREATE TABLE Memes (
    meme_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meme_name TEXT NOT NULL,
    meme_description TEXT NOT NULL,
    meme_intention TEXT NOT NULL,
    meme_example TEXT NOT NULL,
    meme_humor_reason TEXT NOT NULL,
    tags TEXT,                -- Comma-separated tags
    emotional_tone TEXT,
    use_cases TEXT,           -- Comma-separated use cases
    popularity_score INTEGER,
    image_path TEXT,
    text_positions TEXT,      -- JSON string
    font_details TEXT         -- JSON string
);
