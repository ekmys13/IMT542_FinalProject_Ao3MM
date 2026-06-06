### Step 3: Parse HTML Docs

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import re
import json

## Retrieve list of fanwork links from text file
def get_fanwork_links(filepath):
    """Takes in a txt file of pagination links and returns a list."""
    fanwork_links = open(filepath).readlines()
    for i in range(len(fanwork_links)):
        fanwork_links[i] = fanwork_links[i].replace("\n","")
    return fanwork_links

## Scrape fanwork links and create soup objects
def get_fanwork_html(url):
    """
    Takes in a fanwork URL from the list returned in get_fanwork_links and
    returns the outerHTML value from the work_meta_group class.
    """
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

    # detect adult content warning
    accept_adult_content_present = len(driver.find_elements(By.LINK_TEXT, 'Yes, Continue')) > 0
    print("Adult content warning is present: ", str(accept_adult_content_present))

    if accept_adult_content_present:
        wait = WebDriverWait(driver, 15)
        accept_adult_content_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Yes, Continue')))

        # click link + accept adult content warning
        actions = ActionChains(driver)
        actions.move_to_element(accept_adult_content_button).perform()
        actions.click(accept_adult_content_button).perform()

    else:
        pass

    # return page source / html doc
    driver.implicitly_wait(10) # seconds

    # get OuterHTML from 'work meta group'
    work_meta_group = driver.find_element(By.CLASS_NAME, 'wrapper')
    outer_html = work_meta_group.get_attribute('outerHTML')

    return outer_html

def get_soup(html):
    """Takes in outer_html from get_fanwork_html and returns BeautifulSoup object."""
    soup = BeautifulSoup(html, features='html.parser')
    return soup

def detect_adult_content_warning(soup):
    h2 = soup.find('h2')
    string = str(h2.string)
    if string == "Adult Content Warning":
        adult_content_present = True
    else:
        adult_content_present = False
    return adult_content_present

## Retrieve Metadata - works with "adult content warning"
def get_rating_adult(soup):
    rating_class = soup.find_all(attrs={'class':'rating'})
    if len(rating_class) == 0:
        rating_list = "Rating not tagged"
    else:
        rating_list = []
        for item in rating_class:
            tag = item
            string = tag.string
            rating_list.append(string)
        rating_list = list(set(rating_list))
        for i in range(len(rating_list)):
            rating_list[i] = str(rating_list[i])
        if len(rating_list) == 1:
            rating_list = rating_list[0]
        else:
            pass
    return rating_list

def get_warnings_adult(soup):
    warning_class = soup.find_all(attrs={'class':'warnings'})
    if len(warning_class) == 0:
        warning_list = "Warnings not tagged"
    else:
        warnings_list = []
        for item in warning_class:
            tag = item
            string = tag.string
            warnings_list.append(string)
        warnings_list = list(set(warnings_list))
        for i in range(len(warnings_list)):
            warnings_list[i] = str(warnings_list[i])
        if len(warnings_list) == 1:
            warnings_list = warnings_list[0]
        else:
            pass
    return warnings_list

def get_category_adult(soup):
    category_class = soup.find_all(attrs={'class':'category'})
    if len(category_class) == 0:
        category_list = "No categories tagged"
    else:
        category_list = []
        for item in category_class:
            tag = item
            string = tag.string
            category_list.append(string)
        rating_list = list(set(category_list))
        for i in range(len(category_list)):
            category_list[i] = str(category_list[i])
        if len(category_list) == 1:
            category_list = category_list[0]
        else:
            pass
    return category_list

def get_language_adult(soup):
    language_class = soup.find_all(attrs={'class':'language'})
    language_list = []
    for item in language_class:
        tag = item
        string = str(tag.string)
        language_list.append(string)
    language = language_list[1]
    return (language)

def get_fandom_adult(soup):
    fandom_class = soup.find(attrs={'class':'fandoms heading'}).find('a')
    fandom_list = []
    for item in fandom_class:
        string = str(item.string)
        fandom_list.append(string)
    fandom_list = list(set(fandom_list))
    if len(fandom_list) == 1:
        fandom_list = fandom_list[0]
    else:
        pass
    return fandom_list

