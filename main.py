import os
import json
import re
from rule_based_method.table_parser import parse_table


def process_tables(base_directory):
    tables_dir = os.path.join(base_directory, 'train', 'tables')
    metadata_dir = os.path.join(base_directory, 'train', 'metadata')

    # Ensure the metadata directory exists
    os.makedirs(metadata_dir, exist_ok=True)

    for filename in os.listdir(tables_dir):
        if filename.endswith(".html"):
            input_path = os.path.join(tables_dir, filename)

            # Extract the number from the filename
            match = re.search(r'(\d+)_table\.html', filename)
            if match:
                number = match.group(1)
                output_filename = f"{number}_metadata_pred.json"
                output_path = os.path.join(metadata_dir, output_filename)

                with open(input_path, 'r') as file:
                    table_content = file.read()

                parsed_data = parse_table(table_content)

                # Save the parsed data as JSON
                with open(output_path, 'w') as outfile:
                    json.dump(parsed_data, outfile, indent=4)

                print(f"Processed {filename} -> {output_filename}")
            else:
                print(f"Skipped {filename} - doesn't match expected naming pattern")


# Usage
base_directory = r"C:\Users\Avi\PycharmProjects\interview\beaconcure\dataset"
process_tables(base_directory)