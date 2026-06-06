## This is a script you can run to test Step 2: Get Fanwork Links

"""
This script will:
1) Read in a list of pagination links from the file 'pagination_links.txt',
2) Select a test pagination link from the list,
3) Scrape the test pagination link and return a list of fanwork links for that page of search results.

Note that if you want to get the full list of fanworks for any given fandom, you will want to
run this script for each pagination link / page of search results for your fandom's Ao3 tag.

Particularly if you are getting fanwork links for an Ao3 fandom with 500+ works,
I strongly recommend scraping pagination links one at a time to avoid RAM usage issues.

Further development is needed to reduce the memory load of the scraping / fanwork link compiling process --
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

# import functions
from src.Step2_get_fanwork_links import(get_links_to_scrape,
                                        get_html_doc_pagination,
                                        get_all_links,
                                        get_urls_only,
                                        get_work_links,
                                        pare_down_work_links,
                                        remove_chapter_links,
                                        save_links_to_txt
)

# get_links_to_scrape
links_to_scrape = get_links_to_scrape('../data/pagination_links.txt')

# test test_link
test_link = links_to_scrape[0]

# get BeautifulSoup object
soup = get_html_doc_pagination(test_link)

# get work links
all_links = get_all_links(soup)
urls_only = get_urls_only(all_links)
work_links = get_work_links(urls_only)
work_links_pared = pare_down_work_links(work_links)

# remove chapter links
work_links_nochap = remove_chapter_links(work_links_pared)

# save fanwork links to .txt file
filepath = '../data/txt_files/step2_test.txt'
save_links_to_txt(filepath, work_links_nochap)