def get_relationships_adult(soup):
    relationships_class = soup.find_all(attrs={'class':'relationships'})
    if len(relationships_class) == 0:
        relationships_list = 'No relationships tagged'
    else:
        relationships_list = []
        for item in relationships_class:
            string = str(item.string)
            relationships_list.append(string)
        if len(relationships_list) == 1:
            relationships_list = relationships_list[0]
        else:
            pass
    return relationships_list

def get_characters_adult(soup):
    character_class = soup.find_all(attrs={'class':'characters'})
    if len(character_class) == 0:
        character_list = 'No characters tagged'
    else:
        character_list = []
        for item in character_class:
            string = str(item.string)
            character_list.append(string)
    return character_list

def get_additional_adult(soup):
    freeform_class = soup.find_all(attrs={'class':'freeforms'})
    if len(freeform_class) == 0:
        freeform_list = 'No additional tags'
    else:
        freeform_list = []
        for item in freeform_class:
            string = str(item.string)
            freeform_list.append(string)
    return freeform_list

def get_date_published_adult(soup):
    published_class = soup.find_all(attrs={'class':'published'})
    if len(published_class) == 0:
        published_list = 'Unknown'
    else:
        published_list = []
        for item in published_class:
            string = str(item.string)
            published_list.append(string)
    return published_list

def get_date_updated_adult(soup):
    updated_class = soup.find_all(attrs={'class':'datetime'})
    if len(updated_class) == 0:
        date_updated = 'Unknown'
    else:
        updated_list = []
        for item in updated_class:
            string = str(item.string)
            updated_list.append(string)
        date_updated = updated_list[0]
    return date_updated

def get_comment_count_adult(soup):
    comments_class = soup.find_all(attrs={'class':'comments'})
    if len(comments_class) < 2:
        comment_count = 0
    else:
        comment_count_list = []
        for item in comments_class:
            string = str(item.string)
            comment_count_list.append(string)
        comment_count = comment_count_list[1]
    return comment_count

def get_bookmarks_count_adult(soup):
    bookmarks_class = soup.find_all(attrs={'class':'bookmarks'})
    if len(bookmarks_class) == 0:
        bookmarks_count = 0
    else:
        bookmarks_count_list = []
        for item in bookmarks_class:
            string = str(item.string)
            bookmarks_count_list.append(string)
        bookmarks_count = bookmarks_count_list[1]
    return bookmarks_count

def get_hits_count_adult(soup):
    hits_class = soup.find_all(attrs={'class':'hits'})
    if len(hits_class) == 0:
        hits_count = 0
    else:
        hits_count_list = []
        for item in hits_class:
            string = str(item.string)
            hits_count_list.append(string)
        hits_count = hits_count_list[1]
    return hits_count


## Retrieve Metadata - works without "adult content warning"
def get_rating_nonadult(soup):
    """Get rating for fanworks that do NOT have the adult content warning."""
    rating_class = soup.find_all(attrs={'class':'rating tags'})
    if len(rating_class) == 0:
        rating = 'Unknown'
    else:
        rating_class1 = rating_class[1]
        tag = rating_class1.find('a')
        string = str(tag.string)
        rating = string
    return rating

def get_warnings_nonadult(soup):
    warnings_list = []
    warning_class = soup.find_all(attrs={'class':'warning tags'})
    if len(warning_class) == 0:
        warnings_list = "Warnings not tagged"
    else:
        warning_class1 = warning_class[1]
        tag = warning_class1.find('a')
        string = str(tag.string)
        warnings_list.append(string)
        if len(warnings_list) == 1:
            warnings_list = warnings_list[0]
    return warnings_list

def get_category_nonadult(soup):
    category_class = soup.find_all(attrs={'class':'category tags'})
    if len(category_class) == 0:
        category = "No categories tagged"
    else:
        category_class1 = category_class[1]
        tag = category_class1.find('a')
        string = str(tag.string)
        category = string
    return category

def get_language_nonadult(soup):
    """Reads in BeautifulSoup object and returns fanwork language as string."""
    language_class = soup.find_all(attrs={'class':'language'})
    language_list = []
    for item in language_class:
        tag = item
        string = str(tag.string)
        language_list.append(string)
    language_list1 = language_list[1]
    language_list1 = language_list1.split('\n')
    language = language_list1[1]
    language = language.strip()
    return (language)

