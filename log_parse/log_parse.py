from datetime import datetime
from dataclasses import dataclass
from typing import List
import re
import logging

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

    if len(line) <= 1:
        raise ValueError('The log entry did not contain any data.')
    
    logging.info(f"\nParsing:\n{line}")
    
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

    # Get the date field (everything between [])
    hard_bracket_content_regex = '\[(.+)\]'
    hard_bracket_content_regex_result = re.search(hard_bracket_content_regex, line)
    if not hard_bracket_content_regex_result or len(hard_bracket_content_regex_result.groups()) != 1:
        raise ValueError('Could not parse date from log entry.')
    date_str = hard_bracket_content_regex_result.group(1)
    date = datetime.strptime(date_str, "%d/%b/%Y:%H:%M:%S %z")

    # Get remaining fields
    remaining_fields = line.split(' ')
    if len(remaining_fields) < 10:
        raise ValueError('Could not parse ip, user, response or bytes from log entry.')
    ip, _, user, _, _, _, _, _, response, bytes, *_ = remaining_fields
    response = int(response)
    bytes = int(bytes)

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
        print(f"{[i.ip for i in log_entries.logs]}")
    
    except ValueError as error:
        print('Failed to parse the log file.\n')
        print(error)

    pass

if __name__ == "__main__":
    main()
