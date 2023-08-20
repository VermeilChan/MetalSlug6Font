import sys
import random
from color import COLORS
from main import generate_filename, generate_image_with_filename

# Prevent the generation of __pycache__ directories
sys.dont_write_bytecode = True

# Main function
def main():
    print("Note: Using the Metal Slug font style to turn text into images might not work perfectly with all fonts. Check The SUPPORTED.md file for more information")
    
    while True:
        text = input(random.choice(COLORS) + "Enter the desired output (press Enter to quit): ")
        
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
