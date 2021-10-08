from datetime import datetime
from dataclasses import dataclass
from typing import List
import re
import logging
import argparse
import sys

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
    
    logging.info(f"\n{line}")
    
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

def get_args(args: List[str]):
    """
    Get the arguments passed into our script
    """

    parser = argparse.ArgumentParser(description="Parse HTTP log requests and return a summary of the data")
    parser.add_argument("--log-file", required=True, type=argparse.FileType('r', encoding='UTF-8'), help="The file path of the file to parse.")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose logging to console.")


    return parser.parse_args(args)

def main():
    """
    Execute the log parser
    """

    args = get_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig( level=logging.INFO )

    try:
        log_entries = LogEntries([parse_log_line(line) for line in args.log_file.readlines()])
        print(f"{[i.date.strftime('%D') for i in log_entries.logs]}")
    
    except ValueError as error:
        print('Failed to parse the log file.\n')
        print(error)

    finally:
        args.log_file.close()

if __name__ == "__main__":
    main()
