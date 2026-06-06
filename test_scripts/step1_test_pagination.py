## This is a script you can run to test Step 1: Get Pagination Links

"""
This script will:
1) Read in the first pagination link for a sample Ao3 fandom (i.e. the first page of search results for the sample fandom's Ao3 tag),
2) Scrape the test pagination link,
3) Return a list of pagination links for the entire fandom (i.e. links to every page of search results for the sample fandom)

The sample fandom selected, "Candela Obscura (Critical Role Web Series)", has a little over 200 works as of 6/5/2026.
Running this script with a larger Ao3 fandom (think 1000+ works) should not cause RAM / memory usage issues, but
be aware that you may encounter memory usage issues in downstream scripts.

"""

# import libraries
from bs4 import BeautifulSoup
import requests
import re

# import functions
from src.Step1_get_pagination_links import (get_html_doc,
                                            get_all_urls,
                                            get_urls_only,
                                            get_all_ol,
                                            get_pagination_links,
                                            update_pagination_links_list,
                                            save_links_to_txt
)

# Set test url (note you can sub in a link to a different fandom page if desired)
test_url = 'https://archiveofourown.org/tags/Candela%20Obscura%20(Critical%20Role%20Web%20Series)/works?page=1'

# get BeautifulSoup object
soup = get_html_doc(test_url)

# from BeautifulSoup object, get all_urls
all_urls = get_all_urls(soup)

# update all_urls to only include href links
all_urls_updated = get_urls_only(all_urls)

# from BeautifulSoup object, get all_ol
all_ol = get_all_ol(soup)

# get list of pagination links
pagination_links = get_pagination_links(all_ol)
links_to_scrape = update_pagination_links_list(pagination_links)
print("There are: ", str(len(links_to_scrape)), " pagination links to scrape for the Candela Obscura fandom.")

# save pagination links to txt file
file_path = "../data/txt_files/pagination_links.txt"
save_links_to_txt(file_path, links_to_scrape)