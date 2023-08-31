import os
import PIL
from PIL import Image
from colorama import Fore
from datetime import datetime

SPACE_WIDTH = 30

class ColorError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def generate_filename(user_input):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    sanitized_input = '-'.join(filter(str.isalnum, user_input.split()))
    filename = f"{sanitized_input}-{timestamp}.png"
    return filename

while True:
    try:
        font = int(input(f"{Fore.GREEN}Choose A Font From 1 To 4 :{Fore.RESET}"))

        if 1 <= font <= 4:
            if font == 3 or font == 4:
                valid_colors = ["Blue"]
            else:
                valid_colors = ["Blue", "Orange-1", "Orange-2"]

            print(" | ".join(valid_colors))
            color = input(f"{Fore.GREEN}Choose A Color: {Fore.RESET}")

            if color in valid_colors:
                break
            else:
                print(f"{Fore.RED}Invalid color. Please choose a valid color.{Fore.RESET}")

        else:
            print(f"{Fore.RED}Invalid input. Please choose a font between 1 and 4.{Fore.RESET}")

    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a valid number.{Fore.RESET}")

def get_font_paths(font , color):
    base_path = f'Assets/Font-{font}/Font-{font}-{color}'
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
            '|': 'Vertical-bar',
            ',': 'Comma',
            '&': 'Ampersand',
        }
        if char in SPE_CHAR:
            return os.path.join(SYMBOLS_FOLDER, f"{SPE_CHAR[char]}.png")
        else:
            raise ValueError(f"The character '{char}' is not supported.")

def generate_image_with_filename(text, filename, font_paths):
    try:
        img_height = None
        char_images = {}
        output_dir = "Output"
        os.makedirs(output_dir, exist_ok=True)
        img_path = os.path.join(output_dir, filename)

        for char in text:
            if char == ' ':
                char_img = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
            else:
                try:
                    char_img_path = get_character_image_path(char, font_paths)
                    with Image.open(char_img_path) as char_img:
                        char_img = char_img.convert('RGBA')
                except FileNotFoundError:
                    return None, f"Image not found for character '{char}'"
                except Exception as e:
                    return None, f"An error occurred for character '{char}': {e}"

            char_images[char] = char_img
            img_height = char_img.size[1] if img_height is None else img_height

        chars = [(char_images[char], SPACE_WIDTH if char == ' ' else char_images[char].size[0]) for char in text]
        total_width = sum(char_width for _, char_width in chars)
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0

        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        img.save(img_path)
        return filename, None

    except FileNotFoundError as e:
        return None, f"Image not found for character '{char}': {e}"
    
    except (PIL.UnidentifiedImageError, ValueError) as e:
        return None, f"Error processing character '{char}': {e}"
    
    except Exception as e:
        return None, f"An error occurred: {e}"
