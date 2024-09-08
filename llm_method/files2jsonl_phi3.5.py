import os
import json
from tqdm import tqdm


def process_files(tables_folder, metadata_folder):
    output_lines = []
    files = [f for f in os.listdir(tables_folder) if f.endswith("_table.html")]

    for filename in tqdm(files, desc="Processing files"):
        if filename.endswith("_table.html"):
            table_id = filename.split("_")[0]
            html_file = os.path.join(tables_folder, filename)
            metadata_file = os.path.join(metadata_folder, f"{table_id}_metadata.json")

            if os.path.exists(metadata_file):
                with open(html_file, "r", encoding='utf-8') as f:
                    html_content = f.read()
                with open(metadata_file, "r", encoding='utf-8') as f:
                    metadata_content = json.load(f)

                system_prompt = "You are an AI assistant specialized in converting HTML tables to JSON format. \n "
                # Create the conversations list
                conversations = [
                    {'from': 'human', 'value': system_prompt + html_content},
                    {'from': 'gpt', 'value': json.dumps(metadata_content)}
                ]

                # Create the text string
                text = f"<s><|user|> {system_prompt} {html_content} <|end|> <|assistant|> {json.dumps(metadata_content)} <|end|>"

                # Create the output dictionary
                output_dict = {
                    "conversations": conversations,
                    "text": text
                }

                # Serialize the entire dictionary to JSON
                json_line = json.dumps(output_dict, ensure_ascii=False)
                output_lines.append(json_line)

    # Write all lines to the output file
    with open("output_phi35.jsonl", "w", encoding='utf-8') as f:
        for line in output_lines:
            f.write(line + "\n")


# Usage example
tables_folder = "./dataset/generated_tables/tables/"
metadata_folder = "./dataset/generated_tables/metadata/"
process_files(tables_folder, metadata_folder)