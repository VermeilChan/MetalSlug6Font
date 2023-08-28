import os
import re
import PIL
from PIL import Image
from colorama import Fore
from datetime import datetime

SPACE_WIDTH = 30

def generate_filename(user_input):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_input = re.sub(r'\W+', '_', user_input)
    filename = f"{sanitized_input}_{timestamp}.png"
    return filename

font = int(input(f"{Fore.GREEN}Choose A Font From 1 To 4 : {Fore.RESET}"))

def get_font_paths(font):
    base_path = f'Assets/Font-{font}'
    return (
        os.path.join(base_path, 'Letters'),
        os.path.join(base_path, 'Numbers'),
        os.path.join(base_path, 'Symbols')
    )

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

def generate_image_with_filename(text, filename, font_paths):
    try:
        img_height = None
        char_images = {}

        for char in text:
            if char not in char_images:
                if char == ' ':
                    char_images[char] = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
                else:
                    char_img_path = get_character_image_path(char, font_paths)
                    char_img = Image.open(char_img_path).convert('RGBA')
                    char_images[char] = char_img
                    char_size = char_img.size
                    img_height = char_size[1] if img_height is None else img_height

        chars = [(char_images[char], SPACE_WIDTH if char == ' ' else char_images[char].size[0]) for char in text]
        total_width = sum(char_width for _, char_width in chars)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0
        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        img_path = os.path.join(output_dir, filename)
        img.save(img_path)

        return filename, None

    except (FileNotFoundError, PIL.UnidentifiedImageError, ValueError) as e:
        return None, str(e)
