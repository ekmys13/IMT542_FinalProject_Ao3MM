## Step 2: Get Fanwork Links

# import libraries
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re

def get_links_to_scrape(filepath):
    """Takes in a txt file of pagination links and returns a list of fanwork links."""
    links_to_scrape = open(filepath).readlines()
    return links_to_scrape

def get_html_doc_pagination(url):
    """Takes in a pagination link from get_links_to_scrape and returns a BeautifulSoup object."""
    driver = webdriver.Firefox()
    driver.get(url)

    # detect TOS agreement
    agreement_class_present = len(driver.find_elements(By.CLASS_NAME, value='agreement')) > 0
    print("TOS agreement section is present: ", str(agreement_class_present))

    # if agreement class is present, find TOS agreement checkboxes / submit button
    if agreement_class_present:
        wait = WebDriverWait(driver, 10)
        tos_agree = wait.until(EC.element_to_be_clickable((By.ID, 'tos_agree')))

        # click checkboxes + accept TOS
        actions = ActionChains(driver)
        actions.move_to_element(tos_agree).perform()
        actions.click(tos_agree).perform()

        data_processing_agree = wait.until(EC.element_to_be_clickable((By.ID, 'data_processing_agree')))
        actions.move_to_element(data_processing_agree).perform()
        actions.click(data_processing_agree).perform()

        accept_tos_button = wait.until(EC.element_to_be_clickable((By.ID, 'accept_tos')))
        actions.move_to_element(accept_tos_button).perform()
        actions.click(accept_tos_button).perform()
    else:
        pass

    # return page source / html doc
    driver.implicitly_wait(10) # seconds

    # find /html/body/div[1]/div[1]/div/ol[2]
    body = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/ol[2]')
    body_outer = body.get_attribute('outerHTML')

    # get BeautifulSoup object
    soup = BeautifulSoup(body_outer, 'html.parser')

    return soup

def get_all_links(soup):
    """Takes in BeautifulSoup object from get_html_doc and returns a list of all links in the object."""
    links = soup.find_all('a')
    for link in links:
        link = link.get('href')
    return links

def get_urls_only(links_list):
    """Takes in a list of all links from get_all_urls and returns a list of only the URL strings."""
    # use regex to get just URLs
    urls_only = []
    pattern = r'\"(.*?)\"'
    for i in range(len(links_list)):
        link_str = str(links_list[i])
        match = re.search(pattern, link_str)
        if match:
            urls_only.append(match.group(1))
        else:
            continue

    # update URLs if they do not include 'http://archiveofourown.org' at the start
    for i in range(len(urls_only)):
        if urls_only[i][0] == '/':
            urls_only[i] = 'https://archiveofourown.org' + urls_only[i]
        else:
            continue

    return urls_only

def get_work_links(urls_only):
    """Pares down a list of URLs from get_urls_only to a list of URLs associated with fanworks (as opposd to Ao3 tags, bookmarks, collections, search, users, etc."""
    work_links = []
    for i in range(len(urls_only)):
        if 'https://archiveofourown.org/works/' in urls_only[i]:
            work_links.append(urls_only[i])
        else:
            continue
    return work_links

def pare_down_work_links(work_links):
    """Takes a list of fanwork links from get_work_links and pares down to links that only end in digits (i.e. the link to the first page of an individual fanwork, rather than links to kudos, comments, chapters, etc. associated with that fanwork)."""
    works_only = []
    pattern = r'\d+$'
    for i in range(len(work_links)):
        match = re.search(pattern, work_links[i])
        if match:
            works_only.append(work_links[i])
        else:
            continue

    return works_only

def remove_chapter_links(work_links_pared):
    """Takes in a list of pared down fanwork URLs from pare_down_work_links and removes any links to individual fanwork chapters."""
    works_only = work_links_pared
    for link in works_only:
        if 'chapter' in link:
            works_only.remove(link)
        else:
            continue
    return works_only

def save_links_to_txt(file_path, links_to_scrape):
    """Writes the list of fanwork links from works_only_final to a .txt file."""

    # Using "with open" syntax to automatically close the file
    with open(file_path, 'w') as file:
        # Join the list elements into a single string with a newline character
        data_to_write = '\n'.join(links_to_scrape)

        # Write the data to the file
        file.write(data_to_write)

    print(f"The list of links to scrape has been written to {file_path}.")