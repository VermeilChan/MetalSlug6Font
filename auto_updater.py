# Import necessary libraries
import os
import time
import click
import shutil
import logging
import requests
import semantic_version

from tqdm import tqdm
from fake_useragent import UserAgent
from logging.handlers import RotatingFileHandler

# GitHub settings
GITHUB_OWNER = 'VermeilChan'
GITHUB_REPO = 'MetalSlugFont'

# Release settings
RFEW = '.exe'
CURRENT_VERSION = '0.2.6'

# Logging settings
LOG_FILE = 'updates.log'

# Download settings
DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads')

# Security settings
VERIFY_SSL_CERTIFICATE = True

# Update messages
UPDATE_CANCELLED_MESSAGE = "Update canceled."
UPDATE_CANCELLED_BY_USER_MESSAGE = "Update canceled by the user."

# Retry settings
MAX_RETRIES = 3

# Configure the logger
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

# Function to generate a random user agent
def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

# Function to check for updates
def check_for_updates(update_folder):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            logger.info("Checking for updates...")
            latest_version_str, download_url = get_latest_version_and_download_url()
            current_version = semantic_version.Version(CURRENT_VERSION)
            latest_version = semantic_version.Version(latest_version_str)

            if latest_version == current_version:
                display_up_to_date_message()
            else:
                handle_update_confirmation(download_url, latest_version_str, update_folder)
            break
        except RateLimitExceededError as e:
            handle_rate_limit_exceeded(e)
        except semantic_version.InvalidVersion as e:
            handle_error("Failed to parse version data: %s", e)
        except click.Abort:
            handle_update_cancelled_by_user()
        except requests.exceptions.RequestException as e:
            handle_error("Failed to retrieve release data. Please check your internet connection: %s", e)
        except Exception as e:
            handle_error("An unexpected error occurred while processing release data: %s", e)
        finally:
            logger.info("Update check finished.")

    if retries == MAX_RETRIES:
        click.echo("Maximum retry limit reached. Unable to check for updates.")

# Function to handle update confirmation
def handle_update_confirmation(download_url, latest_version_str, update_folder):
    update_confirmation = click.confirm(f"You are currently running version {CURRENT_VERSION}. Do you want to update to version {latest_version_str}?")
    if update_confirmation:
        handle_update(download_url, latest_version_str, update_folder)
    else:
        handle_update_cancelled_by_user()

# Function to handle update
def handle_update(download_url, latest_version_str, update_folder):
    if is_update_file_exist(download_url):
        click.echo("An update file with the same name already exists. Update aborted.")
        logger.warning("Update file already exists. Update aborted.")
    else:
        download_update(download_url, latest_version_str, update_folder)

# Function to display up-to-date message
def display_up_to_date_message():
    logger.info(f"You are currently running version {CURRENT_VERSION}, which is up to date.")
    click.echo(f"You are currently running version {CURRENT_VERSION}, which is up to date.")

# Function to handle rate limit exceeded
def handle_rate_limit_exceeded(exception):
    sleep_time = exception.sleep_time
    click.echo(f"Rate limit exceeded. Sleeping for {sleep_time:.0f} seconds until the rate limit is reset.")
    time.sleep(sleep_time)

# Function to handle update canceled by the user
def handle_update_cancelled_by_user():
    click.echo(UPDATE_CANCELLED_MESSAGE)
    logger.info(UPDATE_CANCELLED_BY_USER_MESSAGE)

# Function to check if an update file already exists
def is_update_file_exist(download_url):
    download_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(download_url))
    return os.path.exists(download_path)

# Function to retrieve the latest version and download URL
def get_latest_version_and_download_url():
    try:
        headers = {
            'User-Agent': get_random_user_agent()  # Use random user agent
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
        handle_error("Failed to retrieve release data. Please check your internet connection: %s", e)

# Function to retrieve the download URL from release data
def get_download_url(release_data):
    for asset in release_data['assets']:
        if asset['name'].endswith(RFEW):
            return asset['browser_download_url']

# Function to download the update
def download_update(download_url, latest_version_str, update_folder):
    try:
        os.makedirs(update_folder, exist_ok=True)
        download_path = os.path.join(update_folder, os.path.basename(download_url))
        temp_download_path = download_path + '.temp'

        with requests.get(download_url, stream=True, verify=VERIFY_SSL_CERTIFICATE) as response, open(temp_download_path, 'ab') as outfile:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
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

        os.system(download_path) 

    except requests.exceptions.RequestException as e:
        handle_error("Failed to download the update. Please check your internet connection: %s", e)

# Function to log the update
def log_update(version_str):
    try:
        if is_log_file_writable():
            with open(LOG_FILE, 'a'):
                print(f"\nUpdated to version {version_str}")
                logger.info(f"Updated to version {version_str}")
        else:
            click.echo("The log file is not writable. The update could not be logged.")
    except Exception as e:
        handle_error("Failed to log the update: %s", e)

# Function to check if the log file is writable
def is_log_file_writable():
    return os.access(LOG_FILE, os.W_OK)

# Function to handle errors
def handle_error(message, error):
    logger.error(message, error)
    click.echo("An error occurred: %s" % error)

# Entry point of the script
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


