# Import necessary libraries
import sys
import logging

from main import generate_filename, generate_image_with_filename, get_font_paths

# Prevent the generation of bytecode files (.pyc)
sys.dont_write_bytecode = True

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

# Display an introductory message to the user
def display_intro_message():
    print("Note: Metal Slug Font style conversion may not be compatible with all fonts.")
    print("Refer to the SUPPORTED.md file for details.")

# Get user input for the text they want to generate
def get_user_input():
    return input("Enter the text you want to generate (type 'exit' to close): ")

# Get user input for font and color selection
def select_font_and_color():
    VALID_COLORS_BY_FONT = {
        1: ["Blue", "Orange-1", "Orange-2"],
        2: ["Blue", "Orange-1", "Orange-2"],
        3: ["Blue", "Orange-1"],
        4: ["Blue", "Orange-1"],
        5: ["Orange-1"]
    }

    while True:
        try:
            font = int(input("Choose a font from 1 to 5 (Refer to EXAMPLE.md for Font Preview): "))

            if font in VALID_COLORS_BY_FONT:
                valid_colors = VALID_COLORS_BY_FONT[font]
                print("Available colors: " + " | ".join(valid_colors))
                color = input("Enter the color you want to use: ")

                if color in valid_colors:
                    return font, color
                else:
                    print("Invalid color. Please choose a valid color.")

            else:
                print("Invalid input. Please choose a font between 1 and 5.")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Generate an image from the user's text and display it or an error message
def generate_and_display_image(text, font, color):
    try:
        if text.lower() == 'exit':
            print("Closing...")
            sys.exit(0)

        print("Generating the image. Please wait...")

        # Generate a filename based on the user's input
        filename = generate_filename(text)

        # Get font paths based on user-specified font and color
        font_paths = get_font_paths(font, color)

        # Generate the image and handle any potential errors
        img_path, error_message = generate_image_with_filename(text, filename, font_paths)

        if error_message:
            print(f"Error: {error_message}")
            logging.error(error_message)
        else:
            print(f"Image successfully generated and saved as: {img_path}")
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        logging.exception(error_message)

# The main function that orchestrates the program
def main():
    display_intro_message()

    while True:
        font, color = select_font_and_color()
        text = get_user_input()
        generate_and_display_image(text, font, color)

if __name__ == "__main__":
    main()
