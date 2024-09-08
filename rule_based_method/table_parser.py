from bs4 import BeautifulSoup
import re


def parse_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    result = {
        "header": {},
        "body": {"headers": {"col": [], "row": []}, "content": []},
        "footer": {}
    }

    # Parse header
    caption = table.find('caption')
    if caption:
        match = re.search(r'Table ([\d.]+) (.+)', caption.text)
        if match:
            result["header"]["table_id"] = match.group(1)
            result["header"]["text"] = caption.text.strip()

    # Parse body
    rows = table.find_all('tr')
    data_rows = []
    for i, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])
        if i == 0:  # First row is column headers
            result["body"]["headers"]["row"] = [cell.text.strip() for cell in cells[1:]]
        elif all(cell.name == 'th' for cell in cells):  # This is a header row
            result["body"]["headers"]["row"].extend([cell.text.strip() for cell in cells])
        else:  # This is a data row
            data_rows.append(cells)

    # Process data rows
    for row in data_rows:
        if not any(re.search(r'Creation:|modified:', cell.text) for cell in row):
            result["body"]["headers"]["col"].append(row[0].text.strip())
            result["body"]["content"].extend([cell.text.strip() for cell in row[1:]])

    # Parse footer
    footer_text = []
    for row in reversed(rows):
        row_text = ' '.join(cell.text.strip() for cell in row.find_all(['th', 'td']))
        if re.search(r'Creation:|modified:', row_text):
            footer_text.insert(0, row_text)

    if footer_text:
        footer_text = '\n'.join(footer_text)
        creation_match = re.search(r'Creation: (\d+\w+\d+)', footer_text)
        if creation_match:
            result["footer"]["table_creation_date:"] = creation_match.group(1)
            result["footer"]["text"] = footer_text

    # Capture additional row headers
    all_cells = [cell.text.strip() for row in rows for cell in row.find_all(['th', 'td'])]
    existing_items = set(
        result["body"]["headers"]["row"] + result["body"]["headers"]["col"] + result["body"]["content"])
    additional_headers = [cell for cell in all_cells if
                          cell and cell not in existing_items and not re.search(r'Creation:|modified:', cell)]
    result["body"]["headers"]["row"].extend(additional_headers)

    return result