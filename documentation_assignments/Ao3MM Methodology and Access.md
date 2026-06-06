# Ao3MM: Methodology and Access
This document describes how Ao3MM works (i.e. what steps the tool uses to go from a fanwork webpage to a structured JSON array) and gives samples of the "before" and "after" of the information structure.

## Methodology
Ao3 Metadata Mapper organizes fanwork metadata in a JSON array. Ao3MM generates the JSON array in the following steps:
1) First, it takes in the first webpage of an Ao3 fandom (example: https://archiveofourown.org/tags/Candela%20Obscura%20(Critical%20Role%20Web%20Series)/works) and scrapes the page for a list of “pagination links” (box circled in red below). The combined pagination links contain links to all the fanworks for the given Ao3 fandom, but each pagination link only displays 20 fanworks. I have not yet found a reliable way in Ao3’s UI to display all fanwork links on a single page, so it’s necessary to scrape for a list of individual pagination links.

![test.png](assets/screenshots/pagination_links_image.png)

2) Second, for each pagination link, Ao3MM scrapes the webpage for a list of links to the 20 fanworks on that page.
3) Third, for each fanwork link, Ao3MM scrapes the page for the desired metadata, then organizes the metadata into a dictionary. Ao3MM then compiles the individual fanwork dictionaries into a nested dictionary.
4) Fourth, Ao3MM converts the nested dictionary of all fanwork metadata into a JSON array and saves the JSON file to local storage for safekeeping.
5) Last, Ao3MM loads the saved JSON file, converts it to a dataframe, and uses plotly.express to generate visualizations of the saved metadata.

**Python libraries used to accomplish the above steps (beyond native libraries):**

| Library         | Use description                                                                         |
|-----------------|-----------------------------------------------------------------------------------------|
| requests        | pulls html documents from pagination and fanwork links                                  |
| BeautifulSoup   | parses pulled html documents / creates soup objects for text parsing and simplification |
| RegEx           | supports text parsing and simplification of BeautifulSoup objects to extract metadata   |
| json            | converts nested fanwork dictionary to JSON array                                        |
| pandas          | used to create dataframe from JSON array and organize data for visualizations           |
| plotly.express  | creates interactive data visualizations based on standardized Ao3 metadata categories   |

## Access
The goal is for Ao3MM users to be able to fork / download the repository and run the included scripts with a different Ao3 fandom link of their choosing. Users would take the following steps:
- Identify which Ao3 fandom they wish to study, and retrieve the link to the first page of fanworks associated with that fandom tag on Ao3
- Download Ao3MM scripts / package from Github
- Run the Ao3MM scripts with their chosen fanwork page:
-  Run the get_pagination_links script to scrape pagination links 
-  Run the get_fanwork_links script to scrape fanwork links from each pagination link
-  Run the parse_html_docs script to pull metadata from fanworks and organize that metadata into the JSON array
-  Run the create_visualizations script to generate and save visualizations based on the JSON array and the metadata contained within
- Users would then pull visualizations from the assets folder to use / distribute / analyze / present

## Example: parse_html_docs
The example below demonstrates the **parse_html_docs** script. Ao3MM inputs a .txt file list of fanwork links (as generated in the **get_fanwork_links** script) and outputs a JSON array with metadata from each of the fandom links. (Note - this example is using only the first fanwork link in the fanwork_links list.)

### Input
#### .txt file
![test.png](assets/screenshots/fanwork_links_pic.png)
#### html sample from first fanwork link
```

```

### Code
```
## Test Script for parse_html_docs
from src.parse_html_docs import (
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
from src.get_pagination_links import get_html_doc

## Retrieve fanwork links from text file + create list of first 20 fanworks
fanwork_links = get_fanwork_links('/home/ekmys/PycharmProjects/IMT542_FinalProject_Stelter/data/fanwork_links.txt')
one_fanwork = fanwork_links[0:1]
fanwork_to_scrape = one_fanwork[0]

## Scrape fanwork links & create soup objects
total_fanworks = len(one_fanwork)
fanwork_dict = create_all_works_dict()

## load fanworks and create soup objects
soup = get_html_doc(fanwork_to_scrape)
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
filepath = '/home/ekmys/PycharmProjects/IMT542_FinalProject_Stelter/data/json_files/fanwork_dict_forG8.json'
save_json_to_file(fanwork_dict_json_forG8, filepath)
```



### Output: JSON array

#### As Text:
```angular2html
1	
Rating	"Mature"
Archive Warnings	"Graphic Depictions Of Violence"
Category	"Gen"
Fandom	
0	""
1	"Private Nightmares | Project Ghostlight"
2	"Candela Obscura (Critical Role Web Series)"
Characters	
0	""
1	"Katie (Private Nightmares)"
2	"Gable (Private Nightmares)"
3	"Jade (Private Nightmares)"
4	"Eddie (Private Nightmares)"
5	"Naomi (Private Nightmares)"
6	"Robert (Private Nightmares)"
7	"Malcom Trills (Candela Obscura)"
8	"Edgar Lycoris"
9	"Horatio (Private Nightmares)"
10	"Vulo (Private Nightmares)"
11	"Manny (Private Nightmares)"
12	"Cosmo Grimm (Candela Obscura)"
Relationships	
0	""
1	"Eddie & Katie (Private Nightmares)"
2	"Naomi & Jade (Private Nightmares)"
3	"Eddie & Jade (Private Nightmares)"
4	"Gable & Jade (Private Nightmares)"
Additional Tags	
0	""
1	"Vampires"
2	"Gaslamp Fantasy"
3	"Horror"
4	"Monster - Freeform"
5	"Blood"
6	"Body Horror"
7	"Autopsy"
8	"Mystery"
9	"don't look too hard at the Candela timeline"
Language	"English"
Is Series	false
Date Published	"2026-03-04"
Date Updated	"2026-05-12"
Word Count	14223
Chapter Count	"2/?"
Comment Count	4
Kudos Count	6
Bookmarks Count	2
```

#### Screenshot:
![test.png](assets/screenshots/example_json_array.png)