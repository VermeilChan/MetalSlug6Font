# Import necessary libraries
import os
from datetime import datetime

import PIL
from PIL import Image

# Set the width of spaces in the generated image
SPACE_WIDTH = 30

# Custom exception class for color validation
class ColorError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

# Function to generate a filename based on user input and timestamp
def generate_filename(user_input):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    sanitized_input = '-'.join(filter(str.isalnum, user_input.split()))
    filename = f"{sanitized_input}-{timestamp}.png"
    return filename

# Valid color options for each font
VALID_COLORS_BY_FONT = {
    1: ["Blue", "Orange-1", "Orange-2"],
    2: ["Blue", "Orange-1", "Orange-2"],
    3: ["Blue", "Orange-1"],
    4: ["Blue", "Orange-1"],
    5: ["Orange-1"]
}

# User input loop to select a font and color
while True:
    try:
        font = int(input("Choose a font from 1 to 5 (Refer to EXAMPLE.md for Font Preview) : "))

        if font in VALID_COLORS_BY_FONT:
            valid_colors = VALID_COLORS_BY_FONT[font]
            print(" | ".join(valid_colors))
            color = input("Enter the color you want to use: ")

            if color in valid_colors:
                break
            else:
                print("Invalid color. Please choose a valid color.")

        else:
            print("Invalid input. Please choose a font between 1 and 5.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Function to get paths for font files based on font and color
def get_font_paths(font , color):
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
            '|': 'Vertical-bar',
            ',': 'Comma',
            '&': 'Ampersand',
        }
        if char in SPE_CHAR:
            return os.path.join(SYMBOLS_FOLDER, f"{SPE_CHAR[char]}.png")
        else:
            raise ValueError(f"The character '{char}' is not supported.")

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
                try:
                    # Attempt to get the image path for the character
                    char_img_path = get_character_image_path(char, font_paths)
                    
                    # Open and convert the character image to RGBA format
                    with Image.open(char_img_path) as char_img:
                        char_img = char_img.convert('RGBA')

                except FileNotFoundError:
                    # Handle the case where the character image is not found
                    return None, f"Image not found for character '{char}'"
                except Exception as e:
                    # Handle other exceptions that may occur during image processing
                    return None, f"An error occurred for character '{char}': {e}"

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

    # Handle specific exceptions
    except FileNotFoundError as e:
        return None, f"Image not found for character '{char}': {e}"
    
    except (PIL.UnidentifiedImageError, ValueError) as e:
        return None, f"Error processing character '{char}': {e}"
    
    except Exception as e:
        return None, f"An error occurred: {e}"
