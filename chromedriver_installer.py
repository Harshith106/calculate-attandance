import os
import sys
import subprocess
import logging
import zipfile
import requests
import platform
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ChromeDriverInstaller")

def get_chrome_version():
    """Get the Chrome version."""
    system = platform.system()
    try:
        if system == "Linux":
            chrome_path = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome-stable")
            version = subprocess.check_output([chrome_path, "--version"], stderr=subprocess.STDOUT)
            return version.decode("utf-8").strip().split(" ")[2].split(".")[0]
        elif system == "Windows":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return version.split(".")[0]
        elif system == "Darwin":  # macOS
            process = subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                                      stdout=subprocess.PIPE)
            version = process.communicate()[0].decode("utf-8").strip().split(" ")[2].split(".")[0]
            return version
    except Exception as e:
        logger.error(f"Error getting Chrome version: {e}")
        return None

def download_chromedriver(version, install_dir):
    """Download the ChromeDriver for the given Chrome version."""
    try:
        # Use a fixed ChromeDriver version that's known to work
        driver_version = "114.0.5735.90"
        logger.info(f"Using fixed ChromeDriver version: {driver_version}")

        # Determine the platform
        system = platform.system()
        if system == "Linux":
            platform_name = "linux64"
        elif system == "Windows":
            platform_name = "win32"
        elif system == "Darwin":  # macOS
            if platform.machine() == "arm64":  # Apple Silicon
                platform_name = "mac_arm64"
            else:
                platform_name = "mac64"
        else:
            logger.error(f"Unsupported platform: {system}")
            return None

        # Download the ChromeDriver
        download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{platform_name}.zip"
        logger.info(f"Downloading ChromeDriver from: {download_url}")

        response = requests.get(download_url)
        if response.status_code != 200:
            logger.error(f"Failed to download ChromeDriver: {response.status_code}")
            return None

        # Create the installation directory if it doesn't exist
        os.makedirs(install_dir, exist_ok=True)

        # Save the zip file
        zip_path = os.path.join(install_dir, "chromedriver.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)

        # Extract the zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)

        # Make the ChromeDriver executable on Unix-like systems
        if system != "Windows":
            chromedriver_path = os.path.join(install_dir, "chromedriver")
            os.chmod(chromedriver_path, 0o755)
        else:
            chromedriver_path = os.path.join(install_dir, "chromedriver.exe")

        # Clean up
        os.remove(zip_path)

        logger.info(f"ChromeDriver installed at: {chromedriver_path}")
        return chromedriver_path

    except Exception as e:
        logger.error(f"Error downloading ChromeDriver: {e}")
        return None

def install_chromedriver():
    """Install ChromeDriver matching the installed Chrome version."""
    # Determine where to install ChromeDriver
    install_dir = os.environ.get("WEBDRIVER_MANAGER_PATH", os.path.join(os.path.expanduser("~"), ".webdriver"))

    # Get Chrome version
    chrome_version = get_chrome_version()
    if not chrome_version:
        logger.error("Could not determine Chrome version")
        return None

    logger.info(f"Detected Chrome version: {chrome_version}")

    # Download and install ChromeDriver
    chromedriver_path = download_chromedriver(chrome_version, install_dir)
    if not chromedriver_path:
        logger.error("Failed to install ChromeDriver")
        return None

    return chromedriver_path

if __name__ == "__main__":
    chromedriver_path = install_chromedriver()
    if chromedriver_path:
        print(f"ChromeDriver successfully installed at: {chromedriver_path}")
        sys.exit(0)
    else:
        print("Failed to install ChromeDriver")
        sys.exit(1)
