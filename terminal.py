# Import necessary libraries
import sys
import logging

# Prevent the generation of .pyc (Python bytecode) files
sys.dont_write_bytecode = True

# Import functions from another file named 'main'
from main import generate_filename, generate_image_with_filename, get_font_paths

# Set up logging to a file named 'app.log'
log_filename = 'app.log'
log_format = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(filename=log_filename, level=logging.INFO, format=log_format)

# Function to display an introductory message
def display_intro_message():
    print("Note: Metal Slug Font style conversion may not be compatible with all fonts.")
    print("Refer to the SUPPORTED.md file for details.")

# Function to get user input for text to be converted
def get_user_input():
    return input("Enter the text you want to generate (type 'exit' to close): ")

# Function to allow the user to select a font and color
def select_font_and_color():
    # Define valid color options for each font
    VALID_COLORS_BY_FONT = {
        1: ["Blue", "Orange-1", "Orange-2"],
        2: ["Blue", "Orange-1", "Orange-2"],
        3: ["Blue", "Orange-1"],
        4: ["Blue", "Orange-1"],
        5: ["Orange-1"]
    }

    while True:
        try:
            # Prompt the user to choose a font or exit
            user_input = input("Choose a font from 1 to 5 (Refer to EXAMPLE.md for Font Preview) or type 'exit' to close: ")

            if user_input.lower() == 'exit':
                print("Closing...")
                sys.exit(0)

            font = int(user_input)

            # Check if the chosen font is valid
            if font in VALID_COLORS_BY_FONT:
                valid_colors = [color.lower() for color in VALID_COLORS_BY_FONT[font]]
                print("Available colors: " + " | ".join(valid_colors))
                color_input = input("Enter the color you want to use or type 'exit' to close: ").lower()

                if color_input == 'exit':
                    print("Closing...")
                    sys.exit(0)
                elif color_input in valid_colors:
                    logging.info(f"Chosen Font: {font}, Chosen Color: {color_input}")
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
            print("Closing...")
            sys.exit(0)

        filename = generate_filename(text)

        font_paths = get_font_paths(font, color)

        img_path, error_message = generate_image_with_filename(text, filename, font_paths)

        if error_message:
            print(f"Error: {error_message}")
            logging.error(error_message)
        else:
            print(f"Image successfully generated and saved as: {img_path}")
            logging.info(f"Generated Image Path: {img_path}")
    except KeyboardInterrupt:
        print("Closing...")
        sys.exit(0)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        logging.exception(error_message)

# The main function of the program
def main():
    display_intro_message()

    font, color = select_font_and_color() 

    try:
        while True:
            text = get_user_input()
            generate_and_display_image(text, font, color)
    except KeyboardInterrupt:
        print("Closing...")
        sys.exit(0)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        logging.exception(error_message)

    finally:
        logging.shutdown()

# Entry point of the script
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Closing...")
        sys.exit(0)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        logging.exception(error_message)

    finally:
        logging.shutdown()
