# Import necessary libraries
import os
import time
import click
import shutil
import logging
import requests
from logging.handlers import RotatingFileHandler
from requests.exceptions import RequestException

import semantic_version
from tqdm import tqdm

# Constants
GITHUB_OWNER = 'VermeilChan'
GITHUB_REPO = 'MetalSlugFont'
RELEASE_FILE_EXTENSION = '.exe'
CURRENT_VERSION = '0.2.6'
LOG_FILE = 'updates.log'
DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads')
VERIFY_SSL_CERTIFICATE = True

# Configure logging with log rotation
logger = logging.getLogger('updates')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Custom exception for rate limit exceeded
class RateLimitExceededError(Exception):
    def __init__(self, sleep_time):
        self.sleep_time = sleep_time

# Function to check for updates
def check_for_updates(update_folder):
    try:
        logger.info("Update check started.")
        latest_version_str, download_url = get_latest_version_and_download_url()
        current_version = semantic_version.Version(CURRENT_VERSION)
        latest_version = semantic_version.Version(latest_version_str)

        if latest_version == current_version:
            logger.info(f"You are currently running version {CURRENT_VERSION}, which is up to date.")
            click.echo(f"You are currently running version {CURRENT_VERSION}, which is up to date.")
        else:
            update_confirmation = click.confirm(f"You are currently running version {CURRENT_VERSION}. Do you want to update to version {latest_version_str}?")

            if update_confirmation:
                if is_update_file_exist(download_url):
                    update_file_confirmation = click.confirm("A file with the same name already exists. Do you want to overwrite it?")
                    if not update_file_confirmation:
                        click.echo("Update canceled.")
                        logger.info("Update canceled by the user.")
                        return
                download_update(download_url, latest_version_str, update_folder)
            else:
                click.echo("Update canceled.")
                logger.info("Update canceled by the user.")
    except RequestException as e:
        # Retry the request with SSL certificate verification disabled if it fails
        if VERIFY_SSL_CERTIFICATE:
            click.echo("Failed to check for updates with SSL certificate verification enabled. Retrying with verification disabled...")
            logger.warning("Failed to check for updates with SSL certificate verification enabled. Retrying with verification disabled...")
            VERIFY_SSL_CERTIFICATE = False
            check_for_updates(update_folder)
        else:
            handle_error("Failed to check for updates even with SSL certificate verification disabled. Please check your internet connection.", e)
    except RateLimitExceededError as e:
        click.echo(f"Rate limit exceeded. Sleeping for {e.sleep_time:.0f} seconds until the rate limit is reset.")
        time.sleep(e.sleep_time)
        check_for_updates(update_folder)
    except Exception as e:
        handle_error("An unexpected error occurred while checking for updates.", e)
    finally:
        logger.info("Update check finished.")

# Function to check if the download folder exists and is accessible
def is_download_folder_available(download_folder):
    return os.path.isdir(download_folder)

# Function to check if the update file already exists
def is_update_file_exist(download_url):
    download_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(download_url))
    return os.path.exists(download_path)

# Function to get the latest version and download URL
def get_latest_version_and_download_url():
    try:
        headers = {
            'User-Agent': 'Mozilla/117.0.1 (Windows NT 11.0; Win64; x64; rv:117.0) Gecko/20230901 AppleWebKit/537.43 (KHTML, like Gecko) Chrome/117.0.5938.62 Safari/605.1.15 Edg/116.0.1938.81 OPR/102.0.4871.0 YaBrowser/23.7.0.2592 Firefox/117.0.1'
        }

        response = requests.get(f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest', headers=headers, verify=VERIFY_SSL_CERTIFICATE)
        response.raise_for_status()

        # Check rate limiting headers
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
        else:
            return latest_version_str, None
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
def download_update(download_url, latest_version_str, update_folder):
    try:
        os.makedirs(update_folder, exist_ok=True)
        download_path = os.path.join(update_folder, os.path.basename(download_url))
        temp_download_path = download_path + '.temp'

        with requests.get(download_url, stream=True, verify=VERIFY_SSL_CERTIFICATE) as response, open(temp_download_path, 'ab') as outfile:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading", ncols=80)

            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                outfile.write(data)

            progress_bar.close()

        shutil.move(temp_download_path, download_path)

        logger.info(f"Update downloaded to: {download_path}")
        click.echo(f"\nUpdate downloaded to: {download_path}")

        log_update(latest_version_str)

        click.echo("\nUpdate complete. Please close the program.")
        click.echo("Go to your downloads folder and reinstall the program.")
        click.echo("Before that, remove the 'MSFONT' folder.\n")
    except requests.exceptions.RequestException as e:
        handle_error("Failed to download the update. Please check your internet connection.", e)
    except Exception as e:
        handle_error("An unexpected error occurred while downloading the update.", e)

# Function to log the update
def log_update(version_str):
    try:
        if is_log_file_writable():
            with open(LOG_FILE, 'a') as log:
                log.write(f"\nUpdated to version {version_str}")
                logger.info(f"Updated to version {version_str}")
        else:
            click.echo("The log file is not writable. The update could not be logged.")
    except Exception as e:
        handle_error("Failed to log the update.", e)

# Function to check if the log file exists and is writable
def is_log_file_writable():
    return os.access(LOG_FILE, os.W_OK)

# Function to handle errors
def handle_error(message, error):
    logger.error(f"{message}: {error}")
    click.echo(f"An error occurred: {error}")

if __name__ == '__main__':
    while True:
        user_input = click.prompt("Type 'Update' to check for updates or 'exit' to exit").strip().lower()

        if user_input == 'update':
            check_for_updates(DOWNLOAD_FOLDER)
        elif user_input == 'exit':
            click.echo("Exiting the program...")
            logger.info("Exiting the program...")
            break
        else:
            click.echo("Invalid input. Please type 'Update' to check for updates or 'exit' to exit.")
