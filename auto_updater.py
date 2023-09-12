import os
import logging
import requests
import time

from tqdm import tqdm

# Constants and variables
GITHUB_OWNER = 'VermeilChan'
GITHUB_REPO = 'MetalSlugFont'
RELEASE_FILE_EXTENSION = '.exe'
CURRENT_VERSION = '0.2.5'
DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads')
LOG_FILE = 'updates.log'
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest'
DOWNLOAD_URL = None

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Function to check for updates
def check_for_updates():
    try:
        latest_version, download_url = get_latest_version_and_download_url()
        
        if latest_version == CURRENT_VERSION:
            print(f"You are currently running version {CURRENT_VERSION}, which is up to date.")
            logging.info(f"Running version {CURRENT_VERSION}. No updates available.")
        else:
            while True:
                update_confirmation = input(f"You are currently running version {CURRENT_VERSION}. Do you want to update to version {latest_version}? (yes/no): ").strip().lower()
                if update_confirmation in ('yes', 'y'):
                    if is_update_file_exist(download_url):
                        while True:
                            update_file_confirmation = input("A file with the same name already exists. Do you want to overwrite it? (yes/no): ").strip().lower()
                            if update_file_confirmation in ('yes', 'y'):
                                download_update(download_url, latest_version)
                                break
                            elif update_file_confirmation in ('no', 'n'):
                                print("Update canceled.")
                                logging.info("Update canceled by the user.")
                                break
                            else:
                                print("Invalid input. Please enter 'yes' or 'no'.")
                                logging.warning("Invalid input for update file confirmation.")
                    else:
                        download_update(download_url, latest_version)
                    break
                elif update_confirmation in ('no', 'n'):
                    print("Update canceled.")
                    logging.info("Update canceled by the user.")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    logging.warning("Invalid input for update confirmation.")
    except requests.exceptions.RequestException as e:
        handle_error("Failed to check for updates. Please check your internet connection.", e)
    except Exception as e:
        handle_error("An unexpected error occurred while checking for updates.", e)

# Function to check if the download folder exists and is accessible
def is_download_folder_available():
    return os.path.isdir(DOWNLOAD_FOLDER)

# Function to check if the update file already exists
def is_update_file_exist(download_url):
    download_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(download_url))
    return os.path.exists(download_path)

# Function to get the latest version and download URL
def get_latest_version_and_download_url():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36',
        }

        response = requests.get(GITHUB_API_URL, headers=headers, verify=True)  # Use HTTPS with SSL certificate verification
        response.raise_for_status()
        
        # Handle rate limiting
        remaining_requests = int(response.headers.get('X-RateLimit-Remaining', 0))
        if remaining_requests <= 0:
            reset_timestamp = int(response.headers.get('X-RateLimit-Reset', 0))
            current_time = time.time()
            sleep_time = max(0, reset_timestamp - current_time)
            print(f"Rate limit exceeded. Sleeping for {sleep_time:.0f} seconds until the rate limit is reset.")
            time.sleep(sleep_time)
            return get_latest_version_and_download_url()  # Retry the request after sleeping
        
        release_data = response.json()
        latest_version = release_data['tag_name']
        
        if latest_version != CURRENT_VERSION:
            download_url = get_download_url(release_data)
            return latest_version, download_url
        else:
            return latest_version, None
    except requests.exceptions.RequestException as e:
        handle_error("Failed to retrieve release data. Please check your internet connection.", e)
    except Exception as e:
        handle_error("An unexpected error occurred while processing release data.", e)

# Function to get the download URL for the latest release
def get_download_url(release_data):
    for asset in release_data['assets']:
        if asset['name'].endswith(RELEASE_FILE_EXTENSION):
            return asset['browser_download_url']

# Function to download and update the program
def download_update(download_url, latest_version):
    try:
        # Create the download folder if it doesn't exist
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        # Define the path for the downloaded file (using the original file name)
        download_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(download_url))
        
        if os.path.exists(download_path):
            while True:
                update_file_confirmation = input("Are you sure you want to overwrite it? (yes/no): ").strip().lower()
                if update_file_confirmation in ('yes', 'y'):
                    break
                elif update_file_confirmation in ('no', 'n'):
                    print("Update canceled.")
                    logging.info("Update canceled by the user.")
                    return
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
                    logging.warning("Invalid input for update file confirmation.")

        # Download the update with a progress bar
        with requests.get(download_url, stream=True, verify=True) as response, open(download_path, 'wb') as outfile:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                outfile.write(data)

            progress_bar.close()

        print(f"\nUpdate downloaded to: {download_path}")

        # Log the update
        log_update(latest_version)

        # Print post-update instructions
        print("\nUpdate complete. Please close the application.")
        print("Go to your downloads folder and reinstall the program.")
        print("Before that, remove the 'MSFONT' folder.\n")
    except requests.exceptions.RequestException as e:
        handle_error("Failed to download update. Please check your internet connection.", e)
    except Exception as e:
        handle_error("An unexpected error occurred while downloading the update.", e)

# Function to log the update
def log_update(version):
    try:
        if is_log_file_writable():
            with open(LOG_FILE, 'a') as log:
                log.write(f"Updated to version {version}\n")
        else:
            print("Log file is not writable. Update could not be logged.")
    except Exception as e:
        handle_error("Failed to log update.", e)

# Function to check if the log file exists and is writable
def is_log_file_writable():
    return os.access(LOG_FILE, os.W_OK)

# Function to handle errors
def handle_error(message, error):
    logging.error(f"{message}: {error}")
    print(f"An error occurred: {error}")

if __name__ == '__main__':
    while True:
        user_input = input("Type 'Update' to check for updates or 'exit' to exit: ").strip().lower()
        
        if user_input == 'update':
            check_for_updates()
        elif user_input == 'exit':
            print("Exiting the program.")
            logging.info("Exiting the program.")
            break
        else:
            print("Invalid input. Please type 'Update' to check for updates or 'exit' to exit.")
            logging.warning("Invalid input from the user.")
