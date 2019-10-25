p = print
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import datetime;import pandas as pd
import cfscrape
import csv

# scrapes the points of the top X teams on HLTV leaderboard, every month. Used to calculate pd feature.

class MatchScraper:

    def __init__(self, link):
        self.link = link

class ListScraper:
    def __init__(self, link, delay):
        self.link = link
        self.delay = delay
        self.scraper = cfscrape.create_scraper()
        #self.soup = BeautifulSoup(requests.get(self.link).content, 'html.parser')
        self.soup = str(self.scraper.get(link).content)
        self.ids = []
        self.points = []

    def scrape(self):

        #resultssublist = self.soup.find_all('div', class_ = 'ranked-team standard-box')
        #resultssublist = self.soup.find_all('span', class_='team-logo')
        for rank in np.arange(noTeams):
            rank += 1
            positionindex = self.soup.index("position\">#" + str(rank))
            idstring = self.soup[positionindex:positionindex + 220]
            logoindex = idstring.index("/logo/")
            id = idstring[logoindex + 6: logoindex + 10]
            self.ids.append(int(id))

            # find points
            pointsstring = self.soup[positionindex:positionindex + 1000]
            pointindex = pointsstring.index("points\">")
            points = pointsstring[pointindex + 9: pointindex + 13]
            points = pointsstring[pointindex + 9: pointindex + 13].replace("p","").replace("o","")
            print(points)
            self.points.append(int(points))

            #for j in resultscon:
             #   time.sleep(np.random.randint(self.delay * 2))
              #  link2 = j.find('a', class_ = 'a-reset')['href']
               # ms = MatchScraper(link2)
                #ms.createPlayerStats()
                #ms.createMatchResults()

link = "https://www.hltv.org/ranking/teams/2018/september/24"
link ="https://www.hltv.org/ranking/teams/2018/august/27"
link ="https://www.hltv.org/ranking/teams/2018/july/30"
link ="https://www.hltv.org/ranking/teams/2018/june/25"
link ="https://www.hltv.org/ranking/teams/2018/may/28"
link ="https://www.hltv.org/ranking/teams/2018/april/30"
link ="https://www.hltv.org/ranking/teams/2018/march/26"
link ="https://www.hltv.org/ranking/teams/2018/february/26"
link ="https://www.hltv.org/ranking/teams/2018/january/29"
link ="https://www.hltv.org/ranking/teams/2017/december/25"
link ="https://www.hltv.org/ranking/teams/2017/november/27"
# link ="https://www.hltv.org/ranking/teams/2017/october/30"
# link ="https://www.hltv.org/ranking/teams/2017/september/25"
# link ="https://www.hltv.org/ranking/teams/2017/august/28"
# link ="https://www.hltv.org/ranking/teams/2017/july/31"
# link ="https://www.hltv.org/ranking/teams/2017/june/26"
# link ="https://www.hltv.org/ranking/teams/2017/may/29"
# link ="https://www.hltv.org/ranking/teams/2017/april/24"
# link ="https://www.hltv.org/ranking/teams/2017/march/27"
# link ="https://www.hltv.org/ranking/teams/2017/february/27"
# link ="https://www.hltv.org/ranking/teams/2017/january/30"
# link ="https://www.hltv.org/ranking/teams/2016/december/26"
# link ="https://www.hltv.org/ranking/teams/2016/october/24"
# link ="https://www.hltv.org/ranking/teams/2016/november/28"
#link ="https://www.hltv.org/ranking/teams/2016/october/24"
#link ="https://www.hltv.org/ranking/teams/2016/september/26"
#link = "https://www.hltv.org/ranking/teams/2016/august/29"
# link ="https://www.hltv.org/ranking/teams/2016/july/26"
# link ="https://www.hltv.org/ranking/teams/2016/june/27"
# link ="https://www.hltv.org/ranking/teams/2016/may/23"
# link ="https://www.hltv.org/ranking/teams/2016/april/25"
# link = "https://www.hltv.org/ranking/teams/2016/march/28"
# link = "https://www.hltv.org/ranking/teams/2016/february/22"

noTeams = 30
ls = ListScraper(link, noTeams)
ls.scrape()
monthdict = {'january':'1','february':'2','march':'3','april':'4',
     'may':'5','june':'6','july':'7','august':'8','september':'9',
     'october':'10','november':'11','december':'12'}

with open('ranks.csv', 'a') as csvfile:
    # writes something like "05/16; [1423,1535]; [1000,312]. semicolon as delimiter due to commas in lists
    csvfile.write(monthdict[link.split("/")[6]] + "/" + link.split("/")[5][2:]
                  + ";" + str(ls.ids) + ";" + str(ls.points) + "\n")