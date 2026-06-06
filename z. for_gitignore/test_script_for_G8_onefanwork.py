## Test Script for parse_html_docs

from src.Step3_parse_html_docs import (
    get_fanwork_links,
    get_html_doc_fanworks,
    get_all_dt,
    update_all_dt,
    get_all_dd,
    strip_dd,
    cleanup_fandom_tags,
    cleanup_character_tags,
    cleanup_relationship_tags,
    cleanup_additional_tags,
    get_rating,
    get_warnings,
    get_fandom,
    get_category,
    get_characters,
    get_relationships,
    get_additional_tags,
    get_language,
    get_date_published,
    get_date_updated,
    get_word_count,
    get_chapter_count,
    get_comment_count,
    get_kudos_count,
    get_bookmarks_count,
    create_fanwork_dict,
    create_all_works_dict,
    append_all_works_dict,
    convert_to_json,
    save_json_to_file
)

from src.Step1_get_pagination_links import get_html_doc

# Retrieve fanwork links from text file + create list of first 20 fanworks
fanwork_links = get_fanwork_links('/data/fanwork_links.txt')
one_fanwork = fanwork_links[0:1]
fanwork_to_scrape = one_fanwork[0]
print(fanwork_to_scrape)

# Scrape fanwork links & create soup objects
total_fanworks = len(one_fanwork)
fanwork_dict = create_all_works_dict()

## load fanworks and create soup objects
soup = get_html_doc(fanwork_to_scrape)
print(soup)
all_dt = get_all_dt(soup)
all_dt_updated = update_all_dt(all_dt)
all_dd = get_all_dd(soup)
print("Successfully loaded fanworks and created soup objects")

## clean up all_dd
all_dd_stripped = strip_dd(all_dd)
all_dd_stripped = cleanup_fandom_tags(all_dd_stripped)
all_dd_stripped = cleanup_relationship_tags(all_dd_stripped)
all_dd_stripped = cleanup_character_tags(all_dd_stripped)
all_dd_stripped = cleanup_additional_tags(all_dd_stripped)
print("Successfully cleaned all_dd_stripped")

## create individual fanwork dictionary
ind_fanwork_dict = create_fanwork_dict(all_dt_updated, all_dd_stripped)
print("Successfully created individual fanwork dictionary")

## append fanwork dictionary to all_works_dict1
append_all_works_dict(ind_fanwork_dict, fanwork_dict)
print("Successfully appended individual fanwork dictionary to overall fanwork_dict.")

## convert to json and save to file
fanwork_dict_json_forG8 = convert_to_json(fanwork_dict)
filepath = '/data/json_files/fanwork_dict_forG8.json'
save_json_to_file(fanwork_dict_json_forG8, filepath)