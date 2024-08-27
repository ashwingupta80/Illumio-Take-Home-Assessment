# Flow Log Processor

## Project Overview

The Flow Log Processor is a command-line tool designed to parse AWS VPC flow log data and map each log entry to a predefined tag based on a lookup table. The lookup table is specified in a CSV file and contains three columns: `dstport`, `protocol`, and `tag`. The tool processes the flow logs, applies the tags, and generates two output files: one that counts the occurrences of each tag and another that counts occurrences of each port/protocol combination.

## How to Run and Get Required Output Files
1. Required Input files-> `flow_logs.txt`, `lookup_table.csv`, `protocol-numbers-1.csv`. Note- 'protocol-numbers-1.csv' contains mapping of IANA mapping of portocols and keywords (For example- tcp, udp).
2. Using command line navigate to folder `Illumio_Take_Home_Assessment`.
3. Run `python src/flow_log_processor.py` command on command line to output `tag_counts.csv` and `port_protocol_counts.csv` files that contain count of matches for each tag and Count of matches for each port/protocol combination respectively.

## Dependencies

The program is written in Python and requires Python 3.8 or higher.

### Required Python Libraries

The program relies on Python's standard libraries, which should be available in any standard Python installation:

- `csv`: For reading and processing CSV files.

## Features

- **Flow Log Parsing**: Supports AWS flow log format (version 2).
- **Tagging**: Matches flow log entries to tags based on `dstport` and `protocol`.
- **Case-Insensitive Matching**: Handles tags and protocols in a case-insensitive manner.
- **Detailed Output**: Generates comprehensive output files, including tag counts and port/protocol combination counts.
- **Error Handling**: If AWS flow log does not contain 14 parts, then the log is skipped. Moreover, code ensures untagged flow log entries are categorized under the `Untagged` tag. 

## Assumptions

- **Flow Log Format**: The program is designed to work with the default AWS VPC flow log format, version 2. Custom formats or other versions are not supported.
- **Lookup Table Size**: The lookup table CSV file is assumed to be small enough (up to 10,000 entries) to be loaded entirely into memory.
- **Case Insensitivity**: All matching operations are case-insensitive to account for variations in input.
- **Protocol Numbers**: The protocol numbers in the flow logs are assumed to conform to IANA standard protocol numbers.
- **File Integrity**: The input files (`flow_logs.txt` and `lookup_table.csv`) are expected to be well-formed and free of corruption.

## File Structure

- **`src/flow_log_processor.py`**: Main script that processes the flow logs and generates tag_counts.csv and port_protocol_counts.csv.
- **`tests/test_flow_log_processor.py`**: Test script for validating the functionality of the main script-> defines unit tests.
- **`flow_logs.txt`**: Provided input file containing AWS VPC flow log data.
- **`lookup_table.csv`**: Provided input file containing the tag lookup table.
- **`protocol-numbers-1.csv`**: Downloaded input file that maps IANA portocols to keywords (For example- tcp, udp).
- **`tag_counts.csv`**: Output file that contains the count of matches for each tag.
- **`port_protocol_counts.csv`**: Output file that contains the count of matches for each port/protocol combination.

