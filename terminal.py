# Import necessary libraries
import sys
import os
import logging
import argparse
from logging.handlers import RotatingFileHandler

# Prevent the generation of .pyc (Python bytecode) files
sys.dont_write_bytecode = True

from main import generate_filename, generate_image_with_filename, get_font_paths

# Set up logging to a rotating log file named 'app.log' with a maximum size of 1 MB
log_filename = 'app.log'
log_format = '%(asctime)s - %(levelname)s: %(message)s'

# Use a RotatingFileHandler to enable log rotation
log_handler = RotatingFileHandler(log_filename, maxBytes=1e6, backupCount=5)
log_handler.setFormatter(logging.Formatter(log_format))

# Create a logger and set the level to INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Define valid color options for each font
VALID_COLORS_BY_FONT = {
    1: ["Blue", "Orange-1", "Orange-2"],
    2: ["Blue", "Orange-1", "Orange-2"],
    3: ["Blue", "Orange-1"],
    4: ["Blue", "Orange-1"],
    5: ["Orange-1"]
}

# Define a constant for the closing message
CLOSING_MESSAGE = "Closing..."

# Function to display an introductory message
def display_intro_message():
    print("Note: Metal Slug Font style conversion may not be compatible with all fonts.")
    print("Refer to the SUPPORTED.md file for details.")

# Function to get user input for text to be converted
def get_user_input():
    return input("Enter the text you want to generate (type 'exit' to close): ")

# Function to allow the user to select a font and color
def select_font_and_color():
    while True:
        try:
            # Prompt the user to choose a font or exit
            user_input = input("Choose a font from 1 to 5 (Refer to EXAMPLE.md for Font Preview) or type 'exit' to close: ")

            if user_input.lower() == 'exit':
                print(CLOSING_MESSAGE)
                sys.exit(0)

            font = int(user_input)

            # Check if the chosen font is valid
            if font in VALID_COLORS_BY_FONT:
                valid_colors = VALID_COLORS_BY_FONT[font]
                print("Available colors: " + " | ".join(valid_colors))
                color_input = input("Enter the color you want to use or type 'exit' to close: ")

                if color_input.lower() == 'exit':
                    print(CLOSING_MESSAGE)
                    sys.exit(0)
                elif color_input.title() in valid_colors:
                    color_input = color_input.title()
                    logger.info(f"Chosen Font: {font}, Chosen Color: {color_input}")
                    return font, color_input
                else:
                    print("Invalid color. Please choose a valid color.")

            else:
                print("Invalid input. Please choose a font between 1 and 5.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to generate and display an image based on user input
def generate_and_display_image(text, font, color):
    try:
        if text.lower() == 'exit':
            print(CLOSING_MESSAGE)
            sys.exit(0)

        # Check for empty input
        if not text.strip():
            print("Input text is empty. Please enter some text.")
            return

        filename = generate_filename(text)

        font_paths = get_font_paths(font, color)

        img_path, error_message_generate = generate_image_with_filename(text, filename, font_paths)

        if error_message_generate:
            print(f"Error: {error_message_generate}")
            logger.error(error_message_generate)
        else:
            print(f"Image successfully generated and saved as: {img_path}")
            logger.info(f"Generated Image Path: '{img_path}'")
            print(f"You can find the image on your desktop: {os.path.abspath(os.path.join(os.path.expanduser('~'), 'Desktop', img_path))}")

        # Log chosen font, chosen color, and user input
        logger.info(f"Chosen Font: {font}, Chosen Color: {color}, User Input: '{text}'")

    except KeyboardInterrupt:
        print(CLOSING_MESSAGE)
        sys.exit(0)
    except FileNotFoundError as e:
        error_message_generate = f"Font file not found: {e.filename}"
        print(error_message_generate)
        logger.error(error_message_generate)
        logger.debug(e, exc_info=True)
    except Exception as e:
        error_message_generate = f"An error occurred: {e}"
        print(error_message_generate)
        logger.exception(error_message_generate)

# The main function of the program
def main():
    display_intro_message()

    font, color = select_font_and_color()

    try:
        while True:
            text = get_user_input()
            generate_and_display_image(text, font, color)
    except KeyboardInterrupt:
        print(CLOSING_MESSAGE)
        sys.exit(0)
    except Exception as e:
        error_message_main = f"An unexpected error occurred: {e}"
        print(error_message_main)
        logger.exception(error_message_main)

    finally:
        logging.shutdown()

# Entry point of the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MSFONT")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level (default: INFO)")
    args = parser.parse_args()

    try:
        logger.setLevel(args.log_level)
        main()
    except KeyboardInterrupt:
        print(CLOSING_MESSAGE)
        sys.exit(0)
    except Exception as e:
        error_message_main = f"An unexpected error occurred: {e}"
        print(error_message_main)
        logger.exception(error_message_main)

    finally:
        logging.shutdown()
