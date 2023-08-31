import sys
import random
import traceback

# Don't Move This Anymore !!
sys.dont_write_bytecode = True

from color import COLORS
from colorama import Fore
from main import generate_filename, generate_image_with_filename, get_font_paths, font , color



def display_intro_message():
    print(f"{Fore.RED}Note: Metal Slug font style conversion may not be compatible with all fonts."
            " Refer to the SUPPORTED.md file for details.")

def get_user_input(color_choice):
    return input(f"{color_choice}Enter Text: ")

def generate_and_display_image(text, color_choice):
    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(font , color)
        img_path, error_message = generate_image_with_filename(text, filename, font_paths)

        if error_message:
            print(f"{color_choice}Error: {error_message}")
        else:
            print(f"{color_choice}Image generated successfully: {img_path}")
    except Exception as e:
        print(f"{color_choice}An error occurred: {e}")
        traceback.print_exc()

def main():
    color_choice = random.choice(COLORS)
    display_intro_message()

    while True:
        text = get_user_input(color_choice)

        if not text:
            print(f"{color_choice}Closing...")
            break

        generate_and_display_image(text, color_choice)

if __name__ == "__main__":
    main()
