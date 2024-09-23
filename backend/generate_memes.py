# generate_memes.py
import numpy
import re
import asyncio
import sqlite3
from openai import AsyncOpenAI
from openai import OpenAI
import os

OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_memes")

api_key = os.getenv('API_KEY')

client = OpenAI(api_key=api_key)
aclient = AsyncOpenAI(api_key=api_key)

import os
import json
import random
from PIL import Image, ImageDraw, ImageFont
# OpenAI API Key

# User input
#user_input = input("Enter your situation or feeling: ")

# Variation prompts inspired by the comedic styles of the funniest individuals
variation_prompts = {
        "1": "In the style of Dave Chappelle's sharp wit, craft a hilarious caption for this meme: '{meme_name}' based on: \"{user_input}\".",
    "2": "Channeling Ellen DeGeneres' relatable humor, write a funny caption for '{meme_name}' inspired by: \"{user_input}\".",
    "3": "Using Kevin Hart's energetic storytelling, create a comedic caption for '{meme_name}' reflecting: \"{user_input}\".",
    "4": "Embodying Tina Fey's clever satire, compose a witty caption for '{meme_name}' that incorporates: \"{user_input}\".",
    "5": "With Jerry Seinfeld's observational humor, generate a funny caption for '{meme_name}' based on: \"{user_input}\".",
    "6": "Inspired by Ricky Gervais' dry humor, craft a humorous caption for '{meme_name}' reflecting: \"{user_input}\".",
    "7": "In the spirit of Amy Schumer's bold comedy, write a hilarious caption for '{meme_name}' using: \"{user_input}\".",
    "8": "Channeling Jim Gaffigan's self-deprecating humor, create a funny caption for '{meme_name}' about: \"{user_input}\".",
    "9": "Using Trevor Noah's global perspective, compose a witty caption for '{meme_name}' inspired by: \"{user_input}\".",
    "10": "Embodying Ali Wong's edgy humor, generate a comedic caption for '{meme_name}' based on: \"{user_input}\".",
    "11": "Inspired by Conan O'Brien's quick wit, craft a funny caption for '{meme_name}' that reflects: \"{user_input}\".",
    "12": "Using John Mulaney's storytelling style, write a humorous caption for '{meme_name}' about: \"{user_input}\".",
    "13": "Channeling Sarah Silverman's satirical edge, create a witty caption for '{meme_name}' based on: \"{user_input}\".",
    "14": "Embodying Bill Burr's candid humor, compose a funny caption for '{meme_name}' reflecting: \"{user_input}\".",
    "15": "With James Corden's playful style, generate a humorous caption for '{meme_name}' inspired by: \"{user_input}\".",
    "16": "Inspired by Leslie Jones' bold comedy, craft a hilarious caption for '{meme_name}' using: \"{user_input}\".",
    "17": "Using Hasan Minhaj's insightful humor, write a witty caption for '{meme_name}' based on: \"{user_input}\".",
    "18": "Channeling Jimmy Fallon's lightheartedness, create a funny caption for '{meme_name}' reflecting: \"{user_input}\".",
    "19": "Embodying Mindy Kaling's relatable humor, compose a comedic caption for '{meme_name}' about: \"{user_input}\".",
    "20": "With Chris Rock's sharp observations, generate a humorous caption for '{meme_name}' inspired by: \"{user_input}\".",
    "21": "Inspired by Robin Williams' improvisational genius, craft a spontaneous caption for '{meme_name}' using: \"{user_input}\".",
    "22": "Using Eddie Murphy's charismatic humor, write a funny caption for '{meme_name}' based on: \"{user_input}\".",
    "23": "Channeling Stephen Colbert's satirical wit, create a clever caption for '{meme_name}' reflecting: \"{user_input}\".",
    "24": "Embodying Ellen DeGeneres' playful teasing, compose a lighthearted caption for '{meme_name}' about: \"{user_input}\".",
    "25": "With George Carlin's critical eye, generate a thought-provoking yet funny caption for '{meme_name}' inspired by: \"{user_input}\".",
    "26": "Inspired by Richard Pryor's candid storytelling, craft a humorous caption for '{meme_name}' using: \"{user_input}\".",
    "27": "Using Wanda Sykes' sharp humor, write a witty caption for '{meme_name}' based on: \"{user_input}\".",
    "28": "Channeling Bo Burnham's musical comedy style, create a rhythmic caption for '{meme_name}' reflecting: \"{user_input}\".",
    "29": "Embodying Iliza Shlesinger's energetic delivery, compose a funny caption for '{meme_name}' about: \"{user_input}\".",
    "30": "With Bill Murray's deadpan humor, generate a comedic caption for '{meme_name}' inspired by: \"{user_input}\".",
    "31": "Inspired by Key and Peele's sketch comedy, craft a creative caption for '{meme_name}' using: \"{user_input}\".",
    "32": "Using Eddie Izzard's surreal humor, write an imaginative caption for '{meme_name}' based on: \"{user_input}\".",
    "33": "Channeling Maria Bamford's quirky style, create a unique caption for '{meme_name}' reflecting: \"{user_input}\".",
    "34": "Embodying Steve Martin's absurdity, compose a humorous caption for '{meme_name}' about: \"{user_input}\".",
    "35": "With Mitch Hedberg's one-liners, generate a concise and funny caption for '{meme_name}' inspired by: \"{user_input}\".",
    "36": "Inspired by Hannibal Buress' laid-back style, craft a cool caption for '{meme_name}' using: \"{user_input}\".",
    "37": "Using Phoebe Waller-Bridge's dark humor, write a witty caption for '{meme_name}' based on: \"{user_input}\".",
    "38": "Channeling Michael Che's sharp commentary, create a clever caption for '{meme_name}' reflecting: \"{user_input}\".",
    "39": "Embodying Kristen Wiig's character comedy, compose a funny caption for '{meme_name}' about: \"{user_input}\".",
    "40": "With Demetri Martin's clever wordplay, generate a pun-filled caption for '{meme_name}' inspired by: \"{user_input}\".",
    "41": "Inspired by Zach Galifianakis' absurdist humor, craft an offbeat caption for '{meme_name}' using: \"{user_input}\".",
    "42": "Using Leslie Nielsen's deadpan style, write a serious but funny caption for '{meme_name}' based on: \"{user_input}\".",
    "43": "Channeling Melissa McCarthy's physical comedy, create an expressive caption for '{meme_name}' reflecting: \"{user_input}\".",
    "44": "Embodying Rowan Atkinson's visual humor, compose a caption for '{meme_name}' that captures: \"{user_input}\".",
    "45": "With Louis C.K.'s candidness, generate a straightforward yet humorous caption for '{meme_name}' inspired by: \"{user_input}\".",
    "46": "Inspired by Catherine Tate's character comedy, craft a witty caption for '{meme_name}' using: \"{user_input}\".",
    "47": "Using Seth Meyers' political satire, write a clever caption for '{meme_name}' based on: \"{user_input}\".",
    "48": "Channeling Eddie Griffin's energetic style, create a lively caption for '{meme_name}' reflecting: \"{user_input}\".",
    "49": "Embodying Margaret Cho's bold humor, compose a daring caption for '{meme_name}' about: \"{user_input}\".",
    "50": "With Gabriel Iglesias' storytelling, generate a funny caption for '{meme_name}' inspired by: \"{user_input}\".",
    "51": "Inspired by Aziz Ansari's modern perspective, craft a relatable caption for '{meme_name}' using: \"{user_input}\".",
    "52": "Using Sarah Millican's charming humor, write a delightful caption for '{meme_name}' based on: \"{user_input}\".",
    "53": "Channeling John Oliver's satirical edge, create a witty caption for '{meme_name}' reflecting: \"{user_input}\".",
    "54": "Embodying Katherine Ryan's fearless comedy, compose a bold caption for '{meme_name}' about: \"{user_input}\".",
    "55": "With Russell Peters' cultural humor, generate a caption for '{meme_name}' inspired by: \"{user_input}\".",
    "56": "Inspired by Jo Koy's family anecdotes, craft a funny caption for '{meme_name}' using: \"{user_input}\".",
    "57": "Using Trevor Noah's insightful comedy, write a thoughtful yet humorous caption for '{meme_name}' based on: \"{user_input}\".",
    "58": "Channeling Tig Notaro's deadpan style, create a subtle caption for '{meme_name}' reflecting: \"{user_input}\".",
    "59": "Embodying Flight of the Conchords' musical humor, compose a lyrical caption for '{meme_name}' about: \"{user_input}\".",
    "60": "With Pete Davidson's candidness, generate a straightforward and funny caption for '{meme_name}' inspired by: \"{user_input}\".",
    "61": "Inspired by Michelle Wolf's sharp wit, craft a biting caption for '{meme_name}' using: \"{user_input}\".",
    "62": "Using Nick Offerman's dry humor, write a stoic but humorous caption for '{meme_name}' based on: \"{user_input}\".",
    "63": "Channeling Hannibal Buress' laid-back delivery, create a relaxed caption for '{meme_name}' reflecting: \"{user_input}\".",
    "64": "Embodying Kristen Schaal's quirky style, compose an eccentric caption for '{meme_name}' about: \"{user_input}\".",
    "65": "With Daniel Tosh's edgy humor, generate a provocative caption for '{meme_name}' inspired by: \"{user_input}\".",
    "66": "Inspired by Jim Carrey's physical comedy, craft an animated caption for '{meme_name}' using: \"{user_input}\".",
    "67": "Using Amy Poehler's improvisational skills, write a spontaneous caption for '{meme_name}' based on: \"{user_input}\".",
    "68": "Channeling Steve Carell's awkward humor, create a cringeworthy yet funny caption for '{meme_name}' reflecting: \"{user_input}\".",
    "69": "Embodying Keegan-Michael Key's character versatility, compose a dynamic caption for '{meme_name}' about: \"{user_input}\".",
    "70": "With Kate McKinnon's inventive style, generate a creative caption for '{meme_name}' inspired by: \"{user_input}\".",
    "71": "Inspired by Michael McIntyre's observational comedy, craft a relatable caption for '{meme_name}' using: \"{user_input}\".",
    "72": "Using Jack Black's exuberant humor, write an over-the-top caption for '{meme_name}' based on: \"{user_input}\".",
    "73": "Channeling Amy Sedaris' eccentric style, create an offbeat caption for '{meme_name}' reflecting: \"{user_input}\".",
    "74": "Embodying Will Ferrell's absurdity, compose a ridiculous yet funny caption for '{meme_name}' about: \"{user_input}\".",
    "75": "With Tiffany Haddish's candid storytelling, generate a humorous caption for '{meme_name}' inspired by: \"{user_input}\".",
    "76": "Inspired by John Cleese's classic British humor, craft a witty caption for '{meme_name}' using: \"{user_input}\".",
    "77": "Using Bob Newhart's subtle style, write a gentle but funny caption for '{meme_name}' based on: \"{user_input}\".",
    "78": "Channeling Lily Tomlin's character work, create a unique caption for '{meme_name}' reflecting: \"{user_input}\".",
    "79": "Embodying Tim Allen's relatable humor, compose a down-to-earth caption for '{meme_name}' about: \"{user_input}\".",
    "80": "With Patton Oswalt's geeky charm, generate a humorous caption for '{meme_name}' inspired by: \"{user_input}\".",
    "81": "Inspired by Joan Rivers' sharp tongue, craft a biting caption for '{meme_name}' using: \"{user_input}\".",
    "82": "Using George Lopez's cultural insights, write a funny caption for '{meme_name}' based on: \"{user_input}\".",
    "83": "Channeling Lucille Ball's classic comedy, create a timeless caption for '{meme_name}' reflecting: \"{user_input}\".",
    "84": "Embodying Adam Sandler's goofy style, compose a silly caption for '{meme_name}' about: \"{user_input}\".",
    "85": "With Jimmy Carr's dark humor, generate an edgy caption for '{meme_name}' inspired by: \"{user_input}\".",
    "86": "Inspired by Bill Hader's impressions, craft a versatile caption for '{meme_name}' using: \"{user_input}\".",
    "87": "Using Mindy Kaling's relatable wit, write a charming caption for '{meme_name}' based on: \"{user_input}\".",
    "88": "Channeling Tim Minchin's musical comedy, create a lyrical caption for '{meme_name}' reflecting: \"{user_input}\".",
    "89": "Embodying Steve Harvey's observational humor, compose a funny caption for '{meme_name}' about: \"{user_input}\".",
    "90": "With Sarah Silverman's satirical edge, generate a bold caption for '{meme_name}' inspired by: \"{user_input}\".",
    "91": "Inspired by Jason Sudeikis' comedic timing, craft a clever caption for '{meme_name}' using: \"{user_input}\".",
    "92": "Using Leslie Jones' energetic humor, write an animated caption for '{meme_name}' based on: \"{user_input}\".",
    "93": "Channeling Cheech and Chong's stoner comedy, create a laid-back caption for '{meme_name}' reflecting: \"{user_input}\".",
    "94": "Embodying Carol Burnett's sketch comedy brilliance, compose a creative caption for '{meme_name}' about: \"{user_input}\".",
    "95": "With Zach Galifianakis' awkward style, generate a humorous yet uncomfortable caption for '{meme_name}' inspired by: \"{user_input}\".",
    "96": "Inspired by Kristen Bell's bubbly personality, craft a cheerful caption for '{meme_name}' using: \"{user_input}\".",
    "97": "Using Aziz Ansari's modern insights, write a relevant caption for '{meme_name}' based on: \"{user_input}\".",
    "98": "Channeling Bill Hader's quirky characters, create an inventive caption for '{meme_name}' reflecting: \"{user_input}\".",
    "99": "Embodying John Candy's lovable humor, compose a heartwarming caption for '{meme_name}' about: \"{user_input}\".",
    "100": "With Eddie Murphy's iconic style, generate a classic yet funny caption for '{meme_name}' inspired by: \"{user_input}\"."
}

