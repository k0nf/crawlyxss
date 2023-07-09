import argparse
import requests
from urllib.parse import urlparse, parse_qs, urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def find_links_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            absolute_url = urljoin(base_url, href)
            if absolute_url.startswith(base_url):
                links.append(absolute_url)
    return links

def find_input_fields(html):
    soup = BeautifulSoup(html, 'html.parser')
    input_fields = []
    for form in soup.find_all('form'):
        for input_field in form.find_all('input'):
            input_name = input_field.get('name')
            if input_name:
                input_fields.append(input_name)
    return input_fields

def process_request(url, headers, param, payload):
    try:
        response = requests.post(url, headers=headers, data={param: payload})
        if response.ok and payload in response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            input_value = soup.find('input', {'name': param}).get('value')
            if input_value != payload:
                return payload, url, param
        return None
    except requests.exceptions.RequestException:
        return None

def save_potential_xss(payload, url, param):
    domain = urlparse(url).netloc
    filename = f"{domain}_potential_xss.txt"
    with open(filename, 'a') as f:
        f.write(f"{url}?{param}={payload}\n")

def save_failed_request(url):
    domain = urlparse(url).netloc
    filename = f"{domain}_failed_requests.txt"
    with open(filename, 'a') as f:
        f.write(f"{url}\n")

def crawl_and_test_characters(url, num_threads):
    visited_urls = set()
    queue = [url]
    valid_params = set()

    with ThreadPoolExecutor(max_workers=num_threads) as xss_executor:
        while queue:
            current_url = queue.pop(0)
            visited_urls.add(current_url)

            try:
                response = requests.get(current_url, headers=headers)
                page_content = response.text

                parsed_url = urlparse(current_url)
                query_params = parse_qs(parsed_url.query)

                for param in query_params:
                    valid_params.add(param)

                input_fields = find_input_fields(page_content)
                for field in input_fields:
                    valid_params.add(field)

                links = find_links_from_html(page_content, current_url)
                for link in links:
                    if link not in visited_urls:
                        queue.append(link)

            except requests.exceptions.RequestException as e:
                print(f"An error occurred while crawling and testing URL: {current_url}")
                print(str(e))
                save_failed_request(current_url)

        num_params = len(valid_params)
        num_payloads = len(all_payloads)

        payloads_tested = 0
        payloads_found = 0
        potential_xss = []

        print(f"{num_params} params found: {', '.join(valid_params)}")
        print(f"{num_payloads} payloads will be used")

        for payload in all_payloads:
            for param in valid_params:
                result = xss_executor.submit(process_request, target_url, headers, param, payload)
                if result.result():
                    payloads_found += 1
                    save_potential_xss(*result.result())
                else:
                    potential_xss.append((payload, target_url, param))
            payloads_tested += 1
            progress = payloads_tested / num_payloads
            loading_animation = "." * int(progress * 10)
            print(f"\r{payloads_tested}/{num_payloads} payloads tested [{loading_animation}] ", end="")

        print(f"\n{payloads_found} XSS payloads found")
        print(f"{len(potential_xss)} potential XSS payloads")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl and test a website for XSS vulnerabilities.")
    parser.add_argument("--url", help="URL of the website to test", required=True)
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use for testing (default: 10)")
    args = parser.parse_args()

    target_url = args.url
    num_threads = args.threads

    with open('payloads.txt', 'r') as f:
        all_payloads = f.read().splitlines()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    crawl_and_test_characters(target_url, num_threads)
