# create_db.py

import sqlite3

def create_database():
    conn = sqlite3.connect('memes.db')
    cursor = conn.cursor()
    with open('memes_schema.sql', 'r') as f:
        schema = f.read()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Database created and schema applied.")

if __name__ == "__main__":
    create_database()