def get_fandom_nonadult(soup):
    fandom_class = soup.find_all(attrs={'class':'fandom tags'})
    fandom_class1 = fandom_class[1]
    fandom_list = []
    for child in fandom_class1:
        tag = fandom_class1.find('a')
        string = tag.string
        fandom_list.append(string)
    fandom_list = list(set(fandom_list))
    if len(fandom_list) == 1:
        fandom = fandom_list[0]
        return fandom
    else:
        return fandom_list

def get_relationships_nonadult(soup):
    relationships_class = soup.find_all(attrs={'class':'relationship tags'})
    if len(relationships_class) == 0:
        relationships_list = "No relationships tagged"
    else:
        relationships_class1 = relationships_class[1]
        for child in relationships_class1:
            tag_list = relationships_class1.find_all('a')
            relationships_list = []
            for tag in tag_list:
                string = str(tag.string)
                relationships_list.append(string)
            if len(relationships_list) == 1:
                relationships_list = relationships_list[0]
            else:
                pass
    return relationships_list

def get_characters_nonadult(soup):
    character_class = soup.find_all(attrs={'class':'character tags'})
    if len(character_class) == 0:
        character_list = "No characters tagged"
    else:
        character_class1 = character_class[1]
        for child in character_class1:
            tag_list = character_class1.find_all('a')
            character_list = []
            for tag in tag_list:
                string = str(tag.string)
                character_list.append(string)
    return character_list

def get_additional_nonadult(soup):
    freeform_class = soup.find_all(attrs={'class':'freeform tags'})
    if len(freeform_class) == 0:
        freeform_list = "No additional tags"
    else:
        freeform_class1 = freeform_class[1]
        for child in freeform_class1:
            tag_list = freeform_class1.find_all('a')
            freeform_list = []
            for tag in tag_list:
                string = str(tag.string)
                freeform_list.append(string)
    return freeform_list

def get_date_published_nonadult(soup):
    published_class = soup.find_all(attrs={'class':'published'})
    if len(published_class) == 0:
        published_list = 'Unknown'
    else:
        published_list = []
        for item in published_class:
            string = str(item.string)
            published_list.append(string)
        published_list = published_list[1]
    return published_list

def get_date_updated_nonadult(soup):
    updated_class = soup.find_all(attrs={'class':'status'})
    if len(updated_class) == 0:
        updated_list = 'Unknown'
    else:
        updated_list = []
        for item in updated_class:
            string = str(item.string)
            updated_list.append(string)
        updated_list = updated_list[1]
    return updated_list

def get_comment_count_nonadult(soup):
    comments_class = soup.find_all(attrs={'class':'comments'})
    if len(comments_class) < 2:
        comments_count = 0
    else:
        string = str(comments_class[2].string)
        comments_count = int(string)
    return comments_count

def get_bookmarks_count_nonadult(soup):
    bookmarks_class = soup.find_all(attrs={'class':'bookmarks'})
    if len(bookmarks_class) == 0:
        bookmarks_count = 0
    else:
        string = str(bookmarks_class[1].string)
        bookmarks_count = int(string)
    return bookmarks_count

def get_hits_count_nonadult(soup):
    hits_class = soup.find_all(attrs={'class':'hits'})
    if len(hits_class) == 0:
        hits_count = 0
    else:
        string = str(hits_class[1].string)
        string = string.replace(",","")
        hits_count = int(string)
    return hits_count

## Retrieve Remaining Metadata
"""The functions below work for both the 'adult' and 'nonadult' fanworks."""

def get_word_count(soup):
    word_count_class = soup.find_all(attrs={'class':'words'})
    word_count_list = []
    for item in word_count_class:
        string = str(item.string)
        word_count_list.append(string)
    word_count = word_count_list[1]
    word_count = word_count.replace(",","")
    word_count = int(word_count)
    return word_count

def get_chapter_count(soup):
    chapter_count_class = soup.find_all(attrs={'class':'chapters'})
    chapter_count_list = []
    for item in chapter_count_class:
        string = str(item.string)
        chapter_count_list.append(string)
    chapter_count = chapter_count_list[1]
    return chapter_count

