# Step 4: Merge JSON Files
"""
Once you've saved individual JSON files from each pagination link, you will want to
run this function to merge the files and save them again as a nested JSON structure.
"""

# import libraries
import json

def merge_json_files(file_paths, output_file):
    """
    Reads in a list of file paths to JSON files created in Step3_parse_html_docs.py;
    returns a merged, nested JSON string.
    """
    merged_data = []
    for path in file_paths:
        with open(path, 'r') as file:
            data = json.load(file)
            merged_data.append(data)
    with open(output_file, 'w') as outfile:
        json.dump(merged_data, outfile)