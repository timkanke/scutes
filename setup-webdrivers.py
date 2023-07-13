import logging
import requests
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gecko Driver
gecko_version = 'v0.33.0'
gecko_os_type = 'macos-aarch64'
gecko_filename = f'geckodriver-{gecko_version}-{gecko_os_type}.tar.gz'
gecko_url = f'https://github.com/mozilla/geckodriver/releases/download/{gecko_version}/{gecko_filename}'

# Chrome Driver
chrome_version = '114.0.5735.133'
chrome_os_type = 'mac-arm64'
chrome_filename = f'chrome-{chrome_os_type}.zip'
chrome_url = f'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chrome_version}/{chrome_os_type}/{chrome_filename}'

# Save location
base_path = Path('.venv/bin')

# Webdriver lists
webdriver_filename_list = [gecko_filename, chrome_filename]
webdriver_url_list = [gecko_url, chrome_url]


def download_webdriver():
    for webdriver_filename, webdriver_url in zip(webdriver_filename_list, webdriver_url_list):
        file_path = Path(base_path / webdriver_filename)
        requested_url = webdriver_url
        try:
            logger.info(f'Downloading {webdriver_filename}')
            with open(file_path, 'wb') as file:
                r = requests.get(requested_url, stream=True)
                for chunk in r.raw.stream(1024, decode_content=False): 
                    if chunk:
                        file.write(chunk)
                        file.flush()
        except requests.exceptions.HTTPError as errh:
            logger.error("HTTP Error")
            logger.error(errh.args[0])
        except requests.exceptions.ReadTimeout as errt:
            logger.error("Time out")
        except requests.exceptions.ConnectionError as errcon:
            logger.error("Connection error")
        except requests.exceptions.RequestException as errex:
            logger.error("Exception request")


if __name__ == "__main__":
    download_webdriver()