def get_kudos_count(soup):
    kudos_class = soup.find_all(attrs={'class':'kudos'})
    if len(kudos_class) == 0:
        kudos_count = 0
    else:
        kudos_count_list = []
        for item in kudos_class:
            string = str(item.string)
            kudos_count_list.append(string)
        kudos_count = kudos_count_list[1]
    return kudos_count

## Create fanwork dictionary from retrieved metadata

def create_fanwork_dict_adult(soup):
    fanwork_dict = {}

    # add rating
    fanwork_dict['Rating'] = get_rating_adult(soup)
    # add archive warning(s)
    fanwork_dict['Archive Warnings'] = get_warnings_adult(soup)
    # category
    fanwork_dict['Category'] = get_category_adult(soup)
    # add fandom
    fanwork_dict['Fandom'] = get_fandom_adult(soup)
    # add characters
    fanwork_dict['Characters'] = get_characters_adult(soup)
    # add relationships
    fanwork_dict['Relationships'] = get_relationships_adult(soup)
    # add additional tags
    fanwork_dict['Additional Tags'] = get_additional_adult(soup)
    # add language
    fanwork_dict['Language'] = get_language_adult(soup)
    # add stats
    fanwork_dict['Date Published'] = get_date_published_adult(soup)
    fanwork_dict['Date Updated'] = get_date_updated_adult(soup)
    fanwork_dict['Word Count'] = get_word_count(soup)
    fanwork_dict['Chapter Count'] = get_chapter_count(soup)
    fanwork_dict['Comment Count'] = get_comment_count_adult(soup)
    fanwork_dict['Kudos Count'] = get_kudos_count(soup)
    fanwork_dict['Bookmarks Count'] = get_bookmarks_count_adult(soup)
    fanwork_dict['Hits Count'] = get_hits_count_adult(soup)

    return fanwork_dict

def create_fanwork_dict_nonadult(soup):
    fanwork_dict = {}

    # add rating
    fanwork_dict['Rating'] = get_rating_nonadult(soup)
    # add archive warning(s)
    fanwork_dict['Archive Warnings'] = get_warnings_nonadult(soup)
    # category
    fanwork_dict['Category'] = get_category_nonadult(soup)
    # add fandom
    fanwork_dict['Fandom'] = get_fandom_nonadult(soup)
    # add characters
    fanwork_dict['Characters'] = get_characters_nonadult(soup)
    # add relationships
    fanwork_dict['Relationships'] = get_relationships_nonadult(soup)
    # add additional tags
    fanwork_dict['Additional Tags'] = get_additional_nonadult(soup)
    # add language
    fanwork_dict['Language'] = get_language_nonadult(soup)
    # add stats
    fanwork_dict['Date Published'] = get_date_published_nonadult(soup)
    fanwork_dict['Date Updated'] = get_date_updated_nonadult(soup)
    fanwork_dict['Word Count'] = get_word_count(soup)
    fanwork_dict['Chapter Count'] = get_chapter_count(soup)
    fanwork_dict['Comment Count'] = get_comment_count_nonadult(soup)
    fanwork_dict['Kudos Count'] = get_kudos_count(soup)
    fanwork_dict['Bookmarks Count'] = get_bookmarks_count_nonadult(soup)
    fanwork_dict['Hits Count'] = get_hits_count_nonadult(soup)

    return fanwork_dict


## Create empty dictionary for eventual all_works_dict
def create_all_works_dict():
    dict_all_works = {}
    return dict_all_works

## Append all works to all_works_dict (created in create_all_works_dict)
def append_all_works_dict(dict_fanwork, dict_all_works):
    current_length = len(dict_all_works)
    new_idx = current_length + 1
    dict_all_works[new_idx] = dict_fanwork
    return dict_all_works


## Convert all_works_dict to JSON array and save to file
def convert_to_json(dict_all_works):
    json_string = json.dumps(dict_all_works, indent=4)
    return json_string

def save_json_to_file(filepath, json_string):
    with open(filepath, "w") as f:
        f.write(json_string)