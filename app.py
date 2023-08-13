import os
import shutil
from PIL import Image, ImageOps
from flask import Flask, render_template, request

app = Flask(__name__)

CHARACTER_FILES = {
    '?': 'Symbols/question',
    '!': 'Symbols/exclamation'
}

GENERATED_IMAGE_PATH = 'result.png'

def get_character_image(char):
    try:
        char_img_path = os.path.join('static', f"{CHARACTER_FILES.get(char, 'Alphabets/' + char)}.png")
        char_img = Image.open(char_img_path).convert('RGBA')
        return char_img
    except FileNotFoundError:
        return None

def resize_character(char_img, char_width, img_height):
    return ImageOps.fit(char_img, (char_width, img_height), method=Image.BILINEAR)

def generate_image(text):
    try:
        img_widths = []
        img_height = None
        chars = []

        for char in text:
            if char == ' ':
                char_width = 20  # Fixed width for space
                char_img = Image.new('RGBA', (char_width, 1), (0, 0, 0, 0))
            else:
                char_img = get_character_image(char)
                if char_img is None:
                    raise ValueError(f"Character image not found for '{char}'")
                char_size = char_img.size
                char_width = char_size[0]

            img_widths.append(char_width)
            chars.append((char_img, char_width))

            if img_height is None:
                img_height = char_size[1]

        total_width = sum(img_widths)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0

        for char_img, char_width in chars:
            char_img_resized = resize_character(char_img, char_width, img_height)
            img.paste(char_img_resized, (x, 0), char_img_resized)
            x += char_width

        img_path = os.path.join('static', GENERATED_IMAGE_PATH)
        img.save(img_path)

        return GENERATED_IMAGE_PATH, None

    except Exception as e:
        return None, str(e)

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
