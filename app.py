import os
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)

CHARACTER_FILES = {
    '?': 'Symbols/question',
    '!': 'Symbols/exclamation'
}

SPACE_WIDTH = 20
GENERATED_IMAGE_PATH = 'result.png'

def generate_image(text):
    try:
        img_height = None
        chars = []
        char_size = None

        for char in text:
            if char == ' ':
                char_img = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
                char_width = SPACE_WIDTH
            else:
                char_img_path = os.path.join('static', f"{CHARACTER_FILES.get(char, 'Alphabets/' + char)}.png")
                if not os.path.exists(char_img_path):
                    raise ValueError(f"Character image not found for '{char}'")

                char_img = Image.open(char_img_path).convert('RGBA')
                char_size = char_img.size
                char_width = char_size[0]

                if img_height is None:
                    img_height = char_size[1]

            chars.append((char_img, char_width))

        total_width = sum(char_width for _, char_width in chars)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0

        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
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
