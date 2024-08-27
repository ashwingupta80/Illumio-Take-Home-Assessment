import csv

def parse_protocol_mapping(file_path):
    """
    Parses the protocol mapping CSV file and returns a dictionary mapping protocol numbers to protocol names.

    Args:
        file_path (str): Path to the protocol mapping CSV file.

    Returns:
        dict: A dictionary with protocol numbers as keys and protocol names as values.
    """
    protocol_mapping = {}
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            protocol_number = int(row['Decimal'])
            protocol_name = row['Keyword'].strip().lower()
            protocol_mapping[protocol_number] = protocol_name
    return protocol_mapping

def parse_lookup_table(file_path):
    """
    Parses the lookup table CSV file and returns a dictionary for port-protocol-tag mapping.

    Args:
        file_path (str): Path to the lookup table CSV file.

    Returns:
        dict: A dictionary with (dstport, protocol) as keys and tags as values.
    """
    lookup_table = {}
    
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            dstport, protocol, tag = line.strip().split(',')
            key = (int(dstport), protocol.lower())
            lookup_table[key] = tag.lower()
    return lookup_table

def process_flow_logs(log_file, lookup_table, protocol_mapping):
    """Processes the flow logs, mapping each log entry to a tag and counting occurrences."""
    tag_counts = {}
    port_protocol_counts = {}

    with open(log_file, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 14:
                continue  # Skip lines that don't have enough parts

            dstport = int(parts[6])
            protocol_number = int(parts[7])
            protocol_name = protocol_mapping.get(protocol_number, '').lower()
            
            key = (dstport, protocol_name)
            tag = lookup_table.get(key, 'untagged')

            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            port_protocol_counts[key] = port_protocol_counts.get(key, 0) + 1

    return tag_counts, port_protocol_counts

def generate_output(tag_counts, port_protocol_counts):
    """
    Generates output CSV files for tag counts and port-protocol combination counts.

    Args:
        tag_counts (dict): Dictionary with tags as keys and their counts as values.
        port_protocol_counts (dict): Dictionary with (port, protocol) as keys and their counts as values.
    """
    with open('tag_counts.csv', 'w') as file:
        file.write('Tag,Count\n')
        for tag, count in tag_counts.items():
            file.write(f'{tag},{count}\n')
    
    with open('port_protocol_counts.csv', 'w') as file:
        file.write('Port,Protocol,Count\n')
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f'{port},{protocol},{count}\n')

if __name__ == '__main__':
    # Generate Mapping for all protocols. 
    # Referred documentation to get csv-> https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
    protocol_mapping = parse_protocol_mapping('protocol-numbers-1.csv')

    # Generate a lookup table (dstport,protocol,tag) to handle new protocols.
    lookup_table = parse_lookup_table('lookup_table.csv')
    
    # Generate Tag Counts and Port/Protocol Combination Counts.
    tag_counts, port_protocol_counts = process_flow_logs('flow_logs.txt', lookup_table, protocol_mapping)
    
    # Generates output CSV files for tag counts and port-protocol combination counts.
    generate_output(tag_counts, port_protocol_counts)