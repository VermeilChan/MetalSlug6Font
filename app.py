import os
import re
import PIL
import string
from color import *
from PIL import Image
from pathlib import Path
from colorama import init
from datetime import datetime

# Constants
ALLOWED_ALPHABETS = string.ascii_letters
ALLOWED_NUMBERS = string.digits
ALLOWED_SYMBOLS = string.punctuation
ALLOWED_CHARACTERS = set(ALLOWED_ALPHABETS + ALLOWED_NUMBERS + ALLOWED_SYMBOLS + ' ')

CHARACTERS_FOLDER = 'Assets/Alphabets'
NUMBERS_FOLDER = 'Assets/Numbers'
SYMBOLS_FOLDER = 'Assets/Symbols'

SPACE_WIDTH = 20

# Initialize colorama
init(autoreset=True)

# Get the user's desktop folder
def get_desktop_path():
    desktop = Path.home() / "Desktop"
    return str(desktop)

# Generate a unique filename based on user input and current date and time
def generate_filename(user_input):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input = re.sub(r'[^a-zA-Z0-9]', '_', user_input)
    filename = f"{input}_{timestamp}.png"
    return filename

# Get the path of the character image based on the character
def get_character_image_path(char):
    if char in ALLOWED_ALPHABETS:
        return os.path.join(CHARACTERS_FOLDER, char + '.png')
    elif char in ALLOWED_NUMBERS:
        return os.path.join(NUMBERS_FOLDER, char + '.png')
    elif char == '!':
        return os.path.join(SYMBOLS_FOLDER, 'Exclamation.png')
    elif char == '?':
        return os.path.join(SYMBOLS_FOLDER, 'Question.png')
    else:
        raise ValueError(f"The character '{char}' is not supported.")

# Generate an image from the provided text and save it with the provided filename
def generate_image_with_filename(text, filename):
    try:
        text = ''.join(char for char in text if char in ALLOWED_CHARACTERS)
        img_height = None
        chars = []

        for char in text:
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

        # Get the desktop path and save the composite image
        desktop_path = get_desktop_path()
        img_path = os.path.join(desktop_path, filename)
        img.save(img_path)

        return filename, None

    except ValueError as ve:
        return None, str(ve)
