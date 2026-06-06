# IMT 542 Assignment G9 Improve access methodology of existing information
Em Stelter, 6/5/2026

## Purpose
This document outlines the recommended testing strategy for Ao3MM users, existing functional tests, as well as planned performance tests, quality metrics, and alarms and monitoring actions.

(---)

## System Overview
Ao3 Metadata Mapper organizes fanwork metadata in a JSON array. Ao3MM generates the JSON array in the following steps:
1) First, it takes in the first webpage of an Ao3 fandom (example: https://archiveofourown.org/tags/Candela%20Obscura%20(Critical%20Role%20Web%20Series)/works) and scrapes the page for a list of “pagination links” (box circled in red below). The combined pagination links contain links to all the fanworks for the given Ao3 fandom, but each pagination link only displays 20 fanworks. I have not yet found a reliable way in Ao3’s UI to display all fanwork links on a single page, so it’s necessary to scrape for a list of individual pagination links.

![test.png](assets/screenshots/pagination_links_image.png)

2) Second, for each pagination link, Ao3MM scrapes the webpage for a list of links to the 20 fanworks on that page.
3) Third, for each fanwork link, Ao3MM scrapes the page for the desired metadata, then organizes the metadata into a dictionary. Ao3MM then compiles the individual fanwork dictionaries into a nested dictionary.
4) Fourth, Ao3MM converts the nested dictionary of all fanwork metadata into a JSON array and saves the JSON file to local storage for safekeeping.
5) Last, Ao3MM loads the saved JSON file, converts it to a dataframe, and uses plotly.express to generate visualizations of the saved metadata.

(---)

## Test Objectives
Ensure that web scraping processes capture:
- All pagination links for the given Ao3 fandom
- All individual fanwork links for each pagination link
- Complete html documents for each fanwork link scraped

Ensure that text processing effectively parses and extracts complete, desired metadata from fanworks

Ensure that extracted metadata is effectively compiled & converted to JSON array and saved locally

Ensure that multiple JSON arrays are successfully merged into a single nested JSON array

(---)

## Functional Testing
These are the functional tests I’ve developed as I have been writing and debugging my code, and these are the tests I would expect another hobbyist fan with a similar level of Python skill to run when using Ao3MM to build their own visualizations. If I were to implement this as a product for market / on a larger scale, I would incorporate more automation. 

However, the expectation here is that individuals will use this code to generate fanwork visualizations on a one-off basis, or perhaps a semi-regular cadence, but Ao3MM is not so much intended for real-time monitoring or daily use as it is for individual meta analysis projects.

### Test Case 1: get pagination links

#### Description / Method
run step1_test_pagination.py
This script will read in the first pagination link for a sample Ao3 fandom (i.e. the first page of search results for the sample fandom’s Ao3 tag) and scrape the test link.

#### Expected Result
The script will return a list of pagination links for the entire fandom (i.e. a list of links to every page of search results for the sample fandom’s Ao3 tag), then save that list as a .txt file.

For the current sample fandom selected, “Candela Obscura (Critical Role Web Series)”, the script should return a .txt file with 11 pagination links (as of 6/5/2026).

### Test Case 2: get_fanwork_links

#### Description / Method
Run step2_test_fanwork_links.py
This script will read in a list of pagination links from the file ‘pagination_links.txt’, select a test pagination link from the list, and scrape the test pagination link.

#### Expected Result
The script will return a list of fanwork links for the test pagination link, then save that list as a .txt file. There should be 20 fanwork links in the .txt file, and none of the fanwork links should contain ‘chapter’ in the link string (i.e. none of the links should go to specific chapters; each link should just go to the first page of the fanwork).

