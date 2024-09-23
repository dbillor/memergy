# app.py

import os
import asyncio
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from backend.generate_memes import generate_memes_async, OUTPUT_FOLDER

app = Flask(__name__)

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize visitor counter
COUNTER_FILE = os.path.join(OUTPUT_FOLDER, 'counter.txt')

def increment_counter():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'w') as f:
            f.write('0')
    with open(COUNTER_FILE, 'r+') as f:
        try:
            count = int(f.read())
        except ValueError:
            count = 0
        count += 1
        f.seek(0)
        f.write(str(count))
    return count

@app.route('/', methods=['GET', 'POST'])
def index():
    # Increment visitor count on each GET request
    visitor_count = increment_counter()

    if request.method == 'POST':
        user_input = request.form.get('prompt')
        if user_input:
            try:
                # Run the asynchronous meme generation
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                success = loop.run_until_complete(generate_memes_async(user_input))
                loop.close()
                if success:
                    return redirect(url_for('gallery'))
                else:
                    error_message = "No memes found matching your input."
                    return render_template('index.html', error=error_message, visitor_count=visitor_count)
            except Exception as e:
                error_message = f"An error occurred: {e}"
                return render_template('index.html', error=error_message, visitor_count=visitor_count)
    return render_template('index.html', visitor_count=visitor_count)

@app.route('/gallery')
def gallery():
    try:
        images = [
            filename for filename in os.listdir(OUTPUT_FOLDER)
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        ]
        return render_template('gallery.html', images=images)
    except Exception as e:
        error_message = f"Failed to load gallery: {e}"
        return render_template('gallery.html', error=error_message)

# Route to serve generated memes
@app.route('/generated_memes/<filename>')
def generated_memes(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)

















































































































































































































