# Function to analyze user input
async def analyze_user_input(user_input):
    response = await aclient.chat.completions.create(model="gpt-4o",  # Use "gpt-4" or "gpt-3.5-turbo" if "gpt-4o-mini" is unavailable

    messages=[
        {
            "role": "system",
            "content": (
                "You are an assistant that analyzes text and outputs results strictly in JSON format without any additional text."
            )
        },
        {
            "role": "user",
            "content": (
                f"Analyze the following user input and extract key themes, emotions, and contexts:\n\n"
                f"\"{user_input}\"\n\n"
                "Provide the output ONLY as a JSON object with 'themes', 'emotions', and 'contexts' as keys, each containing a list of relevant words. "
                "Do not include any additional text or explanations."
            )
        }
    ],
    max_tokens=150,
    temperature=0.7 )

    analysis = response.choices[0].message.content.strip()
    print("Analysis response:", repr(analysis))  # Print raw string for debugging
    try:
        analysis_data = json.loads(analysis)
        return analysis_data
    except json.JSONDecodeError as e:
        print("Failed to parse analysis response.")
        print("JSONDecodeError:", e)
        # Attempt to extract JSON from the response using regex
        json_match = re.search(r'\{.*\}', analysis, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            try:
                analysis_data = json.loads(json_text)
                return analysis_data
            except json.JSONDecodeError as e2:
                print("Failed to parse extracted JSON.")
                print("JSONDecodeError:", e2)
                return None
        else:
            print("No JSON object found in the response.")
            return None


# Function to search for relevant memes
import numpy as np

def get_user_embedding(user_input):
    response = client.embeddings.create(input=user_input,
    model="text-embedding-3-small")
    embedding = response.data[0].embedding
    return embedding


def search_memes(user_input):
    # Generate embedding for user input
    user_embedding = get_user_embedding(user_input)

    conn = sqlite3.connect('memes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Memes WHERE embedding IS NOT NULL")
    memes = cursor.fetchall()
    conn.close()

    meme_similarities = []

    for meme in memes:
        meme_embedding_json = meme[-1]  # Assuming 'embedding' is the last column
        meme_embedding = json.loads(meme_embedding_json)

        # Compute cosine similarity
        similarity = cosine_similarity(user_embedding, meme_embedding)
        meme_similarities.append((meme, similarity))

    # Sort by similarity
    meme_similarities.sort(key=lambda x: x[1], reverse=True)

    # Get top N memes
    top_memes = [meme[0] for meme in meme_similarities[:10]]

    return top_memes


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0
    else:
        return dot_product / (norm_a * norm_b)


def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width using font.getbbox."""
    lines = []
    if font.getbbox(text)[2] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words):
                test_line = f"{line}{words[i]} "
                if (font.getbbox(test_line)[2] - font.getbbox(test_line)[0]) <= max_width:
                    line = test_line
                    i += 1
                else:
                    break
            if not line:
                # If a single word is longer than max_width, force it onto the line
                line = words[i]
                i += 1
            lines.append(line.strip())
    return "\n".join(lines)

def get_text_height(text, font):
    """Calculate the total height of the wrapped text."""
    lines = text.split('\n')
    ascent, descent = font.getmetrics()
    line_height = ascent + descent + 4  # Adding spacing
    return len(lines) * line_height

def get_text_width(text, font):
    """Calculate the maximum width among all lines of text."""
    lines = text.split('\n')
    return max((font.getbbox(line)[2] - font.getbbox(line)[0] for line in lines), default=0)

def add_text_to_image(image_path, captions, font_details, output_path, text_positions=None):
    # Open the image
    image = Image.open(image_path).convert('RGBA')
    image_width, image_height = image.size
    txt_layer = Image.new('RGBA', image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    
    # Set default font details
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'impact.ttf')
    
    # Dynamic Font Scaling: Define font size as a percentage of image height
    # For example, 5% of the image height
    default_font_size = font_details.get('size', int(image_height * 0.05))
    
    color = font_details.get('color', '#FFFFFF')
    stroke_width = font_details.get('stroke_width', max(1, int(image_height * 0.005)))  # 0.5% of image height
    stroke_fill = font_details.get('stroke_fill', 'black')
    
    # Set default positions if necessary
    if not text_positions or 'top' not in text_positions or 'bottom' not in text_positions:
        text_positions = {
            'top': {
                'x': 0,
                'y': int(image_height * 0.02),  # 2% from the top
                'max_width': image_width,
            },
            'bottom': {
                'x': 0,
                # Adjusted 'y' to move the text higher by removing the additional +40
                'y': int(image_height - (image_height / 3) + (image_height * 0.02)),
                'max_width': image_width,
                # Increased 'max_height' slightly to allow more space
                'max_height': int(image_height / 3),
                'align_v': 'bottom'
            }
        }
    
    for position_key in ['top', 'bottom']:
        text = captions.get(position_key, '')
        if not text:
            print(f"No text for position '{position_key}', skipping.")
            continue

        position_value = text_positions.get(position_key)
        if not position_value:
            print(f"No position data for '{position_key}', skipping.")
            continue

        x = position_value.get('x', 0)
        y = position_value.get('y', 0)
        max_width = position_value.get('max_width', image_width)
        max_height = position_value.get('max_height', image_height)
        align_v = position_value.get('align_v', position_key)
        
        # **Convert to float if necessary**
        try:
            x = float(x)
            y = float(y)
            max_width = float(max_width)
            max_height = float(max_height)
        except ValueError:
            print(f"Invalid number in text_positions for '{position_key}'. Using default values.")
            x = float(x) if isinstance(x, (int, float)) else 0
            y = float(y) if isinstance(y, (int, float)) else 0
            max_width = float(max_width) if isinstance(max_width, (int, float)) else image_width
            max_height = float(max_height) if isinstance(max_height, (int, float)) else image_height / 3
        
        # Load font with dynamic font size
        font_size = default_font_size
        try:
            font = ImageFont.truetype(font_path, int(font_size))
        except IOError:
            font = ImageFont.load_default()
            print("Font file not found. Using default font.")
        
        # Adjust font size to fit within max_width and max_height
        text_wrapped = wrap_text(text, font, max_width)
        text_height = get_text_height(text_wrapped, font)
        while text_height > max_height and font_size > 10:
            font_size -= 2  # Decrease font size
            try:
                font = ImageFont.truetype(font_path, int(font_size))
            except IOError:
                font = ImageFont.load_default()
                print("Font file not found. Using default font.")
                break
            text_wrapped = wrap_text(text, font, max_width)
            text_height = get_text_height(text_wrapped, font)
        
        # Calculate text width and position
        text_width = get_text_width(text_wrapped, font)
        text_x = x + (max_width - text_width) / 2  # Center horizontally
        text_y = 0  # Initialize
        
        if align_v == 'top':
            text_y = y 
        elif align_v == 'center':
            text_y = y + (max_height - text_height) / 2
        elif align_v == 'bottom':
            text_y = y + (max_height - text_height) 
        else:
            text_y = y  # Default to 'top' alignment
        
        # Ensure text doesn't go beyond the image
        padding = int(image_height * 0.01)  # 1% padding
        if text_y + text_height > image_height - padding:
            text_y = image_height - text_height - padding
        
        # **Ensure text_x and text_y are numbers**
        try:
            text_x = float(text_x)
            text_y = float(text_y)
        except ValueError:
            print(f"Invalid text position for '{position_key}'. Using default positions.")
            text_x = x
            text_y = y
        
        # Debug statements
        print(f"Processing '{position_key}':")
        print(f"  x = {x}, y = {y}, max_width = {max_width}, max_height = {max_height}, align_v = '{align_v}'")
        print(f"  text_x = {text_x}, text_y = {text_y}, font_size = {font_size}")
        
        # Draw text
        draw.multiline_text(
            (text_x, text_y),
            text_wrapped,
            font=font,
            fill=color,
            stroke_width=int(stroke_width),
            stroke_fill=stroke_fill,
            align='center',
            spacing=4
        )
    
    # Combine and save image
    combined = Image.alpha_composite(image, txt_layer).convert('RGB')
    combined.save(output_path)
    print(f"Saved image to {output_path}")


async def generate_captions(meme, user_input, variation_key):
    meme_name = meme[1]
    prompt_template = variation_prompts.get(variation_key)
    prompt_template = prompt_template + f"details about the meme are as follows meme_description: < {meme[2]} > \
                                          meme_intention: < {meme[3]}> \
                                          meme_humor_reason: <{meme[4]}> \
                                          emotional_tone : <{meme[5]}>" 
    if not prompt_template:
        print(f"No prompt found for variation {variation_key}")
        return None

    prompt = prompt_template.format(meme_name=meme_name, user_input=user_input)
    # Append instruction to provide JSON output with 'top' and 'bottom' keys
    prompt += (
        "\n\nPlease provide the caption as a JSON object with 'top' and 'bottom' as keys. "
        "Output only the JSON object without any additional text, explanation, or formatting. "
        "Do not include code blocks or any markdown formatting."
    )

    response = await aclient.chat.completions.create(
        model="gpt-4o",  # Use "gpt-4" or "gpt-3.5-turbo" if "gpt-4o" is unavailable
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.9
    )

    # Extract the assistant's response
    caption_data = response.choices[0].message.content.strip()
    print(f"Assistant's response for meme '{meme_name}' variation {variation_key}:\n{repr(caption_data)}")

    # Attempt to parse the JSON response
    try:
        captions = json.loads(caption_data)
        return captions
    except json.JSONDecodeError:
        # If parsing fails, try to extract JSON using regex
        json_match = re.search(r'\{.*\}', caption_data, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            try:
                captions = json.loads(json_text)
                return captions
            except json.JSONDecodeError as e:
                print(f"Failed to parse extracted JSON for meme: {meme_name} with variation {variation_key}")
                print(f"JSONDecodeError: {e}")
                return None
        else:
            print(f"No JSON object found in the response for meme: {meme_name} with variation {variation_key}")
            return None

async def generate_meme(meme, user_input, variation_key, output_folder):
    try:
        captions = await generate_captions(meme, user_input, variation_key)
        if captions:
            meme_id = meme[0]
            image_filename = os.path.basename(meme[10])
            meme_images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme_images")
            # Construct the relative image path
            image_path = os.path.join(meme_images_folder, image_filename)
            

            #image_path = meme[10]  # Adjust index based on your table structure
            text_positions = json.loads(meme[11]) if meme[11] else {}
            font_details = json.loads(meme[12]) if meme[12] else {}
            output_path = os.path.join(OUTPUT_FOLDER, f"meme_{meme_id}_variation_{variation_key}.jpg")
            
            # Corrected function call
            add_text_to_image(
                image_path=image_path,
                captions=captions,
                font_details=font_details,
                output_path=output_path,
                text_positions=text_positions
            )
            
            print(f"Generated meme saved at {output_path}")
        else:
            print(f"Failed to generate meme for meme_id: {meme[0]} with variation {variation_key}")
    except Exception as e:
        print(f"unable to generate meme prob due to captions exception was {e}")


async def generate_memes_async(user_input):
    memes = search_memes(user_input)
    if memes:
        tasks = []
        variation_keys = list(variation_prompts.keys())
        for meme in memes:
            # Randomly select up to 10 variations per meme
            selected_variations = random.sample(variation_keys, min(10, len(variation_keys)))
            for variation_key in selected_variations:
                try:
                    tasks.append(generate_meme(meme, user_input, variation_key, OUTPUT_FOLDER))
                except Exception as e:
                    print(f"Failed to generate {meme} with variation {variation_key}. Exception: {e}")

        # Limit the number of concurrent tasks to manage API rate limits
        semaphore = asyncio.Semaphore(5)  # Adjust as per your rate limit

        async def semaphore_task(task_coro):
            async with semaphore:
                await task_coro

        await asyncio.gather(*(semaphore_task(task) for task in tasks))
        return True
    else:
        return False


def create_html_gallery(output_folder):
    html_content = "<html><body><h1>Generated Memes</h1>"
    for filename in os.listdir(OUTPUT_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = filename
            html_content += f'<div><img src="{image_path}" alt="{filename}" style="width:400px;"><p>{filename}</p></div>'
    html_content += "</body></html>"
    html_file = os.path.join(OUTPUT_FOLDER, "gallery.html")
    with open(html_file, "w") as f:
        f.write(html_content)
    print(f"Gallery created at {html_file}")

async def main():
    memes = search_memes(user_input)
    if memes:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        tasks = []
        variation_keys = list(variation_prompts.keys())
        for meme in memes:
            # Randomly select a subset of variations to avoid overwhelming API limits
            selected_variations = random.sample(variation_keys, min(10, len(variation_keys)))
            for variation_key in selected_variations:
                try:
                    tasks.append(generate_meme(meme, user_input, variation_key, OUTPUT_FOLDER))
                except Exception as e:
                    print(f"for some reason {meme} didn't generate exception is: {e}")

        # Limit the number of concurrent tasks to manage API rate limits
        semaphore = asyncio.Semaphore(5)  # Adjust as per your rate limit

        async def semaphore_task(task_coro):
            async with semaphore:
                await task_coro

        await asyncio.gather(*(semaphore_task(task) for task in tasks))
        create_html_gallery(OUTPUT_FOLDER)
    else:
        print("No memes found matching your input.")

# Run the script
#if __name__ == "__main__":
#    asyncio.run(main())
