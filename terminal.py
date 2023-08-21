import sys
import random
from colorama import Fore
from color import COLORS
from main import generate_filename, generate_image_with_filename

# Prevent the generation of __pycache__ directories
sys.dont_write_bytecode = True

# Main function
def main():
    print(Fore.RED + "Note: Metal Slug font style conversion may not be compatible with all fonts. Refer to the SUPPORTED.md file for details.")
    while True:
        text = input(random.choice(COLORS) + "Enter Text: ")
        
        if not text:
            print(random.choice(COLORS) + "Goodbye!")
            break

        filename = generate_filename(text)
        img_path, error_message = generate_image_with_filename(text, filename)

        if error_message:
            print(random.choice(COLORS) + error_message)
        else:
            print(random.choice(COLORS) + f"Image generated successfully: {img_path}")

if __name__ == "__main__":
    main()
