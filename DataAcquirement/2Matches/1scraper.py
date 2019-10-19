p = print
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import datetime;import pandas as pd

class MatchScraper:

    def __init__(self, link):
        self.link = "https://www.hltv.org/" + link
        self.matchID = link[9:16]
        self.soup = BeautifulSoup(requests.get(self.link).content, 'html.parser')
        self.mapsPlayed = self.getMaps()
        print(self.mapsPlayed, self.matchID)
        self.date = self.getDate()
        self.noMapsPlayed = len(self.mapsPlayed)
        self.startSide = self.getStartSide()
        self.scores = self.getScores()
        self.teamIDs = self.getTeamIDs()
        self.stats = self.getStats()

    def getDate(self):
        date = self.soup.find('div', class_ ='date')
        months = {
        'January' : 1,
        'February' : 2,
        'March' : 3,
        'April' : 4,
        'May' : 5,
        'June' : 6,
        'July' : 7,
        'August' : 8,
        'September' : 9,
        'October' : 10,
        'November' : 11,
        'December' : 12}
        date = date.text
        date = date.split(" ")
        day = "".join(filter(lambda x: x.isdigit(), date[0]))
        month = months[date[2]]
        year = date[3]
        return str(month) + "/" + str(day) + "/" + str(year)[2:]

    def getMaps(self):
        mapholders = self.soup.find_all('div', class_ = 'mapholder')
        maps = self.soup.find_all('div', class_='mapname')
        playedmaps = []
        count = 0
        for i in mapholders:
            if len(i.findChildren()) > 4:
                count += 1
        for i in range(count):
            playedmaps.append(maps[i].text)
        return playedmaps

    def getStartSide(self):
        mapholders = self.soup.find_all('div', class_='mapholder')
        sides = []
        for i in mapholders:

            try:
                k = i.findChild('div', class_='results')
                k = k.find_all('span')
                if str(k[4]['class']) == "['ct']":
                    sides.append("CT")
                    sides.append("T")
                else:
                    sides.append("T")
                    sides.append("CT")

            except AttributeError:
                pass
        return sides

    def getScores(self):
        mapholders = self.soup.find_all('div', class_ = 'mapholder')
        scores = []
        for i in mapholders:

            try:
                text = i.findChild('div', class_ = 'results').text
                # get final scores
                scorestr = text[:5]
                scorestr = scorestr.split(':')
                scorestr = [int(x) for x in scorestr]
                for i in scorestr:
                    scores.append(i)
                # get side scores
                scorestr = text
                s = scorestr[scorestr.find("(") + 1 : scorestr.find(";")].split(":")
                s = [int(x) for x in s]
                for i in s:
                    scores.append(i)
                s = scorestr[scorestr.find(";") + 2 : scorestr.find(")")].split(":")
                s = [int(x) for x in s]
                for i in s:
                    scores.append(i)
                #self.startSide =
            except AttributeError:
                pass
        return scores

    def getTeamIDs(self):
        ids = self.soup.find_all('img', class_ = "logo")
        idlist = []
        for i in ids:
            id = int(i['src'][-4:])
            if idlist.__contains__(id):
                break
            else:
                idlist.append(id)
        return idlist

    def getStats(self):
        # needs to know number of maps played
        # hierarchy: map, team, player, stats
        master = []
        for i in range(self.noMapsPlayed):
            map = self.soup.find_all('table', class_ = 'table')[2 * i + 2 : 2 * i + 4]
            for j in map:
                players = j.find_all('tr', class_ = "")
                maplist = []
                for k in players:
                    stats1 = k.find_all('td')
                    temp = []
                    for l in stats1:
                        temp.append(l.text)
                    try:
                        del temp[0]
                        del temp[1]
                        kd = temp[0].split('-')
                        del temp[0]
                        temp.insert(0, kd[0])
                        temp.insert(1, kd[1])
                        temp = [x.replace("%", "") for x in temp]
                        temp = [float(x) for x in temp]
                    except IndexError:
                        pass

                    maplist.append(temp)
                master.append(maplist)
        return master

    def createPlayerStats(self):

        output = open('playerStatsUnparsed.csv', 'a')

        for tablelist in range(self.noMapsPlayed * 2):
            for playerlist in self.stats[tablelist]:
                output.write("\n")
                output.write(self.mapsPlayed[int(int(tablelist) / 2)] + ",")
                output.write(str(self.teamIDs[tablelist % 2]) + ",")
                output.write("na,")
                for statslist in playerlist:
                    output.write(str(statslist) + ",")
                output.write("2.0,")
                output.write(self.matchID)

    def createMatchResults(self):
        output = open('matchResultsUnparsed.csv', 'a')

        for i in range(self.noMapsPlayed):
            output.write("\n")
            output.write(self.date + ",") #date
            output.write("0,") #time
            output.write(self.mapsPlayed[i].strip('\'') + ",") #map
            output.write(str(self.teamIDs[0]) + ",") #t1id
            output.write(self.startSide[2 * i] + ",") #t1 start side
            output.write(str(self.scores[6 * i]) + ",") #t1 score
            output.write(str(self.scores[6 * i + 2]) + ",") #t1h1 score
            output.write(str(self.scores[6 * i + 4]) + ",") #t1h2 score
            output.write("0,") #t1 ot score
            output.write(str(self.teamIDs[1]) + ",") #t2 id
            output.write(self.startSide[2 * i + 1] + ",") #t2 start side
            output.write(str(self.scores[6 * i + 1]) + ",") #t2 score
            output.write(str(self.scores[6 * i + 3]) + ",") #t2h1 score
            output.write(str(self.scores[6 * i + 5]) + ",") #t2h2 score
            output.write("0,") #t2 ot score
            output.write(self.matchID) #match id

class ListScraper:
    def __init__(self, link, delay):
        self.link = link
        self.delay = delay
        self.soup = BeautifulSoup(requests.get(self.link).content, 'html.parser')

    def scrape(self):
        resultssublist = self.soup.find_all('div', class_ = 'results-sublist')
        if isFeaturedResults:
            resultssublist = resultssublist[1]
        else:
            resultssublist = resultssublist[0]

        resultscon = resultssublist.find_all('div', class_ = 'result-con')

        for j in resultscon:
            time.sleep(np.random.randint(self.delay * 2))
            link2 = j.find('a', class_ = 'a-reset')['href']
            ms = MatchScraper(link2)
            ms.createPlayerStats()
            ms.createMatchResults()

def findStartDate():
    s = pd.read_csv('matchResultsUnparsed.csv')
    s = s.iloc[-1]['Date']
    s = s.split("/")
    s[0],s[1],s[2] = s[2],s[0].lstrip("0"),s[1].lstrip("0")
    s[0] = "20" + s[0]
    if int(s[1]) < 10:
        s[1] = "0" + s[1]
    if int(s[2]) < 10:
        s[2] = "0" + s[2]
    s = s[0] + "/" + s[1] + "/" + s[2]
    return s

startDate = findStartDate()
print(startDate)
isFeaturedResults = True

while True:
    try:
        link = "https://www.hltv.org/results?startDate=" + startDate.replace("/", "-") + "&endDate=" + startDate.replace("/", "-")
        ls = ListScraper(link, 20)
        ls.scrape()
        print("Date " + startDate + " completed!")

    except Exception as e:
        print(link)
        print(e)
    startDate = (datetime.datetime.strptime(startDate, '%Y/%m/%d') + datetime.timedelta(days=1)).strftime('%Y/%m/%d')