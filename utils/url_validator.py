import re
import requests

def is_valid_url_format(url):
    # Basic regex for URL validation
    regex = re.compile(
        r'^(https?:\/\/)?'           # http:// or https://
        r'([a-zA-Z0-9\-_]+\.)+'      # domain
        r'[a-zA-Z]{2,}'              # top-level domain
        r'(\/[^\s]*)?$'              # optional path
    )
    return re.match(regex, url) is not None

def is_accessible_url(url):
    try:
        # Normalize the URL
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code in [200, 301, 302]
    except requests.RequestException:
        return False

def validate_url(url):
    if not is_valid_url_format(url):
        return False, "URL format is invalid."
    if not is_accessible_url(url):
        return False, "URL is not accessible or doesn't respond."
    return True, "URL is valid and accessible."
