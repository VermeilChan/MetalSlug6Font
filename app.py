import os
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)

# Define allowed character sets
ALLOWED_ALPHABETS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALLOWED_NUMBERS = "123456789"
ALLOWED_SYMBOLS = "?!"
ALLOWED_CHARACTERS = ALLOWED_ALPHABETS + ALLOWED_NUMBERS + ALLOWED_SYMBOLS

# Folder names
SYMBOLS_FOLDER = 'Symbols'
CHARACTER_FOLDER = 'Alphabets'
NUMBER_FOLDER = 'Numbers'

# Dimensions
SPACE_WIDTH = 10
GENERATED_IMAGE_PATH = 'result.png'

def generate_image(text):
    try:
        # Sanitize input text
        sanitized_text = ''.join(char for char in text if char in ALLOWED_CHARACTERS)

        img_height = None
        chars = []

        for char in sanitized_text:
            if char == ' ':
                if chars and chars[-1][1] == ' ':
                    continue
                # Create space image for formatting
                char_img = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
                char_width = SPACE_WIDTH
            else:
                # Get image path for the character
                char_img_path = get_character_image_path(char)
                with Image.open(char_img_path).convert('RGBA') as char_img:
                    char_size = char_img.size
                    char_width = char_size[0]
                    img_height = char_size[1] if img_height is None else img_height
            chars.append((char_img, char_width))

        # Combine character images into a single image
        total_width = sum(char_width for _, char_width in chars)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0
        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        # Save the combined image
        img_path = os.path.join('static', GENERATED_IMAGE_PATH)
        img.save(img_path)

        return GENERATED_IMAGE_PATH, None

    except FileNotFoundError:
        return None, "Some characters are not supported."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

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

@app.route('/', methods=['GET', 'POST'])
def index():
    img_path = None
    error_message = None

    if request.method == 'POST':
        text = request.form.get('text', '').upper()

        if not text:
            error_message = "Please enter text."
        else:
            img_path, error_message = generate_image(text)

    return render_template('index.html', img_path=img_path, error_message=error_message)

if __name__ == "__main__":
    app.run()
