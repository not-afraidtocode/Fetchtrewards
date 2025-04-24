import yaml
import requests
import time
import json
import concurrent.futures
from urllib.parse import urlparse
from collections import defaultdict
import sys

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')
    parsed_url = urlparse(url)
    
    json_body = None
    if body:
        try:
            json_body = json.loads(body)
        except json.JSONDecodeError:
            return "DOWN"

    try:
        start = time.perf_counter()
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json_body,
            timeout=(0.2, 0.3)  
        )
        response_time = (time.perf_counter() - start) * 1000

        if (200 <= response.status_code < 300 and 
            response_time <= 500):
            return "UP"
        return "DOWN"
    except (requests.RequestException, requests.Timeout):
        return "DOWN"
        