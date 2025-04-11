import re
import requests

def validate_url(url):
    pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// or https://
        r'([a-zA-Z0-9.-]+)\.'  # domain name
        r'([a-zA-Z]{2,})'  # domain extension
        r'(\/\S*)?$'  # path
    )
    if not pattern.match(url):
        return False
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except:
        return False
