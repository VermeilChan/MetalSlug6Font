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
    ' ': (20, 50)  # Space character
}


# Function to generate an image with the custom font
def generate_image(text):
    # Calculate image dimensions
    total_width = sum(
        max(CHARACTER_DIMENSIONS.get(char_set, (50, 50))[0] for char_set in CHARACTER_DIMENSIONS if char in char_set)
        for char in text)
    img_height = 50

    # Create a transparent image with RGBA mode
    img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
    x = 0

    for char in text:
        if char == ' ':
            char_width, _ = CHARACTER_DIMENSIONS[char]
        else:
            char_img_path = os.path.join('static', f"{char}.png")
            try:
                char_img = Image.open(char_img_path).convert('RGBA')
                char_width, _ = char_img.size

                # Find the character set to get the appropriate width
                char_set = next((char_set for char_set in CHARACTER_DIMENSIONS if char in char_set), None)
                if char_set:
                    char_set_width, _ = CHARACTER_DIMENSIONS[char_set]
                    char_scale_factor = char_set_width / char_width
                    char_width *= char_scale_factor
                else:
                    # Use a default width if the character is not in any defined character set
                    char_width, _ = CHARACTER_DIMENSIONS.get(char, (50, 50))

                # Resize the character image to the appropriate width and paste it
                char_img = char_img.resize((int(char_width), img_height), Image.BILINEAR)
                img.paste(char_img, (x, 0), char_img)
            except Exception as e:
                raise ValueError(f"Error processing character '{char}': {str(e)}")

        x += int(char_width)

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
