from datetime import datetime
from dataclasses import dataclass
from typing import List
import re

@dataclass
class LogEntry:
    ip: str
    user: str
    date: datetime
    response: int
    bytes: int
    method: str
    url: str
    protocol: str
    user_agent: str

@dataclass
class LogEntries:
    logs: List[LogEntry]

    # TODO: func to get unique items

    # TODO: func to get top items

def parse_log_line(line: str) -> LogEntry:
    """
    Parse a line of a log file based on a specific format.

    :param line: A line of text from the log file 
    :type line: str
    :return: A single LogEntry
    :rtype: LogEntry
    """
    
    # Get all fields between quotation marks
    quoted_content_regex = '"([^"]*)"'
    quoted_content_regex_result = re.findall(quoted_content_regex, line)
    if len(quoted_content_regex_result) != 3:
        raise ValueError('Could not parse http_method or user_agent from log entry.')
    http_method, _, user_agent  = quoted_content_regex_result

    # Separate out http_method into method, url, protocol
    http_method_fields = http_method.split(' ')
    if len(http_method_fields) != 3:
        raise ValueError('Could not parse method, url or protocol from http_method.')
    method, url, protocol = http_method_fields

    # TODO: Parse line into separate fields

    ip = '50.112.00.11'
    user = 'admin'
    date = '11/Jul/2018:17:33:01 +0200'
    response = 200
    bytes = 3574
    # method = 'GET'
    # url = '/asset.css'
    # protocol = 'HTTP/1.1'
    # user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'


    return LogEntry(ip, user, date, response, bytes, method, url, protocol, user_agent)

def main():
    """
    Execute the log parser
    """

    lines = [
        '177.71.128.21 - - [10/Jul/2018:22:21:28 +0200] "GET /intranet-analytics/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (X11; U; Linux x86_64; fr-FR) AppleWebKit/534.7 (KHTML, like Gecko) Epiphany/2.30.6 Safari/534.7"',
        '168.41.191.40 - - [09/Jul/2018:10:11:30 +0200] "GET http://example.net/faq/ HTTP/1.1" 200 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"',
        '168.41.191.41 - - [11/Jul/2018:17:41:30 +0200] "GET /this/page/does/not/exist/ HTTP/1.1" 404 3574 "-" "Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC Vision Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"'
    ]

    try:

        log_entries = LogEntries([parse_log_line(line) for line in lines])
        print(f"{[i.user_agent for i in log_entries.logs]}")
    
    except ValueError as error:
        print('Failed to parse the log file.\n')
        print(error)

    pass

if __name__ == "__main__":
    main()
