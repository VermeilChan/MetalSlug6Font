import sys
import traceback

sys.dont_write_bytecode = True

from main import generate_filename, generate_image_with_filename, get_font_paths, font, color

def display_intro_message():
    print("Note: Metal Slug font style conversion may not be compatible with all fonts."
            " Refer to the SUPPORTED.md file for details.")

def get_user_input():
    return input("Enter Text: ")

def generate_and_display_image(text):
    try:
        filename = generate_filename(text)
        font_paths = get_font_paths(font, color)
        img_path, error_message = generate_image_with_filename(text, filename, font_paths)

        if error_message:
            print(f"Error: {error_message}")
        else:
            print(f"Image generated successfully: {img_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

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
