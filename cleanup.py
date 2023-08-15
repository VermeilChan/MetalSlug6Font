import os

GENERATED_IMAGES_DIR = os.path.join('static', 'Generated_Images')

def cleanup_generated_images():
    for filename in os.listdir(GENERATED_IMAGES_DIR):
        file_path = os.path.join(GENERATED_IMAGES_DIR, filename)
        os.remove(file_path)
