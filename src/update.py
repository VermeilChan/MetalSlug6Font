import os
import sys
import time
import shutil
import requests
import platform
import subprocess
import semantic_version
import tkinter as tk
from tkinter import ttk, messagebox
from fake_useragent import UserAgent

# Define constants
GITHUB_OWNER = 'VermeilChan'
GITHUB_REPO = 'MetalSlugFont'

RELEASE_FILE_EXTENSION = '.exe'
CURRENT_VERSION = '0.3.7'

VERIFY_SSL = True

MAX_RETRIES = 3

ERROR_MESSAGE = "Launch Error"

# Custom Exception for Rate Limit Exceeded
class RateLimitExceededError(Exception):
    def __init__(self, sleep_time):
        self.sleep_time = sleep_time

# Function to get a random user agent for making HTTP requests
def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

# Function to check for updates
def check_for_updates(root):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            latest_version_str, download_url = get_latest_version_and_download_url()
            current_version = semantic_version.Version(CURRENT_VERSION)
            latest_version = semantic_version.Version(latest_version_str)

            if latest_version == current_version:
                show_up_to_date_message(current_version)
            else:
                handle_update_confirmation(download_url, root)

            break
        except RateLimitExceededError as e:
            handle_rate_limit_exceeded(e)
        except Exception as e:
            handle_error(f"An unexpected error occurred while processing release data: {e}")

    if retries == MAX_RETRIES:
        messagebox.showerror("Update Error", "Maximum retry limit reached. Unable to check for updates.")

def show_up_to_date_message(current_version):
    messagebox.showinfo("Update Check", f"You are currently running version '{current_version}', which is up to date.")

def handle_update_confirmation(download_url, root):
    result = messagebox.askquestion("Update Available", f"You are currently running version '{CURRENT_VERSION}', and a newer version is available. Do you want to update?")
    if result == "yes":
        remove_folder = ask_to_remove_folder("MSFONT")
        if remove_folder:
            download_update(download_url, root)
        else:
            messagebox.showinfo("Update Canceled", "Update canceled by the user.")

# Function to ask the user if they want to remove a folder
def ask_to_remove_folder(folder_name):
    user_response = messagebox.askquestion("Folder Removal", f"Do you want to remove the folder '{folder_name}' (Recommend)?")
    if user_response == "yes":
        folder_path = os.path.join(os.path.expanduser("~"), "Downloads", folder_name)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                messagebox.showinfo("Folder Removed", f"Folder '{folder_name}' removed successfully.")
            except OSError as e:
                messagebox.showerror("Folder Removal Error", f"Error removing folder '{folder_name}': {str(e)}")
        else:
            messagebox.showinfo("Folder Not Found", f"Folder '{folder_name}' does not exist in the 'Downloads' directory.")
    return user_response == "yes"

# Function to handle the update process
def handle_update(download_url, root):
    if is_update_file_exist(download_url):
        messagebox.showerror("Update Error", "An update file with the same name already exists. Update aborted.")
    else:
        download_update(download_url, root)

# Function to handle rate limit exceeded
def handle_rate_limit_exceeded(exception):
    sleep_time = exception.sleep_time
    messagebox.showinfo("Rate Limit Exceeded", f"Rate limit exceeded. Sleeping for {sleep_time:.0f} seconds until the rate limit is reset.")
    time.sleep(sleep_time)

# Function to check if an update file already exists
def is_update_file_exist(download_url):
    download_path = os.path.join(os.path.expanduser("~"), "Downloads", os.path.basename(download_url))
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
def download_update(download_url, root):
    try:
        download_path = os.path.join(os.path.expanduser("~"), "Downloads", os.path.basename(download_url))
        temp_download_path = download_path + '.temp'

        with requests.get(download_url, stream=True, verify=VERIFY_SSL) as response, open(temp_download_path, 'ab') as outfile:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
            progress_bar.grid(column=0, row=3, columnspan=2, pady=10)
            progress_bar["maximum"] = total_size
            progress = 0

            for data in response.iter_content(block_size):
                progress += len(data)
                progress_bar["value"] = progress
                root.update_idletasks()
                outfile.write(data)

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
        messagebox.showerror(ERROR_MESSAGE, f"Error launching the file on Windows: {e}")

# Function to launch a downloaded file on Linux
def launch_on_linux(download_path):
    if is_wine_installed():
        try:
            subprocess.Popen(['wine', download_path])
        except Exception as e:
            messagebox.showerror(ERROR_MESSAGE, f"Error launching the file on Linux: {e}")
    else:
        distro = platform.linux_distribution()[0]
        messagebox.showinfo("Linux Not Supported", f"{distro} Linux support is not implemented.\nWine is not installed. Please install Wine to run this application on Linux.")

# Function to launch a downloaded file on MacOS
def launch_on_macos(download_path):
    macos_version = platform.mac_ver()[0]
    messagebox.showinfo("MacOS Not Supported", f"MacOS {macos_version} support is not implemented.")
    if is_wine_installed():
        try:
            subprocess.Popen(['wine', download_path])
        except Exception as e:
            messagebox.showerror(ERROR_MESSAGE, f"Error launching the file on MacOS: {e}")
    else:
        messagebox.showinfo("MacOS Not Supported", "Wine is not installed. Please install Wine to run this application on MacOS.")

# Function to launch a downloaded file based on the platform
def launch_downloaded_file(download_path):
    current_platform = sys.platform

    if current_platform.startswith('win'):
        launch_on_windows(download_path)
    elif current_platform.startswith('linux'):
        launch_on_linux(download_path)
    elif current_platform == 'darwin':
        launch_on_macos(download_path)
    else:
        messagebox.showinfo("Platform Not Supported", f"{current_platform} support is not implemented.")

# Function to handle and print error messages
def handle_error(error_message):
    messagebox.showerror("Error", error_message)

# Main program entry point
def main():
    root = tk.Tk()
    root.title("Metal Slug Font Updater")

    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, padx=10, pady=10)

    ttk.Label(frame, text="Metal Slug Font Updater", font=("Helvetica", 16)).grid(column=0, row=0, columnspan=2, pady=10)
    ttk.Button(frame, text="Check for Updates", command=lambda: check_for_updates(root)).grid(column=0, row=1, pady=10, padx=5)
    ttk.Button(frame, text="Exit", command=root.quit).grid(column=1, row=1, pady=10, padx=5)

    root.mainloop()

if __name__ == '__main__':
    main()
