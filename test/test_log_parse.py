from datetime import datetime
from log_parse import log_parse
from unittest import mock
from io import BytesIO, TextIOWrapper
import argparse
import unittest

class TestLogParse(unittest.TestCase):

    # Log Entries Tests
    # -----------------
    def test_success_log_entries(self):
        lines = [
            '177.71.128.21 - - [10/Jul/2018:22:21:28 +0200] "GET /intranet-analytics/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (X11; U; Linux x86_64; fr-FR) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7"',
            '168.41.191.40 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.41 - - [11/Jul/2018:17:41:30 +0200] "GET /this/page/does/not/exist/ HTTP/1.1" 404 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"'
        ]
        log_entries = log_parse.LogEntries([log_parse.parse_log_line(line) for line in lines])

        self.assertIsInstance(log_entries, log_parse.LogEntries)
        self.assertEqual(len(log_entries.logs), len(lines))
        self.assertIsInstance(log_entries.logs[0], log_parse.LogEntry)

    def test_unique_ip_log_entries(self):
        lines = [
            '177.71.128.21 - - [10/Jul/2018:22:21:28 +0200] "GET /intranet-analytics/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (X11; U; Linux x86_64; fr-FR) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7"',
            '168.41.191.40 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.40 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.41 - - [11/Jul/2018:17:41:30 +0200] "GET /this/page/does/not/exist/ HTTP/1.1" 404 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.41 - - [11/Jul/2018:17:41:30 +0200] "GET /this/page/does/not/exist/ HTTP/1.1" 404 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"'
        ]
        expected_unique_ips = ['168.41.191.40', '168.41.191.41', '177.71.128.21']
        log_entries = log_parse.LogEntries([log_parse.parse_log_line(line) for line in lines])

        self.assertListEqual(log_entries.unique('ip'), expected_unique_ips)

    def test_empty_unique_ip_log_entries(self):
        log_entries = log_parse.LogEntries([])
        self.assertListEqual(log_entries.unique('ip'), [])

    def test_top_ip_log_entries(self):
        lines = [
            '177.71.128.21 - - [10/Jul/2018:22:21:28 +0200] "GET /intranet-analytics/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (X11; U; Linux x86_64; fr-FR) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7"',
            '177.71.128.21 - - [10/Jul/2018:22:21:28 +0200] "GET /intranet-analytics/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (X11; U; Linux x86_64; fr-FR) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7"',
            '168.41.191.40 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.31 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.02 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.40 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.41 - - [11/Jul/2018:17:41:30 +0200] "GET /this/page/does/not/exist/ HTTP/1.1" 404 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.41 - - [11/Jul/2018:17:41:30 +0200] "GET /this/page/does/not/exist/ HTTP/1.1" 404 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
            '168.41.191.41 - - [11/Jul/2018:17:41:30 +0200] "GET /this/page/does/not/exist/ HTTP/1.1" 404 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"'
        ]
        expected_top_ips = [
            {'ip': '168.41.191.41', 'count': 3},
            {'ip': '177.71.128.21', 'count': 2},
            {'ip': '168.41.191.40', 'count': 2}
        ]
        log_entries = log_parse.LogEntries([log_parse.parse_log_line(line) for line in lines])

        top_ips = log_entries.top('ip', 3)
        self.assertListEqual(top_ips, expected_top_ips)

        top_ips = log_entries.top('ip', 2)
        self.assertEqual(len(top_ips), 2)

        top_ips = log_entries.top('ip', 500)
        self.assertEqual(len(top_ips), 5)

    def test_empty_or_invalid_top_ip_log_entries(self):
        log_entries = log_parse.LogEntries([])
        self.assertRaisesRegex(ValueError, "Field 'ip' does not exist, or no log entries found.", log_entries.top, 'ip', 5)


    # Log Entry Tests
    # -----------------
    def test_success_parse_log_line(self):
        line = '50.112.00.11 - admin [11/Jul/2018:17:33:01 +0200] "GET /asset.css HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"'

        DATETIME_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

        ip = '50.112.00.11'
        user = 'admin'
        date = '11/Jul/2018:17:33:01 +0200'
        response = 200
        bytes = 3574
        method = 'GET'
        url = '/asset.css'
        protocol = 'HTTP/1.1'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'

        log_entry = log_parse.parse_log_line(line)

        self.assertIsInstance(log_entry, log_parse.LogEntry)
        self.assertEqual(log_entry.ip, ip)
        self.assertEqual(log_entry.user, user)
        self.assertEqual(log_entry.date.strftime(DATETIME_FORMAT), date)
        self.assertIsInstance(log_entry.date, datetime)
        self.assertEqual(log_entry.response, response)
        self.assertEqual(log_entry.bytes, bytes)
        self.assertEqual(log_entry.method, method)
        self.assertEqual(log_entry.url, url)
        self.assertEqual(log_entry.protocol, protocol)
        self.assertEqual(log_entry.user_agent, user_agent)

    def test_no_data_log_entry_exception(self):
        line = ''
        self.assertRaisesRegex(ValueError, 'The log entry did not contain any data.', log_parse.parse_log_line, line)

    def test_invalid_http_method_or_user_agent_log_entry_exception(self):
        line = '50.112.00.11 - admin [11/Jul/2018:17:33:01 +0200] "GET /asset.css HTTP/1.1" 200 3574 "-" no_user_agent'
        self.assertRaisesRegex(ValueError, 'Could not parse http_method or user_agent from log entry.', log_parse.parse_log_line, line)

    def test_invalid_http_method_fields_log_entry_exception(self):
        line = '50.112.00.11 - admin [11/Jul/2018:17:33:01 +0200] "GET HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"'
        self.assertRaisesRegex(ValueError, 'Could not parse method, url or protocol from http_method.', log_parse.parse_log_line, line)

    def test_invalid_date_log_entry_exception(self):
        line = '50.112.00.11 - admin 11/Jul/2018:17:33:01 +0200 "GET /asset.css HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"'
        self.assertRaisesRegex(ValueError, 'Could not parse date from log entry.', log_parse.parse_log_line, line)

    def test_invalid_remaining_fields_log_entry_exception(self):
        line = '[11/Jul/2018:17:33:01 +0200] "GET /asset.css HTTP/1.1" "-" "Mozilla/5.0"'
        self.assertRaisesRegex(ValueError, 'Could not parse ip, user, response or bytes from log entry.', log_parse.parse_log_line, line)
    

    # Argparse Tests
    # -----------------
    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(log_file=TextIOWrapper(BytesIO(), encoding='UTF8'), verbose=None))
    def test_default_get_args(self, *args):
        args = log_parse.get_args(['--log-file', 'file.log'])
        self.assertIsInstance(args.log_file, TextIOWrapper)
        self.assertEqual(args.verbose, None)

    @mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(log_file=TextIOWrapper(BytesIO(), encoding='UTF8'), verbose=True))
    def test_verbose_get_args(self, *args):
        args = log_parse.get_args(['--log-file', 'file.log'])
        self.assertIsInstance(args.log_file, TextIOWrapper)
        self.assertEqual(args.verbose, True)

    def test_invalid_get_args(self):
        with self.assertRaises(SystemExit) as exit_system:
            log_parse.get_args(None)
        self.assertEqual(exit_system.exception.code, 2)