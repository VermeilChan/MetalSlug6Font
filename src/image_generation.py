from uuid import uuid4
from os import path, makedirs
from PIL import Image

special_characters = {
    "!": "exclamation",
    "?": "question",
}


def generate_filename():
    unique_id = uuid4().hex
    return f"{unique_id}.png"


def get_font_paths(font, color):
    base_path = path.join(
        "src", "static", "assets", "fonts", f"font-{font}", f"ms-{color}"
    )
    return [
        path.join(base_path, folder) for folder in ("letters", "numbers", "symbols")
    ]


def get_character_image_path(character, font_paths):
    characters_folder, numbers_folder, symbols_folder = font_paths

    if character.isspace():
        return None
    elif character.islower():
        character_image_path = path.join(
            characters_folder, "lower-case", f"{character}.png"
        )
    elif character.isupper():
        character_image_path = path.join(
            characters_folder, "upper-case", f"{character}.png"
        )
    elif character.isdigit():
        character_image_path = path.join(numbers_folder, f"{character}.png")
    else:
        character_image_path = path.join(
            symbols_folder, f"{special_characters.get(character, '')}.png"
        )

    return character_image_path


def get_character_image(character, font_paths):
    if character.isspace():
        return Image.new("RGBA", (30, 1), (0, 0, 0, 0))

    character_image_path = get_character_image_path(character, font_paths)
    if not character_image_path or not path.isfile(character_image_path):
        raise FileNotFoundError(
            f"The character '{character}' is not supported, please check the supported characters "
        )

    return Image.open(character_image_path)


def generate_image(text, image_filename, font_paths):
    font_images = {c: get_character_image(c, font_paths) for c in set(text)}

    total_width = sum(font_images[c].width for c in text)
    max_height = max(font_images[c].height for c in text)

    final_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    x_position = 0
    for c in text:
        character_image = font_images[c]
        y_position = max_height - character_image.height
        final_image.paste(character_image, (x_position, y_position))
        x_position += character_image.width

    image_directory = path.join("src", "static", "generated-images")
    makedirs(image_directory, exist_ok=True)

    image_path = path.join(image_directory, image_filename)
    final_image.save(image_path, optimize=True)

    image_url = f"static/generated-images/{image_filename}"

    return image_url, None
