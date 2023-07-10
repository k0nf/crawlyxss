import argparse
import os
from urllib.parse import urlparse, parse_qs, urlencode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
import logging

clear = lambda: os.system('clear')
def start_chromedriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)

def check_for_xss_list(urls, payloads):
    driver = start_chromedriver()
    num_urls = len(urls)
    num_payloads = len(payloads)
    num_requests = 0
    num_xss_found = 0

    for i, url in enumerate(urls, 1):
        try:
            driver.get(url)
            alert_present = EC.alert_is_present()(driver)
            if alert_present:
                # print(f"XSS vulnerability found in {url}")
                with open(f"{urlparse(url).netloc}_xss.txt", "a") as f:
                    f.write(f"{url}\n")
                num_xss_found += 1
        except Exception as e:
            logging.error(f"An error occurred while processing URL: {url}", exc_info=True)
            continue
        
        num_requests += 1
        print_statistics(i, num_urls, num_payloads, num_requests, num_xss_found)

    driver.quit()

def check_for_xss_brute(url, payloads, input_elements):
    driver = start_chromedriver()

    try:
        driver.get(url)
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        param_names = list(query_params.keys())
        num_params = len(param_names)
        num_payloads = len(payloads)
        num_requests = 0
        num_xss_found = 0

        for i, param_name in enumerate(param_names, start=1):
            param_values = query_params[param_name]
            for param_value in param_values:
                for payload in payloads:
                    try:
                        url_with_payload = url.replace(f"{param_name}={param_value}", f"{param_name}={urlencode(payload)}")
                        driver.get(url_with_payload)
                        alert_present = EC.alert_is_present()(driver)
                        if alert_present:
                            print(f"XSS vulnerability found in {url_with_payload}")
                            with open(f"{parsed_url.netloc}_xss.txt", "a") as f:
                                f.write(f"{url_with_payload}\n")
                            num_xss_found += 1
                    except UnexpectedAlertPresentException:
                        pass
                    except Exception as e:
                        pass

                    num_requests += 1

                    print_statistics(i, num_params, num_payloads, num_requests, num_xss_found)

        for i, element in enumerate(input_elements, start=len(param_names)+1):
            param_name = element.get_attribute("name")
            param_value = element.get_attribute("value")
            if param_name and param_value:
                for payload in payloads:
                    try:
                        url_with_payload = url.replace(f"{param_name}={param_value}", f"{param_name}={urlencode(payload)}")
                        driver.get(url_with_payload)
                        alert_present = EC.alert_is_present()(driver)
                        if alert_present:
                            print(f"XSS vulnerability found in {url_with_payload}")
                            with open(f"{parsed_url.netloc}_xss.txt", "a") as f:
                                f.write(f"{url_with_payload}\n")
                            num_xss_found += 1
                    except UnexpectedAlertPresentException:
                        pass
                    except Exception as e:
                        pass

                    num_requests += 1

                    print_statistics(i, len(input_elements), num_payloads, num_requests, num_xss_found)

    except Exception as e:
        logging.error(f"An error occurred while processing URL: {url}", exc_info=True)

    driver.quit()

def print_statistics(current_index, total_items, total_payloads, total_requests, total_xss_found):
    progress = current_index / total_items
    loading_animation = "." * int(progress * 10)
    clear()
    print(f"\rParameters found: {total_items} | Payloads loaded: {total_payloads} | Requests sent: {total_requests} | XSS found: {total_xss_found} [{loading_animation}] ", end="")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check for XSS vulnerabilities using Selenium.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", "-l", help="Path to the file containing a list of URLs")
    group.add_argument("--brute", metavar="URL", help="URL to check with brute-force mode")
    args = parser.parse_args()

    logging.basicConfig(level=logging.ERROR)

    if args.list:
        url_file = args.list
        with open(url_file, "r") as f:
            urls = [line.strip() for line in f.readlines()]
        payloads = []
        with open("payloads.txt", "r") as f:
            payloads = [line.strip() for line in f.readlines()]
        check_for_xss_list(urls, payloads)
    else:
        url = args.brute
        payloads = []
        with open("payloads.txt", "r") as f:
            payloads = [line.strip() for line in f.readlines()]
        driver = start_chromedriver()
        driver.get(url)
        input_elements = driver.find_elements(By.XPATH, "//input[@type='text' or @type='search' or @type='hidden']")
        driver.quit()
        check_for_xss_brute(url, payloads, input_elements)
