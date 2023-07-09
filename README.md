```markdown
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
python3 crawly.py --url [URL] --threads [NUM_THREADS] [--gen] [--num-payloads [NUM_PAYLOADS]]
```

- `--url` (required): URL of the website to test.
- `--threads` (optional, default=10): Number of threads to use for testing.
- `--gen` (optional): Generate XSS payloads instead of loading from `payloads.txt`.
- `--num-payloads` (optional, default=1000): Number of XSS payloads to generate when using `--gen` flag.

## Examples

Test a website with default settings:
```
python3 crawly.py --url https://example.com
```

Test a website with generative mode and custom number of payloads:
```
python3 crawly.py --url https://example.com --gen --num-payloads 2000
```

## Requirements

- Python 3.7+
- Requests library
- Beautiful Soup library

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

Please note that the content provided here is raw markdown text. Make sure to save it as `readme.md` in your project directory.

Let me know if you have any further questions or need any more assistance!