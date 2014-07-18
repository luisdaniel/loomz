"""
For an Organization, get info about discussion lengths
@author soph
"""

from bs4 import BeautifulSoup
import requests # The urllib2 module is bad, this is better.


# First get all discussions
base_url = "https://internet-party.loomio.org/"

# For now hardcode page_num, don't know how to get total
# For pages: base_url + "?page=" + page_num

TOTAL_PGS = 16
for i in range(1, TOTAL_PGS): 
    r = requests.get(base_url + "?page=" + str(i))
    page = r.text
    soup = BeautifulSoup(page)

    titles = [t.text for t in soup.find_all('div', {'class':'discussion-title'})]
    links = soup.find_all('a', {'class': 'selector-discussion-link'})

    print "DISCUSSION_TITLE\tDISCUSSION_LINK\tNUM_TEXTS\tWORD_COUNT"
        
    for title, link in zip(titles, links):
        discussion_url = link.get('href')
        r = requests.get(base_url + discussion_url)
        page = r.text
        soup = BeautifulSoup(page)

        # Count the number of activities on this topic
        responses = soup.find_all('li', {'class': 'activity-tem-container'})
        num_responses = len(responses) 

        # Count the number of text replies to this topic
        text_responses = soup.find_all('span',
            {'class': 'activity-item-content word-break'})
        texts = [t.text for t in text_responses if t.text]
        num_texts = len(texts)

        # Count the total length of text replies
        word_count = sum([len(t.split()) for t in texts])

        # ORG DISCUSSION_TITLE DISCUSSION_LINK NUM_TEXTS WORD_COUNT
        print str(base_url) + "\t" + str(title) + "\t" + \
            str(discussion_url) + "\t" + str(num_texts) + \
            "\t" + str(word_count)

