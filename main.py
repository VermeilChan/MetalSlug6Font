import os
import re
import PIL
import string
from PIL import Image
from pathlib import Path
from colorama import Fore
from datetime import datetime

# Set of allowed characters for the generated image
ALLOWED_CHARACTERS = set(string.ascii_letters + string.digits + string.punctuation + ' ')

# Width of a space character in pixels
SPACE_WIDTH = 10

# Function to get the user's desktop path
def get_desktop_path():
    desktop = Path.home() / "Desktop"
    return str(desktop)

# Function to generate a filename based on user input and current timestamp
def generate_filename(user_input):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_input = re.sub(r'\W+', '_', user_input)
    return f"{sanitized_input}_{timestamp}.png"

# Get user input for font choice
font = int(input(f"{Fore.GREEN}Choose A Font From 1 To 4 : {Fore.RESET}"))

# Function to get paths to font resources
def get_font_paths(font):
    base_path = f'Assets/Font-{font}'
    return (
        os.path.join(base_path, 'Letters'),
        os.path.join(base_path, 'Numbers'),
        os.path.join(base_path, 'Symbols')
    )

# Function to get the image path for a specific character
def get_character_image_path(char, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if char.isalpha():
        folder = 'Lower-Case' if char.islower() else 'Upper-Case'
        return os.path.join(CHARACTERS_FOLDER, folder, char + '.png')
    elif char.isdigit():

        return os.path.join(NUMBERS_FOLDER, char + '.png')
    
    elif char == ' ':
        return None
    
    else:
        # Special characters mapping
        SPE_CHAR = {
            '!': 'Exclamation',
            '?': 'Question',
            "'": 'Apostrophe',
            '*': 'Asterisk',
            ')': 'Bracket-Left',
            '}': 'Bracket-Left-2',
            ']': 'Bracket-Left-3',
            '(': 'Bracket-Right',
            '{': 'Bracket-Right-2',
            '[': 'Bracket-Right-3',
            '^': 'Caret',
            ':': 'Colon',
            '$': 'Dollar',
            '=': 'Equals',
            '>': 'Greater-than',
            '-': 'Hyphen',
            '∞': 'Infinity',
            '<': 'Less-than',
            '#': 'Number',
            '%': 'Percent',
            '.': 'Period',
            '+': 'Plus',
            '"': 'Quotation',
            ';': 'Semicolon',
            '/': 'Slash',
            '~': 'Tilde',
            '_': 'Underscore',
            '|': 'Vertical-bar'
        }
        if char in SPE_CHAR.keys():
            return os.path.join(SYMBOLS_FOLDER, f"{SPE_CHAR[char]}.png")
        else:
            raise ValueError(f"The character '{char}' is not supported.")

# Function to generate an image based on input text, filename, and font paths
def generate_image_with_filename(text, filename, font_paths):
    try:
        # Remove any characters not in the allowed set
        text = ''.join(char for char in text if char in ALLOWED_CHARACTERS)
        img_height = None
        chars = []

        # Generate a list of character images and widths
        for char in text:
            if char == ' ':
                if chars and chars[-1][1] == ' ':
                    continue
                char_img = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
                char_width = SPACE_WIDTH
            else:
                char_img_path = get_character_image_path(char, font_paths)
                try:
                    char_img = Image.open(char_img_path).convert('RGBA')
                    char_size = char_img.size
                    char_width = char_size[0]
                    img_height = char_size[1] if img_height is None else img_height

                except FileNotFoundError as fnfe:
                    raise ValueError(f"Image file not found: {str(fnfe)}")
                
                except PIL.Image.Error as img_err:
                    raise ValueError(f"Error processing image: {str(img_err)}")

            chars.append((char_img, char_width))

        # Calculate total width of the image
        total_width = sum(char_width for _, char_width in chars)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0
        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        # Save the generated image to the user's desktop
        try:
            img_path = os.path.join("Output", filename)
            img.save(img_path)
        except FileNotFoundError:
            os.mkdir("Output")
            img_path = os.path.join("Output", filename)
            img.save(img_path)

        return filename, None

    except ValueError as ve:
        return None, str(ve)
