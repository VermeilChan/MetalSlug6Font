# Import necessary libraries
import os
from datetime import datetime

from PIL import Image, UnidentifiedImageError

# Constants
SPACE_WIDTH = 30
MAX_FILENAME_LENGTH = 255
DESKTOP_PATH = os.path.expanduser("~/Desktop")

# Function to generate a filename based on user input and timestamp
def generate_filename(user_input):
    try:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        sanitized_input = '-'.join(filter(str.isalnum, user_input.split()))
        filename = f"{sanitized_input}-{timestamp}.png"
        if len(filename) > MAX_FILENAME_LENGTH:
            filename = f"{timestamp}.png"
        return filename
    except Exception as e:
        raise RuntimeError(f"Error generating filename: {str(e)}")

# Function to get paths to font assets (letters, numbers, symbols) based on font and color
def get_font_paths(font, color):
    try:
        base_path = os.path.join('Assets', 'FONTS', f'Font-{font}', f'Font-{font}-{color}')
        return (
            os.path.join(base_path, 'Letters'),
            os.path.join(base_path, 'Numbers'),
            os.path.join(base_path, 'Symbols')
        )
    except Exception as e:
        raise RuntimeError(f"Error getting font paths: {str(e)}")

# Function to get the image path for a specific character based on its type
def get_character_image_path(char, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if char.isalpha():
        folder = 'Lower-Case' if char.islower() else 'Upper-Case'
        char_img_path = os.path.join(CHARACTERS_FOLDER, folder, f"{char}.png")
    elif char.isdigit():
        char_img_path = os.path.join(NUMBERS_FOLDER, f"{char}.png")
    elif char == ' ':
        return None
    else:
        SPECIAL_CHARACTERS = {
            '!': 'Exclamation', '?': 'Question', "'": 'Apostrophe', '*': 'Asterisk',
            ')': 'Bracket-Left', '}': 'Bracket-Left-2', ']': 'Bracket-Left-3',
            '(': 'Bracket-Right', '{': 'Bracket-Right-2', '[': 'Bracket-Right-3',
            '^': 'Caret', ':': 'Colon', '$': 'Dollar', '=': 'Equals', '>': 'Greater-than',
            '-': 'Hyphen', '∞': 'Infinity', '<': 'Less-than', '#': 'Number', '%': 'Percent',
            '.': 'Period', '+': 'Plus', '"': 'Quotation', ';': 'Semicolon', '/': 'Slash',
            '~': 'Tilde', '_': 'Underscore', '|': 'Vertical-bar', ',': 'Comma', '&': 'Ampersand',
            '♥': 'Heart', '©': 'Copyright', '⛶': 'Square', 'Ⅰ': 'One', 'Ⅱ': 'Two', 'Ⅲ': 'Three',
            'Ⅳ': 'Four', 'Ⅴ': 'Five', '◀': 'Left', '▲': 'Up', '▶': 'Right', '▼': 'Down',
            '★': 'Star', '⋆': 'Mini-Star', '☞': 'Hand', '¥': 'Yen', '♪': 'Musical-Note', '︷': 'Up-Arrow'
        }
        char_img_path = os.path.join(SYMBOLS_FOLDER, f"{SPECIAL_CHARACTERS.get(char, '')}.png")

    try:
        if not os.path.isfile(char_img_path):
            return None
        return char_img_path
    except Exception as e:
        raise RuntimeError(f"Error getting character image path for '{char}': {str(e)}")

# Function to generate an image with a given filename and text using provided font assets
def generate_image_with_filename(text, filename, font_paths):
    try:
        img_height = None
        char_images = {}
        img_path = os.path.join(DESKTOP_PATH, filename)

        with Image.new('RGBA', (1, 1), (0, 0, 0, 0)) as space_img:
            for char in text:
                if char == ' ':
                    char_img = space_img
                else:
                    char_img_path = get_character_image_path(char, font_paths)
                    if char_img_path is None:
                        # Handle the case where the character image is not found.
                        print(f"Character image not found for '{char}'. Skipping.")
                        continue

                    with Image.open(char_img_path).convert('RGBA') as char_img:
                        char_images[char] = char_img
                        img_height = char_img.size[1] if img_height is None else img_height

            chars = [(char_images[char], SPACE_WIDTH if char == ' ' else char_images[char].size[0]) for char in text]
            total_width = sum(char_width for _, char_width in chars)

            with Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0)) as img:
                x = 0
                for char_img, char_width in chars:
                    img.paste(char_img, (x, 0), char_img)
                    x += char_width

                img.save(img_path)
        return filename, None

    except FileNotFoundError as e:
        return None, f"File not found error: {str(e)}"
    except UnidentifiedImageError as e:
        return None, f"Unidentified image error: {str(e)}"
    except ValueError as e:
        return None, f"Value error: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"
