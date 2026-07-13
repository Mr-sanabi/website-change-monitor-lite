import requests


def fetch_page(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        response.raise_for_status()

        return {
            "url": url,
            "status_code": response.status_code,
            "html": response.text,
            "error": "",
            "error_type": None
        }

    except requests.exceptions.HTTPError as error:
        return {
            "url": url,
            "status_code": error.response.status_code,
            "html": None,
            "error": str(error),
            "error_type": "http_error"
        }
    except requests.exceptions.RequestException as error:
        return {
            "url": url,
            "status_code": None,
            "html": None,
            "error": str(error),
            "error_type": "request_error"
        }