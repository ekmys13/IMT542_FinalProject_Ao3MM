## This is a script you can run to test Step 4: Merge JSON Files
"""
This test will take a list JSON files created from fandom pagination links and merge them
into a new nested JSON structure.
"""

## import libraries
import json

## import scripts
from src.Step4_merge_json_files import merge_json_files
from src.Step3_parse_html_docs import (convert_to_json, save_json_to_file)

## Merge JSON files

# get list of file paths for pagination link JSON files
filepaths_list = [
    '../data/json_files/json_tests/candela_test_jsons/candela_page1.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page2.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page3.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page4.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page5.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page7.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page8.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page9.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page10.json',
    '../data/json_files/json_tests/candela_test_jsons/candela_page11.json'
]

# create empty JSON file to initiate merge
output_dict = {}
output_file = convert_to_json(output_dict)
output_filepath = '../data/json_files/json_tests/candela_test_jsons/all_candela_test.json'
with open(output_filepath, 'w') as f:
    f.write(output_file)

# merge JSON files into new empty JSON file
merge_json_files(filepaths_list, output_filepath)
print(f"Merged data written to '{output_file}'")