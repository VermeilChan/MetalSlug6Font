import os
from PIL import Image

def resize_images_in_directory(directory, output_directory, scale_factor=4):
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    input_path = os.path.join(root, filename)
                    output_path = os.path.join(output_directory, os.path.relpath(input_path, directory))
                    
                    output_subdirectory = os.path.dirname(output_path)
                    if not os.path.exists(output_subdirectory):
                        os.makedirs(output_subdirectory)
                    
                    img = Image.open(input_path)
                    new_width = img.width * scale_factor
                    new_height = img.height * scale_factor
                    resized_img = img.resize((new_width, new_height), Image.BILINEAR)
                    resized_img.save(output_path)
                    print(f"Image '{filename}' resized and saved successfully.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    input_directory = "assets"  # Replace with your input directory path
    output_directory = "resized_assets"  # Replace with your desired output directory path
    resize_images_in_directory(input_directory, output_directory)
