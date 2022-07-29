"""A web scraper designed to collect the current global male MMA fighter rankings from Tapopology.com"""

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

"""url variables store the web page addresses for scraping."""
url = 'https://www.tapology.com/rankings/top-ten-all-time-greatest-mma-and-ufc-fighters'

"""The soup variable stores the parsed data from the url variable."""
results = get(url)
soup = BeautifulSoup(results.text, 'html.parser')

"""A loop to scrape, parse and append the data from the rest of the pages from the rankings."""
for n in range(2, 20):
    url = f'https://www.tapology.com/rankings/top-ten-all-time-greatest-mma-and-ufc-fighters?page={n}&ranking=3'
    results = get(url)
    soup.append(BeautifulSoup(results.text, 'html.parser'))

"""The list variables below are used to store the extracted information from the parsed data."""
rankings = []
names = []
wins = []
losses = []
draws = []
no_contests = []

"""rankings_list stores the desired information from the parsed data which is in a html list of the class below."""
rankings_list = soup.find_all('li', class_='rankingItemsItem')

"""for loop to pull the data from rankings_list and append to the list variables initiated earlier."""
for entry in rankings_list:
    rank = int(entry.p.text)
    rankings.append(rank)

    title = entry.h1.a.text
    name = re.search(r'', title)
    names.append(name)

    record = entry.find('h1', class_='right').span.text
    rec = re.search(r'(\d+)\-(\d+)\-(\d+),?\s*(\d+)*', record)

    win = int(rec.group(1))
    wins.append(win)

    loss = int(rec.group(2))
    losses.append(loss)

    draw = int(rec.group(3))
    draws.append(draw)

    if rec.group(4) != None:
        no_contest = int(rec.group(4))
    else:
        no_contest = 0
    no_contests.append(no_contest)

"""fighters variable stores the data from the lists in a 2D data frame."""
fighters = pd.DataFrame({
    'rank': rankings,
    'name': names,
    'wins' : wins,
    'losses' : losses,
    'draws' : draws,
    'no contests' : no_contests
})

# print(fighters)

fighters.to_csv('fighters.csv')