### Test Case 3: parse_html_doc
(individual fanwork links AND parse_html_doc: fanwork links list_

#### Description / Method
Run step3_test_parse_html.py

This script will run three tests. 

The first two tests scrape metadata and create a JSON array for individual fanwork links, one link that contains adult content (i.e. is rated "Mature" or "Explicit") and one that does not (i.e.
is rated "Not Rated," "General Audiences, or "Teen And Up Audiences".

The third test scrapes metadata and creates a nested JSON array for the first 10 fanwork links in
the text file: "fanwork_links.txt".

#### Expected Result
For the first two (individual link) tests, the script will return and save two respective JSON files: test_fanwork_json1.json and test_fanwork_json2.json. Both resulting JSON files should have populated metadata fields (1-2 fields per file may have value=’Unknown’ due to not-yet-solved bugs in the web scraping code, but no more than 1-2 fields.)

For the third (link list) test, the script will return a nested JSON file: ‘first10works_test.json’. There should be a total of 10 JSON arrays with fanwork data nested within the file. 1-2 fields per fanwork may have value=’Unknown’ due to not-yet-solved bugs in the web scraping code, but no more than 1-2 fields.)

### Test Case 4: test_merge_JSON

#### Description / Method
Run step4_test_merge_JSON.py

#### Expected Result
This test will take a list of JSON files created from fandom pagination links and merge them
into a new nested JSON structure, then save that nested structure as ‘all_candela_test.json’.

(---)

## Performance Testing
These performance tests are not yet fully developed, so specific scripts and instructions are not available like they are for the Functional Testing section. However, these would help respond to some of the challenges I encountered with RAM / memory issues when trying to scrape too many webpages in a single script or notebook cell. If I were to operationalize Ao3MM on a larger scale, these performance tests would be how I would determine the efficacy of the tool for collecting metadata from larger Ao3 fandoms (i.e. fandoms with more fanworks) and work to increase the tool’s efficacy.

### Test Case 1: 20 fanwork links
(OR: single pagination link)
#### Description / Method
Input a single pagination link (i.e. link of search results for any given fandom tag).

Run methods from:
Step2_get_fanwork_links.py, Step3_parse_html_docs.py, and Step4_merge_json_files.py

A single pagination link, if scraped properly, should produce a list of 20 fanworks. So this will test how effectively and quickly Ao3MM can return a nested JSON array from 20 fanwork links.

#### Expected Result:
Returns nested JSON array of length=10 populated with data from 10 fanworks.

### Test Case 2: 50 fanwork links
#### Description / Method
Input first pagination link (i.e. first page of search results for any given fandom tag), for any fandom with at least 50 fanworks.

Run methods from:
- Step1_get_pagination_links.py
- Step2_get_fanwork_links.py
- Step3_parse_html_docs.py
- Step4_merge_json_files.py
This will test how effectively and quickly Ao3MM can return a nested JSON array from 50 fanwork links.

#### Expected Result:
Returns nested JSON array of length=50 populated with data from 50 fanworks; 5 or fewer entries only contains “Unknown” fields (i.e. no metadata was successfully scraped)

### Test Case 3: 100 fanwork links
#### Description / Method
Input first pagination link (i.e. first page of search results for any given fandom tag), for any fandom with approximately 100 fanworks.

Run methods from:
- Step1_get_pagination_links.py
- Step2_get_fanwork_links.py
- Step3_parse_html_docs.py
- Step4_merge_json_files.py
This will test how effectively and quickly Ao3MM can return a nested JSON array from 100 fanwork links.

#### Expected Result:
Returns nested JSON array of length=100 populated with data from 100 fanworks; 10 or fewer entries only contains “Unknown” fields (i.e. no metadata was successfully scraped)


### Test case 4: 1,000 fanwork links
#### Description / Method
Input first pagination link (i.e. first page of search results for any given fandom tag), for any fandom with approximately 1,000 fanworks.

Run methods from:
- Step1_get_pagination_links.py
- Step2_get_fanwork_links.py
- Step3_parse_html_docs.py
- Step4_merge_json_files.py
This will test how effectively and quickly Ao3MM can return a nested JSON array from 1,000 fanwork links.

#### Expected Result:
Returns nested JSON array of length=1000 populated with data from 1000 fanworks; 100 or fewer entries only contains “Unknown” fields (i.e. no metadata was successfully scraped)

### Test Case 5: 10,000 fanwork links
#### Description / Method
Input first pagination link (i.e. first page of search results for any given fandom tag), for any fandom with approximately 10,000 fanworks.

Run methods from:
- Step1_get_pagination_links.py
- Step2_get_fanwork_links.py
- Step3_parse_html_docs.py
- Step4_merge_json_files.py
This will test how effectively and quickly Ao3MM can return a nested JSON array from 10,000 fanwork links.

#### Expected Result:
Returns nested JSON array of length=10,000 populated with data from 10,000 fanworks; 1000 or fewer entries only contains “Unknown” fields (i.e. no metadata was successfully scraped)

(---)

## Quality Metrics
Similar to performance tests, these quality metrics are defined but not yet measured in Ao3MM. Adding ways to track these metrics is part of the future scope of the project.

### Metric 1
Time to scrape individual fanwork link and return an HTML document (seconds)
Goal: <=60s per fanwork link (to start)

### Metric 2
Time to scrape individual pagination link doc and return BeautifulSoup object (seconds)
Goal: <=60s per pagination link (to start)

### Metric 3
Number of fanwork links successfully scraped before scraping task is interrupted (i.e. terminal / IDE / computer crashes before the task can be completed)
Goal: >=20 fanwork links scraped per set of links (to start)

### Metric 4
Percentage of ‘Unknown’ entries in a nested JSON (where no data is returned / all entries are blank or ‘Unknown’)
Goal: <=10% of JSON entries have 'Unknown' or blank values (i.e. web scraping tasks returned no metadata)

(---)

## Alarms & Monitoring

### Alarm 1
scraping task interrupted
**Trigger:** process for scraping a list of fanworks does not complete
**Action(s):**
- Shut down terminal
- Check how many fanwork links appended to the fanwork dictionary
- Save combined fanwork dictionary as-is
- Identify which links were not captured
- Rerun scraping task with list of not captured links
If number of fanwork links successfully scraped < 20, test in jupyter notebooks using single fanwork link to troubleshoot.

### Alarm 2
scraping fanwork links is too slow
**Trigger:** scraping time (seconds) per individual fanwork increases to > 60 s for 5 or more fanwork links in a row
**Action(s):**
Add implicit waits of 10 seconds between each fanwork link to see if this helps processing speed / increase the rate of scraping per fanwork link

### Alarm 3 
greater than 10% unknown entries in final JSON arrays
**Trigger:** number of JSON entries with blank / unknown values in combined array reaches > 10% of total fanworks being scraped
**Action(s):**
- Terminate process
- Raise error flag
- Test single link in Jupyter notebooks to troubleshoot.

(---)

# Continuous Testing & Maintenance
- Implement methods to track quality metrics as defined above
- Implement methods to raise alarms as defined above
- Write scripts for performance testing and begin process of incremental performance improvement (identify improvements in processing speed & accuracy based on results of each test before moving to the next performance test)