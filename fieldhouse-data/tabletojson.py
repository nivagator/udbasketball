import json
from bs4 import BeautifulSoup
import os
import glob

def sanitize_row(row_dict):
    """
    - Removes '*' from all values.
    - Replaces any value 'NA' with an empty string ''.
    """
    sanitized = {}
    for k, v in row_dict.items():
        val = v.replace('*', '').strip()
        if val == "NA":
            val = ""
        sanitized[k] = val
    return sanitized

def extract_tables_from_file(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        contents = f.read()
    soup = BeautifulSoup(contents, "html.parser")
    tables = soup.find_all('table', {'class': 'rgMasterTable'})
    all_rows = []
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = [td.get_text(strip=True) for td in row.find_all('td')]
            if cells:
                row_dict = dict(zip(headers, cells))
                sanitized = sanitize_row(row_dict)
                all_rows.append(sanitized)
    return all_rows

def strip_suffixes(name):
    if name.endswith('-standings'):
        return name[:-10]
    elif name.endswith('-schedule'):
        return name[:-9]
    return name

def process_files(pattern, output_filename):
    files = glob.glob(pattern)
    if not files:
        print(f"No files found for pattern: {pattern}")
        return

    output_obj = {}
    for input_file in files:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        stripped_name = strip_suffixes(base_name)
        rows = extract_tables_from_file(input_file)
        output_obj[stripped_name] = rows
        print(f"Processed {input_file}: {len(rows)} row(s) extracted.")

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(output_obj, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {output_filename} with {len(output_obj)} entries.")

def main():
    process_files("*-standings.html", "standings.json")
    process_files("*-schedule.html", "schedule.json")

if __name__ == "__main__":
    main()
