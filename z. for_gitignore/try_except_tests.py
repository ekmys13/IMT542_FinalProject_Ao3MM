## Test Script for parse_html_docs with try_except statements

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
first_10_fanworks = fanwork_links[0:10]
fanwork_to_scrape = first_10_fanworks[0]
total_fanworks = len(first_10_fanworks)

for i in range(len(first_10_fanworks)):
    print(first_10_fanworks[i])
    print("Current fanwork link:", str(i+1), "of", total_fanworks)

    ## load fanworks and create soup objects
    soup = get_html_doc_fanworks(first_10_fanworks[i])
    all_dt = get_all_dt(soup)
    print(all_dt)
    if len(all_dt) <= 9:
        all_dt = get_all_dt(soup)
    else:
        pass
    all_dt_updated = update_all_dt(all_dt)
    if len(all_dt_updated) <= 9:
        all_dt_updated = update_all_dt(all_dt)
        print(all_dt_updated)
    else:
        pass
    print(len(all_dt_updated))
    all_dd = get_all_dd(soup)
    if len(all_dd) <= 9:
        all_dd = get_all_dd(soup)
        print(len(all_dd))
    else:
        pass
    print("Successfully loaded fanworks and created soup objects for link", str(i+1))

    ## clean up all_dd
    # all_dd_stripped = strip_dd(all_dd)
    # all_dd_stripped = cleanup_fandom_tags(all_dd_stripped)
    # all_dd_stripped = cleanup_relationship_tags(all_dd_stripped)
    # all_dd_stripped = cleanup_character_tags(all_dd_stripped)
    # all_dd_stripped = cleanup_additional_tags(all_dd_stripped)
    # print(all_dd_stripped)
    # print("Successfully cleaned all_dd_stripped for link", str(i+1))

    ## create individual fanwork dictionary
    # fanwork_dict = create_fanwork_dict(all_dt_updated, all_dd_stripped)
    # print("Successfully created individual fanwork dictionary for link", str(i+1))

    ## append fanwork dictionary to all_works_dict1
    # append_all_works_dict(fanwork_dict, first_20_fanworks)
    # print("Successfully appended individual fanwork dictionary", str(i+1), "to first_20_fanworks.")

## convert to json and save to file
# first20works_json = convert_to_json(first_20_fanworks)
# filepath = '/home/ekmys/PycharmProjects/IMT542_FinalProject_Stelter/data/json_files/first20works_forG8.json'
# save_json_to_file(first20works_json, filepath)