from log_parse import log_parse
import unittest

class TestLogParse(unittest.TestCase):
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

    def test_success_parse_log_line(self):
        line = '50.112.00.11 - admin [11/Jul/2018:17:33:01 +0200] "GET /asset.css HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6"'

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
        self.assertEqual(log_entry.date, date)
        self.assertEqual(log_entry.response, response)
        self.assertEqual(log_entry.bytes, bytes)
        self.assertEqual(log_entry.method, method)
        self.assertEqual(log_entry.url, url)
        self.assertEqual(log_entry.protocol, protocol)
        self.assertEqual(log_entry.user_agent, user_agent)
    