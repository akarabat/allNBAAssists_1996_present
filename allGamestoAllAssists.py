#########################
### Creating a  program to scrape every assist from every game from basketball-reference.com
### Data available 1996-1997 season and on
### Outputs a dataset to a text document for use in later data analysis
### data of the form (scoring player ID, assisting player ID, information about the shot made, gameID, assist time)
### November 9, 2021

### This code creates a list of all assists from 1996-1997 season to present
#########################

import requests
from bs4 import BeautifulSoup
import time

#Track runtime
starttime = time.time()

#### Have list of all regular season NBA games from 1996-1997 season on
#### Want to iterate through each game and grab all assists in game
#### Save as data element in text file

## helper functions
def findScorer(info):
    nstart = info.find("/players/")
    nend = info.find(".html")
    return info[nstart+11:nend]

def findAssister(info):
    info = info[info.find(".html")+6:]
    return findScorer(info)

def findShotInfo(info):
    nstart = info.find("</a>")
    nend = info.find("(")
    return info[nstart+4:nend]

def findGameID(info):
    nend = info.find(".html")
    return info[11:nend]

def findGT(info):
    nstart = info.find("<td>")
    nend = info.find("</td>")
    return info[nstart+4:nend]

##break game files up into files of 100 games
##incase any errors arise
lines_per_file = 300
smallfile = None
with open('allgames.txt') as bigfile:
    for lineno, line in enumerate(bigfile):
        if lineno % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            small_filename = 'allgames_{}.txt'.format(lineno + lines_per_file)
            smallfile = open(small_filename, "w")
        smallfile.write(line)
    if smallfile:
        smallfile.close()

allassists = []
for f in range(300, 31200, 300):
    print(str(f))
    filein = "allgames_" + str(f) + ".txt"
    fileout = "allassists_" + str(f) + ".txt"
    allassists.clear()
    with open(filein) as file:
            while (line := file.readline().rstrip()):
                url = "https://www.basketball-reference.com/boxscores/pbp" + line[10:]
                currenttimer = time.time() - starttime
                gamesoupinfo = requests.get(url)
                gamesoup = BeautifulSoup(gamesoupinfo.text, "html.parser")
                for possible in gamesoup.find_all('tr'):
                    str1 = str(possible)
                    if str1.find("assist") > -1:
                        scorer = findScorer(str1)
                        assister = findAssister(str1)
                        shotInfo = findShotInfo(str1)
                        gameID = findGameID(line)
                        gt = findGT(str1)
                        item = (scorer, assister, shotInfo, gameID, gt)
                        allassists.append(item)

    textfile = open(fileout, "w")
    for element in allassists:
        textfile.write(str(element) + "\n")
    textfile.close()

endtime = time.time()
runtime = endtime - starttime

print("time in seconds: " + str(runtime))