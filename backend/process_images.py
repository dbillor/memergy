import base64
from openai import OpenAI
import requests
import sqlite3
import json
import os
from PIL import Image

# OpenAI API Key
api_key = os.getenv("API_KEY")

meme_folder= os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme_images")


def initialize_database():
    conn = sqlite3.connect('memes.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Memes (
        meme_id INTEGER PRIMARY KEY AUTOINCREMENT,
        meme_name TEXT,
        meme_description TEXT,
        meme_intention TEXT,
        meme_example TEXT,
        meme_humor_reason TEXT,
        tags TEXT,
        emotional_tone TEXT,
        use_cases TEXT,
        popularity_score INTEGER,
        image_path TEXT,
        text_positions TEXT,
        font_details TEXT
    )
    ''')
    conn.commit()
    conn.close()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to call GPT-4o-mini Vision API
def describe_image(image_base64):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze the meme image provided and output a JSON object with the following keys: meme_name, meme_description, meme_intention, meme_example, meme_humor_reason, tags (comma-separated string), emotional_tone, use_cases (comma-separated string), popularity_score (integer 1-100), text_positions (JSON), font_details (JSON). The text_positions and font_details should be appropriate for overlaying text on the meme."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
       

        if response.status_code == 200:
            response_json = response.json()
            content = response_json['choices'][0]['message']['content']
            return content
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

# Function to insert meme data into the database
def insert_meme_into_db(meme_data):
    conn = sqlite3.connect('memes.db')
    cursor = conn.cursor()
    sql = '''
    INSERT INTO memes (
        meme_name, meme_description, meme_intention, meme_example, meme_humor_reason,
        tags, emotional_tone, use_cases, popularity_score, image_path, text_positions, font_details
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(sql, (
        meme_data.get('meme_name'),
        meme_data.get('meme_description'),
        meme_data.get('meme_intention'),
        meme_data.get('meme_example'),
        meme_data.get('meme_humor_reason'),
        meme_data.get('tags'),
        meme_data.get('emotional_tone'),
        meme_data.get('use_cases'),
        meme_data.get('popularity_score'),
        meme_data.get('image_path'),
        meme_data.get('text_positions'),
        meme_data.get('font_details')
    ))
    conn.commit()
    conn.close()

# Function to process a single image
def process_image(image_path):
    base64_image = encode_image(image_path)
    description = describe_image(base64_image)
    print("Raw API response:")
    print(description)
    if description:
        # Remove any code block markers and language specifiers
        sanitized_description = description.strip('`').strip()
        if sanitized_description.startswith('json'):
            sanitized_description = sanitized_description[4:].strip()

        try:
            meme_data = json.loads(sanitized_description)
            meme_data['image_path'] = image_path  # Add the image path
            # Ensure text_positions and font_details are stored as JSON strings
            if isinstance(meme_data.get('text_positions'), dict):
                meme_data['text_positions'] = json.dumps(meme_data['text_positions'])
            if isinstance(meme_data.get('font_details'), dict):
                meme_data['font_details'] = json.dumps(meme_data['font_details'])
            insert_meme_into_db(meme_data)
            print(f"Successfully inserted meme: {meme_data.get('meme_name')}")
        except json.JSONDecodeError as e:
            print(f"Failed to parse GPT-4o-mini response for image: {image_path}")
            print(f"JSONDecodeError: {e}")
            print(f"Response content:\n{description}")
    else:
        print(f"Failed to get a description from GPT-4o-mini for image: {image_path}")

# Function to process all images in a directory
def process_all_images(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(directory, filename)
            print(f"Processing {image_path}...")
            process_image(image_path)

# Main execution
if __name__ == "__main__":
    initialize_database() 
    process_all_images(meme_folder)


































































































































































































