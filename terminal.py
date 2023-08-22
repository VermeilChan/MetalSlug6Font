import sys
import random
import traceback
from color import COLORS  # Importing COLORS from the 'color' module
from colorama import Fore  # Importing the 'Fore' class from the 'colorama' module
from main import generate_filename, generate_image_with_filename, get_font_paths, font

sys.dont_write_bytecode = True  # Disable writing compiled bytecode files

def main():
    # Print a note about compatibility
    print(Fore.RED + "Note: Metal Slug font style conversion may not be compatible with all fonts. Refer to the SUPPORTED.md file for details.")
    
    # Start an infinite loop for user input
    while True:
        color_choice = random.choice(COLORS)  # Choose a random color from the COLORS list
        text = input(f"{color_choice}Enter Text: ")  # Prompt the user for input
        
        if not text:
            print(f"{color_choice}Goodbye!")  # Exit loop if no input is provided
            break

        try:
            filename = generate_filename(text)  # Generate a filename based on the entered text
            font_paths = get_font_paths(font)  # Get the paths of available fonts
            img_path, error_message = generate_image_with_filename(text, filename, font_paths)  # Generate an image with the given text and font
            
            if error_message:
                print(f"{color_choice}Error: {error_message}")  # Print error message if there's an issue
            else:
                print(f"{color_choice}Image generated successfully: {img_path}")  # Print success message with image path
        except Exception as e:
            print(f"{color_choice}An error occurred: {e}")  # Print an error message if an exception occurs
            traceback.print_exc()  # Print the traceback for debugging purposes

if __name__ == "__main__":
    main()  # Execute the 'main' function when the script is run directly
