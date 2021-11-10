#########################
### Creating a  program to scrape every assist from every game from basketball-reference.com
### Data available 1996-1997 season and on
### Outputs a dataset to a text document for use in later data analysis
### data of the form (scoring player ID, assisting player ID, information about the shot made, gameID, assist time)
### November 9, 2021

### This code brings in some player data and performs statistical analysis
#########################

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


#Track runtime
starttime = time.time()

def getPlayerName(soupy):
    titleline = str(soupy.find("title"))
    nstart = titleline.find(">")
    nend = titleline.find(" Stats")
    return titleline[nstart+1:nend]

def stripper(line):
    nstart = line.find("('")
    if nstart == -1:
        nstart = line.find(", '") + 3
    else:
        nstart = nstart + 2
    nend = line.find("',")
    if nend == -1:
        nend = line.find("')")
    data = line[nstart:nend].strip()
    lineout = line[nend + 1:]
    return((data, lineout))


## concatinate many files to one to make overall scores
filenames = []
for x in range(300, 31200, 300):
    fname = "allassists_" + str(x) + ".txt"
    filenames.append(fname)

with open("allassists_all.txt", "w") as outfile:
    for fname in filenames:
        with open(fname ) as infile:
            outfile.write(infile.read())

assists = []
counter = 0
with open("allassists_all.txt") as file:
    while (line := file.readline().rstrip()):
        counter = counter + 1
        if counter % 500 == 0:
            print(counter)

        shooter = stripper(line)[0]
        line = stripper(line)[1]

        assister = stripper(line)[0]
        line = stripper(line)[1]

        typeshot = stripper(line)[0]
        line = stripper(line)[1]

        gameID = stripper(line)[0]
        line = stripper(line)[1]

        timeshot = stripper(line)[0]

        item = (shooter, assister, typeshot, gameID, timeshot)

        assists.append(item)

assistDF = pd.DataFrame(assists, columns=['shooterID', 'assisterID', 'typeshot', 'gameID', 'timeshot'])
assistcountDF = assistDF.drop(['typeshot', 'gameID', 'timeshot'], axis=1)
colIDs = ['shooterID', 'assisterID']
assistcountDF['uniqueID'] = assistcountDF[colIDs].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
assistcountDF['counter'] = 1
pd.set_option("display.max_rows", None, "display.max_columns", None)

freqDF = assistcountDF.groupby('uniqueID', as_index=False).sum('counter')

freqDF = freqDF.sort_values('counter', ascending=False)

print(freqDF.head())
print(freqDF.columns.values)

## bringing the names back in to the frame
freqDF['pos'] = freqDF['uniqueID'].str.find('_')
freqDF['shooterID'] = freqDF.apply(lambda x: x['uniqueID'][0:x['pos']], axis=1)
freqDF['assisterID'] = freqDF.apply(lambda x: x['uniqueID'][x['pos']+1:], axis=1)

print(freqDF.columns.values)
freqDF = freqDF.drop('pos', axis=1)


##get list of all unique players in dataframe
##get their display names from bball-references
shooters = [i[0] for i in assists]
assisters = [i[1] for i in assists]
playersdup = shooters + assisters
players = list(set(playersdup))
print(len(players))
playernames = []

for player in players:
    tempurl = "https://www.basketball-reference.com/players/" + player[0] + "/" + player + ".html"
    print(tempurl)
    tempurlsoupinfo = requests.get(tempurl)
    tempsoup = BeautifulSoup(tempurlsoupinfo.text, "html.parser")
    playername = getPlayerName(tempsoup)
    playernames.append(playername)

print(players)
print(playernames)

shooterNameDF = pd.DataFrame({'shooterID': players,
                   'shooterName': playernames
                   })
assisterNameDF = pd.DataFrame({'assisterID': players,
                   'assisterName': playernames
                   })

freqDF = pd.merge(freqDF, shooterNameDF, how='left')
freqDF = pd.merge(freqDF, assisterNameDF, how='left')

fname2 = "assistfreq_all.csv"
freqDF.to_csv(fname2)