# Import necessary libraries
import os
import sys
import time
import shutil
import requests
import platform
import subprocess
import semantic_version

from tqdm import tqdm
from fake_useragent import UserAgent

# Define constants
GITHUB_OWNER = 'VermeilChan'
GITHUB_REPO = 'MetalSlugFont'

RELEASE_FILE_EXTENSION = '.exe'
CURRENT_VERSION = '0.3.7'

DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads')

VERIFY_SSL = True

UPDATE_CANCELLED_MESSAGE = "Update canceled."

MAX_RETRIES = 3

# Custom Exception for Rate Limit Exceeded
class RateLimitExceededError(Exception):
    def __init__(self, sleep_time):
        self.sleep_time = sleep_time

# Function to get a random user agent for making HTTP requests
def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

# Function to check for updates
def check_for_updates(update_folder):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print("Checking for updates...")
            latest_version_str, download_url = get_latest_version_and_download_url()
            current_version = semantic_version.Version(CURRENT_VERSION)
            latest_version = semantic_version.Version(latest_version_str)

            if latest_version == current_version:
                print(f"You are currently running version '{CURRENT_VERSION}', which is up to date.")
            else:
                handle_update_confirmation(download_url, update_folder, current_version, latest_version_str)
            sys.exit(0)
        except RateLimitExceededError as e:
            handle_rate_limit_exceeded(e)
        except Exception as e:
            handle_error(f"An unexpected error occurred while processing release data: {e}")

    if retries == MAX_RETRIES:
        print("Maximum retry limit reached. Unable to check for updates.")

# Function to handle user confirmation for updating
def handle_update_confirmation(download_url, update_folder, current_version, latest_version_str):
    update_confirmation = input(f"You are currently running version '{current_version}', and a newer version '{latest_version_str}' is available. Do you want to update? (yes/no): ").strip().lower()
    if update_confirmation in ('yes', 'y'):
        remove_folder = ask_to_remove_folder("MSFONT")
        if remove_folder:
            handle_update(download_url, update_folder)
        else:
            handle_update_cancelled_by_user()

# Function to ask the user if they want to remove a folder
def ask_to_remove_folder(folder_name):
    user_input = input(f"Do you want to remove the folder '{folder_name}' (Recommend)? (yes/no): ").strip().lower()
    if user_input in ('yes', 'y'):
        folder_path = os.path.join(os.path.expanduser("~"), "Downloads", folder_name)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Folder '{folder_name}' removed successfully.")
            except OSError as e:
                print(f"Error removing folder '{folder_name}': {str(e)}")
        else:
            print(f"Folder '{folder_name}' does not exist in the 'Downloads' directory.")
    return user_input in ('yes', 'y')

# Function to handle the update process
def handle_update(download_url, update_folder):
    if is_update_file_exist(download_url):
        print("An update file with the same name already exists. Update aborted.")
    else:
        download_update(download_url, update_folder)

# Function to handle rate limit exceeded
def handle_rate_limit_exceeded(exception):
    sleep_time = exception.sleep_time
    print(f"Rate limit exceeded. Sleeping for {sleep_time:.0f} seconds until the rate limit is reset.")
    time.sleep(sleep_time)

# Function to handle update cancellation by the user
def handle_update_cancelled_by_user():
    print(UPDATE_CANCELLED_MESSAGE)

# Function to check if an update file already exists
def is_update_file_exist(download_url):
    download_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(download_url))
    return os.path.exists(download_path)

# Function to get the latest version and download URL from GitHub
def get_latest_version_and_download_url():
    try:
        headers = {
            'User-Agent': get_random_user_agent()
        }

        response = requests.get(f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest', headers=headers, verify=VERIFY_SSL)
        response.raise_for_status()

        remaining_requests = int(response.headers.get('X-RateLimit-Remaining', 0))
        reset_timestamp = int(response.headers.get('X-RateLimit-Reset', 0))
        current_time = time.time()

        if remaining_requests <= 0:
            sleep_time = max(0, reset_timestamp - current_time)
            raise RateLimitExceededError(sleep_time)

        release_data = response.json()
        latest_version_str = release_data['tag_name']

        if latest_version_str != CURRENT_VERSION:
            download_url = get_download_url(release_data)
            return latest_version_str, download_url
        return latest_version_str, None
    except requests.exceptions.RequestException as e:
        handle_error(f"Failed to retrieve release data. Please check your internet connection: {e}")

# Function to get the download URL from the release data
def get_download_url(release_data):
    for asset in release_data['assets']:
        if asset['name'].endswith(RELEASE_FILE_EXTENSION):
            return asset['browser_download_url']

# Function to download the update
def download_update(download_url, update_folder):
    try:
        os.makedirs(update_folder, exist_ok=True)
        download_path = os.path.join(update_folder, os.path.basename(download_url))
        temp_download_path = download_path + '.temp'

        with requests.get(download_url, stream=True, verify=VERIFY_SSL) as response, open(temp_download_path, 'ab') as outfile:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading", ncols=80)

            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                outfile.write(data)

            progress_bar.close()

        shutil.move(temp_download_path, download_path)

        # Wait 3 seconds before starting the executable
        time.sleep(3)

        # Launch the downloaded file
        launch_downloaded_file(download_path)

    except requests.exceptions.RequestException as e:
        handle_error(f"Failed to download the update. Please check your internet connection: {e}")

# Function to check if Wine is installed
def is_wine_installed():
    try:
        subprocess.check_call(['wine', '--version'])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to launch a downloaded file on Windows
def launch_on_windows(download_path):
    try:
        subprocess.Popen([download_path])
    except Exception as e:
        print(f"Error launching the file on Windows: {e}")

# Function to launch a downloaded file on Linux
def launch_on_linux(download_path):
    if is_wine_installed():
        try:
            subprocess.Popen(['wine', download_path])
        except Exception as e:
            print(f"Error launching the file on Linux: {e}")
    else:
        distro = platform.linux_distribution()[0]
        print(f"{distro} Linux support is not implemented.")
        print("Wine is not installed. Please install Wine to run this application on Linux.")

# Function to launch a downloaded file on MacOS
def launch_on_macos(download_path):
    macos_version = platform.mac_ver()[0]
    print(f"MacOS {macos_version} support is not implemented.")
    if is_wine_installed():
        try:
            subprocess.Popen(['wine', download_path])
        except Exception as e:
            print(f"Error launching the file on MacOS: {e}")
    else:
        print("Wine is not installed. Please install Wine to run this application on MacOS.")

# Main function to launch a downloaded file based on the platform
def launch_downloaded_file(download_path):
    current_platform = sys.platform

    if current_platform.startswith('win'):
        launch_on_windows(download_path)
    elif current_platform.startswith('linux'):
        launch_on_linux(download_path)
    elif current_platform == 'darwin':
        launch_on_macos(download_path)
    else:
        print(f"{current_platform} support is not implemented.")

# Function to handle and print error messages
def handle_error(error_message):
    print(error_message)

# Main program entry point
if __name__ == '__main__':
    while True:
        user_input = input("Type 'Update' to check for updates or 'exit' to exit: ").strip().lower()

        if user_input == 'update':
            check_for_updates(DOWNLOAD_FOLDER)
        elif user_input == 'exit':
            print("Exiting the program...")
            sys.exit(0)
        else:
            print("Invalid input. Please type 'Update' to check for updates or 'exit' to exit.")


