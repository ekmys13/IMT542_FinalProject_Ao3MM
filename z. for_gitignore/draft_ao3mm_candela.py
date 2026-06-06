# This is the script I'm using to draft the process of pulling everything together for the actual data & visualizations

# import scripts
from src.Step2_get_fanwork_links import(get_links_to_scrape)
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



# get_links_to_scrape
file_path = "../data/txt_files/pagination_links.txt"
links_to_scrape = get_links_to_scrape(file_path)

## get pagination links to scrape
fanwork_links1 = get_fanwork_links('../data/txt_files/fanwork_links1.txt')
fanwork_links2 = get_fanwork_links('../data/txt_files/fanwork_links2.txt')
fanwork_links3 = get_fanwork_links('../data/txt_files/fanwork_links3.txt')
fanwork_links4 = get_fanwork_links('../data/txt_files/fanwork_links4.txt')
fanwork_links5 = get_fanwork_links('../data/txt_files/fanwork_links5.txt')
fanwork_links6 = get_fanwork_links('../data/txt_files/fanwork_links6.txt')
fanwork_links7 = get_fanwork_links('../data/txt_files/fanwork_links7.txt')
fanwork_links8 = get_fanwork_links('../data/txt_files/fanwork_links8.txt')
fanwork_links9 = get_fanwork_links('../data/txt_files/fanwork_links9.txt')
fanwork_links10 = get_fanwork_links('../data/txt_files/fanwork_links10.txt')
fanwork_links11 = get_fanwork_links('../data/txt_files/fanwork_links11.txt')

## scrape pagination_link1
total_fanworks = len(fanwork_links1)
fanwork_dict1 = create_all_works_dict()
for i in range(len(fanwork_links1)):
    print("Current fanwork link: ", str(i+1), "of", str(total_fanworks))

    current_work_html = get_fanwork_html(fanwork_links1[i])
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

    append_all_works_dict(current_work_dict, fanwork_dict1)
    print("Successfully appended dictionary to fanwork_dict1 for link: ", str(i+1), " of ", str(total_fanworks))

# convert to json and save to file
fanwork_json1 = convert_to_json(fanwork_dict1)
filepath = '../data/json_files/fanwork_json_files_live/candela_page1.json'
save_json_to_file(filepath, fanwork_json1)

# scrape pagination_link2
total_fanworks = len(fanwork_links2)
fanwork_dict2 = create_all_works_dict()
for i in range(len(fanwork_links2)):
    print("Current fanwork link: ", str(i+1), "of", str(total_fanworks))

    current_work_html = get_fanwork_html(fanwork_links2[i])
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

    append_all_works_dict(current_work_dict, fanwork_dict1)
    print("Successfully appended dictionary to fanwork_dict1 for link: ", str(i+1), " of ", str(total_fanworks))

# convert to json and save to file
fanwork_json1 = convert_to_json(fanwork_dict1)
filepath = '../data/json_files/fanwork_json_files_live/candela_page1.json'
save_json_to_file(filepath, fanwork_json1)
