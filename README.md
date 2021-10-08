# azenix-challenge

## Getting Started

### Prerequisites
- Python3

### Execution
To run the log parser you need to pass in a filepath to the log file via the `--file-path` argument. This should be a valid log file that matches the expected layout of the logs being parsed.

```bash
python .\log_parse\log_parse.py --log-file 'sample-data.log' 
```

### Logging
If you need to debug a why parsing fails for a file, you can add the `--verbose` flag to the exection to output the line that is being parsed to troubleshoot.

```bash
python .\log_parse\log_parse.py --log-file 'sample-data.log' --verbose
```

### Tests
To execute the tests you can run the below:

```bash
python -m unittest discover
```

#### Code Coverage
To check code coverage, run the below and open the `htmlcov\index.html` file.

```bash
pip install coverage
coverage run -m unittest discover
coverage html
```

## Challenge Details
### Requirements
The task is to parse a log file containing HTTP requests and to report on its contents.

For a given log file we want to know:
- The number of unique IP addresses
- The top 3 most visited URLs
- The top 3 most active IP addresses

### Deliverables
- For this task you can choose from Java, Python, JavaScript, Kotlin, Go, or C#.
- There are no restrictions on language features and you are free to use third-party libraries.
- Please include tests that demonstrate your solution is working.
- You can submit your solution as a zip file containing the source code or a public git repository.

### Sample Data
[Sample Log](sample-data.log)
