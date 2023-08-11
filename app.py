import os

from PIL import Image, ImageOps
from flask import Flask, render_template, request

app = Flask(__name__)

# Mapping special characters to filenames
CHARACTER_FILES = {
    ' ': 'space',
    '?': '_',
    '!': 'exclamation'
}


# Function to get the dimensions of a character image
def get_character_dimensions(char):
    char_img_path = os.path.join('static', f"{char}.png")
    char_img = Image.open(char_img_path).convert('RGBA')
    return char_img.size


# Function to generate an image with the custom font
def generate_image(text):
    try:
        img_height = None
        img_widths = []
        for char in text:
            char_size = get_character_dimensions(CHARACTER_FILES.get(char, char))
            img_widths.append(char_size[0])
            if img_height is None:
                img_height = char_size[1]

        total_width = sum(img_widths)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0

        for char, char_width in zip(text, img_widths):
            char_img_path = os.path.join('static', f"{CHARACTER_FILES.get(char, char)}.png")
            char_img = Image.open(char_img_path).convert('RGBA')
            char_img = ImageOps.fit(char_img, (char_width, img_height), method=Image.BILINEAR)
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        return img, None

    except Exception as e:
        return None, str(e)


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text', '').upper()

    if not text:
        return render_template('index.html', error_message="Please enter text.")

    img, error_message = generate_image(text)

    if img is None:
        return render_template('index.html', error_message=error_message)

    img_path = os.path.join('static', 'result.png')
    img.save(img_path)

    return render_template('result.html', img_path=img_path)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
