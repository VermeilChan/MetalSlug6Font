import os

from PIL import Image
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Define character dimensions
CHARACTER_DIMENSIONS = {
    'ABCDEFGJKMOQRSU': (50, 50),
    'HNPT': (48, 50),
    'L': (46, 50),
    '23456789': (50, 50),
    '1': (32, 50),
    'exclamation': (26, 50),
    'question': (50, 50),
    'default': (50, 50),  # Default character set
    ' ': (20, 50)  # Space character
}


# Function to generate an image with the custom font
def generate_image(text):
    # Calculate image dimensions
    img_height = 50  # Fixed height for characters
    img_widths = []
    for char in text:
        if char == ' ':
            img_widths.append(20)  # Fixed width for spaces
        else:
            char_img_path = os.path.join('static', f"{char}.png")
            try:
                char_img = Image.open(char_img_path).convert('RGBA')
                char_aspect_ratio = char_img.width / char_img.height
                char_width = int(img_height * char_aspect_ratio)
                img_widths.append(char_width)
            except Exception as e:
                raise ValueError(f"Error processing character '{char}': {str(e)}")

    total_width = sum(img_widths)

    # Create a transparent image with RGBA mode
    img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
    x = 0

    for char, char_width in zip(text, img_widths):
        if char == ' ':
            x += char_width
            continue

        char_img_path = os.path.join('static', f"{char}.png")
        try:
            char_img = Image.open(char_img_path).convert('RGBA')
            char_img = char_img.resize((char_width, img_height), Image.BILINEAR)
            img.paste(char_img, (x, 0), char_img)
            x += char_width
        except Exception as e:
            raise ValueError(f"Error processing character '{char}': {str(e)}")

    return img


# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle form submission
@app.route('/generate', methods=['POST'])
def generate():
    text = request.form.get('text', '').upper()  # Convert to uppercase
    if not text:
        return render_template('index.html', error_message="Please enter text.")
    try:
        img = generate_image(text)
        img_path = 'static/result.png'
        img.save(img_path)
        return render_template('result.html', img_path=img_path)
    except ValueError as ve:
        return render_template('index.html', error_message=str(ve))


# Route to serve the generated image
@app.route('/image/<filename>')
def image(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(debug=True)
