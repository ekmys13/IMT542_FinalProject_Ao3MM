## This is a script you can run to test Step 3: Get Fanwork Links
"""
This script will run three tests.

The first two tests scrape metadata and create a JSON array for individual fanwork links,
one link that contains adult content (i.e. is rated "Mature" or "Explicit") and one that does not (i.e.
is rated "Not Rated," "General Audiences, or "Teen And Up Audiences".

The third test scrapes metadata and creates a nested JSON array for the first 10 fanwork links in
the text file: "fanwork_links.txt".

You can run additional tests with more than 10 links at a time; I don't recommend testing with more than 20 links
at a time, as this can cause memory / RAM usage issues depending on your device.

To build the sample visualizations you can see in the "assets" folder, I ran Step3_parse_html_docs.py
on each of the 11 pagination links for the Candela Obscura fandom one at a time, then merged the resulting JSON arrays
into one array.

Further development is needed to reduce the memory load of the fanwork scraping / metadata compiling process --
until that point, scrape in high volumes at your own risk.

"""

# import libraries
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re
import json

# import scripts
from src.Step3_parse_html_docs import(get_fanwork_links,
                                      get_fanwork_html,
                                      get_soup,
                                      detect_adult_content_warning,
                                      get_rating_adult,
                                      get_warnings_adult,
                                      get_category_adult,
                                      get_language_adult,
                                      get_fandom_adult,
                                      get_relationships_adult,
                                      get_characters_adult,
                                      get_additional_adult,
                                      get_date_published_adult,
                                      get_date_updated_adult,
                                      get_comment_count_adult,
                                      get_bookmarks_count_adult,
                                      get_hits_count_adult,
                                      get_rating_nonadult,
                                      get_warnings_nonadult,
                                      get_category_nonadult,
                                      get_language_nonadult,
                                      get_fandom_nonadult,
                                      get_relationships_nonadult,
                                      get_characters_nonadult,
                                      get_additional_nonadult,
                                      get_date_published_nonadult,
                                      get_date_updated_nonadult,
                                      get_comment_count_nonadult,
                                      get_bookmarks_count_nonadult,
                                      get_hits_count_nonadult,
                                      get_word_count,
                                      get_chapter_count,
                                      get_kudos_count,
                                      create_fanwork_dict_adult,
                                      create_fanwork_dict_nonadult,
                                      create_all_works_dict,
                                      append_all_works_dict,
                                      convert_to_json,
                                      save_json_to_file)

## Get fanwork links
fanwork_links = get_fanwork_links('../data/fanwork_links.txt')

## Test Individual Fanwork Links
# Test Link 1 (has adult content)
test_url1 = 'https://archiveofourown.org/works/73925776'
outer_html1 = get_fanwork_html(test_url1)
soup1 = get_soup(outer_html1)
test_fanwork_dict1 = create_fanwork_dict_adult(soup1)
all_works1 = create_all_works_dict()
append_all_works_dict(test_fanwork_dict1, all_works1)
test_fanwork_json1 = convert_to_json(all_works1)
filepath1 = '../data/json_files/json_tests/single_fanwork_link_test1.json'
save_json_to_file(filepath1, test_fanwork_json1)

# Test Link 2 (does not have adult content)
test_url2 = 'https://archiveofourown.org/works/51518734'
outer_html2 = get_fanwork_html(test_url2)
soup2 = get_soup(outer_html2)
test_fanwork_dict2 = create_fanwork_dict_nonadult(soup2)
all_works2 = create_all_works_dict()
append_all_works_dict(test_fanwork_dict2, all_works2)
test_fanwork_json2 = convert_to_json(all_works2)
filepath2 = '../data/json_files/json_tests/single_fanwork_link_test2.json'
save_json_to_file(filepath2, test_fanwork_json2)

## Test First 10 Fanwork Links

first_10_fanworks = fanwork_links[0:10]
total_fanworks = len(first_10_fanworks)
test_first10works_dict = create_all_works_dict()

for i in range(len(first_10_fanworks)):
    print("Current fanwork link: ", str(i+1), "of", str(total_fanworks))

    current_work_html = get_fanwork_html(first_10_fanworks[i])
    print("Successfully created outer html for link: ", str(i+1), " of ", str(total_fanworks))

    soup = get_soup(current_work_html)
    print("Successfully created soup for link: ", str(i+1), " of ", str(total_fanworks))

    adult_content_present = detect_adult_content_warning(soup)
    print("Adult content is present: ", str(adult_content_present))

    if adult_content_present:
        current_work_dict = create_fanwork_dict_adult(soup)
    else:
        current_work_dict = create_fanwork_dict_nonadult(soup)
    print("Successfully created dictionary for link: ", str(i+1), " of ", str(total_fanworks))

    append_all_works_dict(current_work_dict, test_first10works_dict)
    print("Successfully appended dictionary to test_first10works_dict for link: ", str(i+1), " of ", str(total_fanworks))

# convert to json and save to file
test_first10works_json = convert_to_json(test_first10works_dict)
filepath3 = '../data/json_files/json_tests/first10works_test.json'
save_json_to_file(filepath3, test_first10works_json)