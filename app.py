import os
from PIL import Image
import PIL
from flask import Flask, render_template, request, send_from_directory
from html import escape
from datetime import datetime, timedelta

# Create a Flask web app instance
app = Flask(__name__)

# Constants
ALLOWED_ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ALLOWED_NUMBERS = "123456789"
ALLOWED_SYMBOLS = "?!"
ALLOWED_CHARACTERS = ALLOWED_ALPHABETS + ALLOWED_NUMBERS + ALLOWED_SYMBOLS + ' '

CHARACTER_FOLDER = os.environ.get('CHARACTER_FOLDER', 'Alphabets')
NUMBER_FOLDER = os.environ.get('NUMBER_FOLDER', 'Numbers')
SYMBOLS_FOLDER = os.environ.get('SYMBOLS_FOLDER', 'Symbols')

SPACE_WIDTH = 20

# Define the path for generated images directory
GENERATED_IMAGES_DIR = os.path.join('static', 'Generated_Images')
os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

# Generate a unique filename based on user input and current date and time
def generate_filename(user_input):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_input = user_input.replace(" ", "_").replace("?", "_")
    filename = f"{sanitized_input}_{timestamp}.png"
    return filename

# Get the path of the character image based on the character
def get_character_image_path(char):
    if char in ALLOWED_ALPHABETS:
        return os.path.join('static', CHARACTER_FOLDER, char + '.png')
    elif char in ALLOWED_NUMBERS:
        return os.path.join('static', NUMBER_FOLDER, char + '.png')
    elif char == '!':
        return os.path.join('static', SYMBOLS_FOLDER, 'Exclamation.png')
    elif char == '?':
        return os.path.join('static', SYMBOLS_FOLDER, 'Question.png')
    else:
        raise ValueError(f"The character '{char}' is not supported.")

# Generate an image from the provided text and save it with the provided filename
def generate_image_with_filename(text, filename):
    try:
        sanitized_text = ''.join(char for char in text if char in ALLOWED_CHARACTERS)
        img_height = None
        chars = []

        for char in sanitized_text:
            if char == ' ':
                # Handle spaces by creating a transparent image
                if chars and chars[-1][1] == ' ':
                    continue
                char_img = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
                char_width = SPACE_WIDTH
            else:
                char_img_path = get_character_image_path(char)
                try:
                    with Image.open(char_img_path).convert('RGBA') as char_img:
                        char_size = char_img.size
                        char_width = char_size[0]
                        img_height = char_size[1] if img_height is None else img_height
                except FileNotFoundError as fnfe:
                    raise ValueError(f"Image file not found: {str(fnfe)}")
                except PIL.Image.Error as img_err:
                    raise ValueError(f"Error processing image: {str(img_err)}")
            chars.append((char_img, char_width))

        # Create a composite image by pasting individual character images
        total_width = sum(char_width for _, char_width in chars)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0
        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        # Save the composite image with the provided filename and new path
        img_path = os.path.join(GENERATED_IMAGES_DIR, filename)
        img.save(img_path)

        return filename, None

    except ValueError as ve:
        return None, str(ve)
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    img_path = None
    error_message = None

    if request.method == 'POST':
        text = request.form.get('text', '').upper()
        sanitized_text = escape(text)

        if not sanitized_text:
            error_message = "Please Enter Text."
        else:
            filename = generate_filename(sanitized_text)
            img_path, error_message = generate_image_with_filename(sanitized_text, filename)

    return render_template('index.html', img_path=img_path, error_message=error_message)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/generated_images/<path:filename>')
def serve_generated_images(filename):
    return send_from_directory(GENERATED_IMAGES_DIR, filename)

if __name__ == "__main__":
    app.run()
