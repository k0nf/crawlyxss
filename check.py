import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

def check_for_xss(url_list):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    with webdriver.Chrome(options=chrome_options) as driver:
        for i, url in enumerate(url_list):
            print(f"Processing URL {i+1}/{len(url_list)}: {url}")
            try:
                driver.get(url)
                try:
                    WebDriverWait(driver, 5).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                    domain = urlparse(url).netloc
                    filename = f"{domain}_xss.txt"
                    with open(filename, 'a') as f:
                        f.write(f"{url}\n")
                    print(f"XSS vulnerability detected for URL: {url}. Saved to {filename}")
                except UnexpectedAlertPresentException:
                    pass
            except TimeoutException:
                print(f"Timeout occurred while processing URL: {url}. Skipping...")
            except Exception as e:
                print(f"An error occurred while processing URL: {url}. Skipping... Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check URLs for XSS vulnerabilities using Selenium.")
    parser.add_argument("-l", "--list", help="Path to the file containing the list of URLs", required=True)
    args = parser.parse_args()

    url_file = args.list
    urls = []

    with open(url_file, 'r') as f:
        urls = f.read().splitlines()

    check_for_xss(urls)
