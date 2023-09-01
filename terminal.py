import sys
import traceback

# Prevent the generation of bytecode files (.pyc)
sys.dont_write_bytecode = True

# Import functions and variables from the 'main.py' file
from main import generate_filename, generate_image_with_filename, get_font_paths, font, color

# Display an introductory message to the user
def display_intro_message():
    print("Note : Metal Slug font style conversion may not be compatible with all fonts."
            " Refer to the SUPPORTED.md file for details.")

# Get user input for the text they want to generate
def get_user_input():
    return input("Enter the text you want to generate: ")

# Generate an image from the user's text and display it or an error message
def generate_and_display_image(text):
    try:
        # Generate a filename based on the user's input
        filename = generate_filename(text)

        # Get font paths based on user-specified font and color
        font_paths = get_font_paths(font, color)

        # Generate the image and handle any potential errors
        img_path, error_message = generate_image_with_filename(text, filename, font_paths)

        if error_message:
            print(f"Error: {error_message}")
        else:
            print(f"Successfully generated and saved: {img_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

        # Print a traceback to help diagnose the error
        traceback.print_exc()

# The main function that orchestrates the program
def main():
    display_intro_message()

    while True:
        text = get_user_input()

        if not text:
            print("Closing...")
            break

        generate_and_display_image(text)

if __name__ == "__main__":
    main()
