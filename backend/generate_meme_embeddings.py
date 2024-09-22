import sqlite3
from openai import OpenAI
import json
import os

api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("No API_KEY set for Flask application")


client = OpenAI(api_key=api_key)


# OpenAI API Key

def get_meme_embedding(text):
    response = client.embeddings.create(input=text,
    model="text-embedding-3-small")
    embedding = response.data[0].embedding
    return embedding

def update_meme_embeddings():
    conn = sqlite3.connect('memes.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT meme_id, meme_name, meme_description, meme_intention, meme_example,
               meme_humor_reason, tags, emotional_tone, use_cases
        FROM Memes
    """)
    memes = cursor.fetchall()

    for meme in memes:
        meme_id = meme[0]
        # Combine all textual fields
        text_fields = [str(field) for field in meme[1:] if field]
        combined_text = ' '.join(text_fields)

        # Generate embedding
        embedding = get_meme_embedding(combined_text)

        # Store embedding as JSON string
        embedding_json = json.dumps(embedding)

        # Update the database
        cursor.execute("UPDATE Memes SET embedding = ? WHERE meme_id = ?", (embedding_json, meme_id))
        print(f"Updated embedding for meme_id: {meme_id}")

    conn.commit()
    conn.close()

def add_embedding_column():
    conn = sqlite3.connect('memes.db')
    cursor = conn.cursor()
    # Check if the 'embedding' column already exists
    cursor.execute("PRAGMA table_info(Memes)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'embedding' not in columns:
        cursor.execute("ALTER TABLE Memes ADD COLUMN embedding TEXT")
        conn.commit()
        print("Added 'embedding' column to 'Memes' table.")
    else:
        print("'embedding' column already exists.")
    conn.close()




if __name__ == "__main__":

    add_embedding_column()  # Add this line

    update_meme_embeddings()





































