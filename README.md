# Crawly - XSS Testing Tool

Crawly is a command-line tool for crawling and testing websites for XSS vulnerabilities. It automates the process of scanning URLs, identifying parameters, and testing XSS payloads. It is designed to help bug bounty hunters and security professionals in their web application security testing efforts.

## Features

- Crawls the target website and discovers links and input fields
- Identifies parameters in the URLs and input fields
- Tests XSS payloads against the discovered parameters
- Saves potential XSS vulnerabilities to files
- Supports multithreaded testing for faster execution

## Usage

1. Install the required packages listed in `requirements.txt` using pip:
```
pip install -r requirements.txt
```

2. Run the `crawly.py` script with the following command-line arguments:
```
python3 crawly.py --url [URL] [--threads [NUM_THREADS]] [--gen [NUM_PAYLOADS]]
```

- `--url` (required): URL of the website to test.
- `--threads` (optional, default=10): Number of threads to use for testing.

## Examples

Test a website with default settings:
```
python3 crawly.py --url https://example.com
```

## Requirements

- Python 3.7+
- Requests library
- Beautiful Soup library
- Selenium library (for additional check script)

## Additional Check Script

The additional `check.py` script allows you to navigate to each URL in a text file and check if an alert or prompt is being displayed using Selenium. To use the script, follow these steps:

1. Install the required packages listed in `requirements.txt` using pip:
```
pip install -r requirements.txt
```

2. Run the `check.py` script with the following command-line argument:
```
python3 check.py -l [URL_FILE]
```

- `-l` or `--list` (required): Path to the text file containing the list of URLs to check.

The script will navigate to each URL in the file and check if an alert or prompt is being displayed using Selenium. If an alert or prompt is detected, the URL will be saved to a file with the format `{domain}_xss.txt`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
