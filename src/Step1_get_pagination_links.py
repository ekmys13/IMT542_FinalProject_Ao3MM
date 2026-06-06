## Step 1: Get Pagination Links

# import libraries
from bs4 import BeautifulSoup
import requests
import re

def get_html_doc(url):
    """Takes in the url for the first page of works for any given Ao3 fandom and returns a BeautifulSoup object from that page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_all_urls(soup):
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

def get_all_ol(soup):
    """Takes in BeautifulSoup object from get_html_doc and returns a list of all elements of the class 'ol'. This is a step in finding all pagination links for a given Ao3 fandom's works."""
    all_ol = soup.find_all('ol')
    all_ol = list(all_ol)
    return all_ol

def get_pagination_links(all_ol):
    """Takes in all 'ol' elements from get_all_ol and returns a list of raw pagination links for that fandom's works."""
    pagination1 = all_ol[0]

    # get only href items from all_ol
    pagination_links = pagination1.find_all('a')
    pagination_links_list = []
    for link in pagination_links:
        print(link.get('href'))
        pagination_links_list.append(link.get('href'))

    return pagination_links_list

def update_pagination_links_list(list):
    """Takes in a list of raw pagination links from get_pagination_links and returns a more parseable list of links to scrape."""
    # get second to last item in list
    pagination_idx = len(list) - 2
    second_to_last_link = list[pagination_idx]

    # get number associated with second-to-last link
    last_page = second_to_last_link.rsplit('=',1)
    last_page_num = last_page[1]

    # generate list of pagination links to scrape
    links_to_scrape = []
    last_page_num1 = int(last_page_num)
    link_str = last_page[0] + '='
    for i in range(1,last_page_num1+1):
        num = str(i)
        full_link = 'https://archiveofourown.org' + link_str + num
        links_to_scrape.append(full_link)

    return links_to_scrape

def save_links_to_txt(file_path, links_to_scrape):
    """Writes the list of pagination links from update_pagination_links_list to a .txt file."""

    # Using "with open" syntax to automatically close the file
    with open(file_path, 'w') as file:
        # Join the list elements into a single string with a newline character
        data_to_write = '\n'.join(links_to_scrape)

        # Write the data to the file
        file.write(data_to_write)

    print(f"The list of links to scrape has been written to {file_path}.")