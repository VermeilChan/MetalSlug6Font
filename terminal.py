import sys
import random
import traceback

from colorama import Fore

import sys
sys.dont_write_bytecode = True

from color import COLORS
from main import generate_filename, generate_image_with_filename, get_font_paths, font

# Disable writing compiled bytecode files
sys.dont_write_bytecode = True 

def main():
    # Print a note about compatibility
    print(Fore.RED + "Note: Metal Slug font style conversion may not be compatible with all fonts. Refer to the SUPPORTED.md file for details.")
    
    # Start an infinite loop for user input
    while True:
        # Choose a random color from the COLORS list
        color_choice = random.choice(COLORS)
        # Prompt the user for input
        text = input(f"{color_choice}Enter Text: ")
        
        if not text:
            # Exit loop if no input is provided
            print(f"{color_choice}Goodbye!")
            break

        try:
            # Generate a filename based on the entered text
            filename = generate_filename(text)
            # Get the paths of available fonts
            font_paths = get_font_paths(font)
            # Generate an image with the given text and font
            img_path, error_message = generate_image_with_filename(text, filename, font_paths)
            
            if error_message:
                # Print error message if there's an issue
                print(f"{color_choice}Error: {error_message}")
            else:
                # Print success message with image path
                print(f"{color_choice}Image generated successfully: {img_path}")
        except Exception as e:
            # Print an error message if an exception occurs
            print(f"{color_choice}An error occurred: {e}")
            # Print the traceback for debugging purposes
            traceback.print_exc()

if __name__ == "__main__":
    main()
