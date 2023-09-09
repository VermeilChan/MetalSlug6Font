# Import necessary libraries
import os
from datetime import datetime

from PIL import Image, UnidentifiedImageError

# Constant
SPACE_WIDTH = 30
MAX_FILENAME_LENGTH = 255

# Custom exception class for color validation
class ColorError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# Function to generate a filename based on user input and timestamp
def generate_filename(user_input):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    sanitized_input = '-'.join(filter(str.isalnum, user_input.split()))
    filename = f"{sanitized_input}-{timestamp}.png"
    if len(filename) > MAX_FILENAME_LENGTH:
        filename = f"{timestamp}.png"
    return filename

# Function to get paths for font files based on font and color
def get_font_paths(font, color):
    base_path = f'Assets/FONTS/Font-{font}/Font-{font}-{color}'
    return (
        os.path.join(base_path, 'Letters'),
        os.path.join(base_path, 'Numbers'),
        os.path.join(base_path, 'Symbols')
    )

# Function to get the path of an image for a given character in a font
def get_character_image_path(char, font_paths):
    CHARACTERS_FOLDER, NUMBERS_FOLDER, SYMBOLS_FOLDER = font_paths

    if char.isalpha():
        folder = 'Lower-Case' if char.islower() else 'Upper-Case'
        char_img_path = os.path.join(CHARACTERS_FOLDER, folder, char + '.png')
    elif char.isdigit():
        char_img_path = os.path.join(NUMBERS_FOLDER, char + '.png')
    elif char == ' ':
        return None
    else:
        # Special characters mapping
        SPE_CHAR = {
            '!': 'Exclamation', '?': 'Question', "'": 'Apostrophe', '*': 'Asterisk',
            ')': 'Bracket-Left', '}': 'Bracket-Left-2', ']': 'Bracket-Left-3',
            '(': 'Bracket-Right', '{': 'Bracket-Right-2', '[': 'Bracket-Right-3',
            '^': 'Caret', ':': 'Colon', '$': 'Dollar', '=': 'Equals', '>': 'Greater-than',
            '-': 'Hyphen', '∞': 'Infinity', '<': 'Less-than', '#': 'Number', '%': 'Percent',
            '.': 'Period', '+': 'Plus', '"': 'Quotation', ';': 'Semicolon', '/': 'Slash',
            '~': 'Tilde', '_': 'Underscore', '|': 'Vertical-bar', ',': 'Comma', '&': 'Ampersand',
            '♥': 'Heart', '©': 'Copyright', '⛶': 'Square', 'Ⅰ': 'One', 'Ⅱ': 'Two', 'Ⅲ': 'Three',
            'Ⅳ': 'Four', 'Ⅴ': 'Five', '◀': 'Left', '▲': 'Up', '▶': 'Right', '▼': 'Down',
            '★': 'Star', '⋆': 'Star-2', '☞': 'Hand', '¥': 'Yen', '♪': 'Musical-Note', '︷': 'Up-Arrow'
        }
        if char in SPE_CHAR:
            char_img_path = os.path.join(SYMBOLS_FOLDER, f"{SPE_CHAR[char]}.png")
        else:
            raise ValueError(f"The character '{char}' is not supported.")

    # Check if the image file exists
    if not os.path.isfile(char_img_path):
        raise FileNotFoundError(f"Image not found for character '{char}'")

    return char_img_path

# Function to generate an image from text and save it with a given filename
def generate_image_with_filename(text, filename, font_paths):
    try:
        # Initialize variables
        img_height = None
        char_images = {}
        img_path = os.path.join(os.path.expanduser("~/Desktop"), filename)

        # Iterate through each character in the input text
        for char in text:
            if char == ' ':
                # Create a transparent space if the character is a space
                char_img = Image.new('RGBA', (SPACE_WIDTH, 1), (0, 0, 0, 0))
            else:
                char_img_path = get_character_image_path(char, font_paths)

                # Open and convert the character image to RGBA format
                with Image.open(char_img_path) as char_img:
                    char_img = char_img.convert('RGBA')

            # Store the character image in a dictionary
            char_images[char] = char_img

            # Update the image height (used for creating the final image)
            img_height = char_img.size[1] if img_height is None else img_height

        # Create a list of tuples, each containing the character image and its width
        chars = [(char_images[char], SPACE_WIDTH if char == ' ' else char_images[char].size[0]) for char in text]

        # Calculate the total width of the final image
        total_width = sum(char_width for _, char_width in chars)

        # Create an empty RGBA image with the calculated dimensions
        img = Image.new('RGBA', (total_width, img_height), (0, 0, 0, 0))
        x = 0

        # Paste each character image onto the final image
        for char_img, char_width in chars:
            img.paste(char_img, (x, 0), char_img)
            x += char_width

        # Save the final image to the specified path
        img.save(img_path)

        # Return the filename and no error message
        return filename, None

    # Handle file not found errors
    except FileNotFoundError as e:
        return None, f"File not found: {e}"

    # Handle image processing errors
    except (UnidentifiedImageError, ValueError) as e:
        return None, f"Image processing error: {e}"

    # Handle other unexpected errors
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"
