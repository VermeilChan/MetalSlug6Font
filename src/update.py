# Import necessary libraries
import requests
import semantic_version

# GitHub settings
GITHUB_OWNER = 'VermeilChan'
GITHUB_REPO = 'MetalSlugFont'

# Current version
CURRENT_VERSION = '0.2.6'

# Custom exception for rate limit exceeded
class RateLimitExceededError(Exception):
    def __init__(self, sleep_time):
        self.sleep_time = sleep_time

# Function to check for updates
def check_for_updates():
    try:
        latest_version_str = get_latest_version()
        current_version = semantic_version.Version(CURRENT_VERSION)
        latest_version = semantic_version.Version(latest_version_str)

        if latest_version > current_version:
            print(f"\nYour current version ({CURRENT_VERSION}) is outdated. The latest version is {latest_version_str}.\n")
        else:
            print(f"\nYour current version ({CURRENT_VERSION}) is up to date.\n")
    except RateLimitExceededError as e:
        print(f"\nRate limit exceeded. Please try again in {e.sleep_time} seconds.\n")
    except requests.exceptions.RequestException as e:
        print(f"\nFailed to retrieve release data. Please check your internet connection: {e}\n")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}\n")

# Function to retrieve the latest version from GitHub releases
def get_latest_version():
    response = requests.get(f'https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest')
    response.raise_for_status()
    release_data = response.json()
    latest_version_str = release_data['tag_name']
    return latest_version_str

# Entry point of the script
if __name__ == '__main__':
    check_for_updates()
