"""A web scraper designed to collect the current global male MMA fighter rankings from Tapopology.com"""

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

url = 'https://www.tapology.com/rankings/top-ten-all-time-greatest-mma-and-ufc-fighters'    # url variables store the web page addresses for scraping.

results = get(url)          # The soup variable stores the parsed data from the url variable.
soup = BeautifulSoup(results.text, 'html.parser')


for n in range(2, 20):          # A loop to scrape, parse and append the data from the rest of the pages from the rankings.
    url = f'https://www.tapology.com/rankings/top-ten-all-time-greatest-mma-and-ufc-fighters?page={n}&ranking=3'
    results = get(url)
    soup.append(BeautifulSoup(results.text, 'html.parser'))

rankings = []           # The list variables below are used to store the extracted information from the parsed data.
names = []
url_names = []
wins = []
losses = []
draws = []
no_contests = []


rankings_list = soup.find_all('li', class_='rankingItemsItem')        # rankings_list stores the desired information from the parsed data which is in a html list of the class below."

for entry in rankings_list:         # for loop to pull the data from rankings_list and append to the list variables initiated earlier.
    rank = int(entry.p.text)
    rankings.append(rank)

    title = entry.h1.a.text         # Pulling and splitting the name of each fighter into groups before appending the name to the names list.
    name = re.search(r'("[\w\s\'.-]*)?("\s)?([\w\s\'.-]*)?("[\w\s\'.-]*)?("\s)?([\w\s\'.-]*)?("[\w\s\'.-]*)?(")?', title)
    names.append(name.group())

    url_name = name.group(3)            # Extracting and appending the full name from the name variable, without the nickname of each fighter, to the url_names list.
    if name.group(4) != None:
        url_name += name.group(6)
    if url_name[-1] == ' ':
        url_name = url_name[0:-1]

    if name.group(1) != None:           # Extracting and appending the nickname from the name variable of each fighter to the nicknames list.
        url_name += name.group(1)
    elif name.group(4) != None:
        url_name += name.group(4)
    elif name.group(7) != None:
        url_name += name.group(7)
    url_name = re.sub('\.', '', url_name)
    url_name = re.sub('[\s"]', '-', url_name)
    url_name = url_name.lower()
    url_names.append(url_name)

    records = entry.find('h1', class_='right').span.text            # Pulling a string of the record of each fighter and splitting it into groups before storing it in the record variable.
    record = re.search(r'(\d+)\-(\d+)\-(\d+),?\s*(\d+)*', records)

    win = int(record.group(1))          # Extracting the wins, losses, draws and no contests from the record variable and converting them to integers for each fighter before appending to their relevant list. If there aren't any no contests, we append 0.
    wins.append(win)

    loss = int(record.group(2))
    losses.append(loss)

    draw = int(record.group(3))
    draws.append(draw)

    if record.group(4) != None:
        no_contest = int(record.group(4))
    else:
        no_contest = 0
    no_contests.append(no_contest)

# fighters variable stores the data from the lists in a 2D data frame.
fighters = pd.DataFrame({
    'rank': rankings,
    'name': names,
    'url name' : url_names,
    'wins' : wins,
    'losses' : losses,
    'draws' : draws,
    'no contests' : no_contests
})

print(fighters)

fighters.to_csv('fighters.csv')
