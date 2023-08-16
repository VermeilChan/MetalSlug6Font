import os
import logging

def clean_up_images(directory_path):
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        
        # Set up logging
        log_file = os.path.join(directory_path, "cleanup_log.txt")
        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logger = logging.getLogger(__name__)
        
        logger.info("Cleanup process started.")
        
        # Get a list of all files in the directory
        file_list = os.listdir(directory_path)
        
        for file_name in file_list:
            # Construct the full path of the file
            file_path = os.path.join(directory_path, file_name)
            
            # Check if the path is a file (not a subdirectory)
            if os.path.isfile(file_path):
                # Check if the file has a .png extension
                if file_name.lower().endswith('.png'):
                    # Remove the file
                    os.remove(file_path)
                    logger.info(f"Removed: {file_path}")
                else:
                    logger.info(f"Skipped (not a .png file): {file_path}")
        
        logger.info("Cleanup complete.")
        
    except FileNotFoundError:
        logger.error("Directory not found.")
    except PermissionError:
        logger.error("Permission denied.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Specify the directory path to clean up
directory_to_clean = "/home/Vermeil/MetalSlugFont/static/Generated_Images"

# Call the cleanup function
clean_up_images(directory_to_clean)
