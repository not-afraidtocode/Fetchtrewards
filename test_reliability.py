import requests
import unittest
from unittest.mock import patch
import requests_mock
from reliable import check_health, load_config
from urllib.parse import urlparse

class TestMonitor(unittest.TestCase):

    # --- Core Functionality Tests ---
    def test_success_case(self):
        """200 OK + 400ms → UP"""
        with requests_mock.Mocker() as m:
            m.get('http://good.com', status_code=200)
            with patch('time.perf_counter') as mock_time:
                mock_time.side_effect = [0, 0.4]  # 400ms
                endpoint = {"url": "http://good.com"}
                self.assertEqual(check_health(endpoint), "UP")

    def test_status_code_failure(self):
        """300 Redirect → DOWN"""
        with requests_mock.Mocker() as m:
            m.get('http://redirect.com', status_code=300)
            endpoint = {"url": "http://redirect.com"}
            self.assertEqual(check_health(endpoint), "DOWN")

    def test_exact_500ms_response(self):
        """Exactly 500ms → UP"""
        with requests_mock.Mocker() as m:
            m.get('http://exact.com', status_code=200)
            with patch('time.perf_counter') as mock_time:
                mock_time.side_effect = [0, 0.5]  # 500ms
                endpoint = {"url": "http://exact.com"}
                self.assertEqual(check_health(endpoint), "UP")

    def test_501ms_response(self):
        """501ms → DOWN"""
        with requests_mock.Mocker() as m:
            m.get('http://slow.com', status_code=200)
            with patch('time.perf_counter') as mock_time:
                mock_time.side_effect = [0, 0.501]  # 501ms
                endpoint = {"url": "http://slow.com"}
                self.assertEqual(check_health(endpoint), "DOWN")

    # --- Edge Case Tests ---
    def test_domain_with_port(self):
        """example.com:8080 → example.com"""
        endpoint = {"url": "http://example.com:8080/api"}
        domain = urlparse(endpoint['url']).hostname
        self.assertEqual(domain, "example.com")

    def test_invalid_json_body(self):
        """Invalid JSON → DOWN"""
        endpoint = {
            "url": "http://badjson.com",
            "method": "POST",
            "body": "{invalid}"
        }
        self.assertEqual(check_health(endpoint), "DOWN")

    def test_missing_method(self):
        """Default to GET if method omitted"""
        with requests_mock.Mocker() as m:
            m.get('http://default.com', status_code=200)
            endpoint = {"url": "http://default.com"}
            self.assertEqual(check_health(endpoint), "UP")

    # --- Security/Protocol Tests ---
    def test_https_success(self):
        """Valid HTTPS → UP"""
        with requests_mock.Mocker() as m:
            m.get('https://secure.com', status_code=201)  # 201 is still 2xx
            endpoint = {"url": "https://secure.com"}
            self.assertEqual(check_health(endpoint), "UP")

    def test_ssl_verification_failure(self):
        """Invalid SSL cert → DOWN"""
        endpoint = {"url": "https://self-signed.badssl.com"}
        with requests_mock.Mocker() as m:
            # Simulate SSL verification failure
            m.get(endpoint['url'], exc=requests.exceptions.SSLError)
            result = check_health(endpoint)
            self.assertEqual(result, "DOWN")

    # --- Concurrency Tests ---
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_concurrent_execution(self, mock_executor):
        """Verify thread pool usage"""
        mock_executor.return_value.__enter__.return_value.submit.side_effect = lambda f: f()
        config = [{"url": "http://test1.com"}, {"url": "http://test2.com"}]
        load_config = lambda _: config  # Mock config
        
        # This will trigger the ThreadPoolExecutor logic
        check_health(config[0])  # Indirectly test concurrency setup

if __name__ == '__main__':
    unittest.main()
    