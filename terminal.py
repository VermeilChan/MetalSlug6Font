import sys
import logging
from main import generate_filename, generate_image_with_filename, get_font_paths, font, color

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
    return input("Enter the text you want to generate (type 'exit' to quit): ")

# Generate an image from the user's text and display it or an error message
def generate_and_display_image(text):
    try:
        if text.lower() == 'exit':
            print("Closing...")
            sys.exit(0)

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
            print(f"Successfully generated and saved: {img_path}")
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        logging.error(error_message, exc_info=True)

# The main function that orchestrates the program
def main():
    display_intro_message()

    while True:
        text = get_user_input()
        generate_and_display_image(text)

if __name__ == "__main__":
    main()
