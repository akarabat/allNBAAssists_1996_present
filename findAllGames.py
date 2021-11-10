#########################
### Creating a  program to scrape every assist from every game from basketball-reference.com
### Data available 1996-1997 season and on
### Outputs a dataset to a text document for use in later data analysis
### data of the form (scoring player ID, assisting player ID, gameID, date, scoring team, defending team, assist time)
### November 9, 2021

### This code crates a list of every game from 1996-1997 season to present

#########################

import requests
from bs4 import BeautifulSoup

#### Need list of teams playing in each season to iterate over
allteams_allyears = []
for y in range(1997,2023):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(y) + ".html"
    yearsiteinfo = requests.get(url)
    yearsoup = BeautifulSoup(yearsiteinfo.text, "html.parser")
    for possible in yearsoup.find_all('a'):
        str1 = str(possible.get('href'))
        if str1.find('/teams/') > -1 and str1.find(str(y) + '.html') > -1:
            if str1 not in allteams_allyears:
                allteams_allyears.append(str1)

#### Also need list of playoff games from each year
#### Can't find gameType ID in page, so just going to get list of all playoff games
#### And only add games to all_games_allteams_allyears if they are NOT in playoff game list
#### stupid but whatever
allplayoffgames_allteams_allyears = []
for y in range(1997, 2023):
    url = "https://www.basketball-reference.com/playoffs/NBA_" + str(y) + "_games.html"
    playoffinfo = requests.get(url)
    playoffsoup = BeautifulSoup(playoffinfo.text, "html.parser")
    for possible in playoffsoup.find_all('a'):
        str1 = str(possible.get('href'))
        if str1.find('/boxscores/') > -1 and str1.find('.html') > -1:
            if str1 not in allplayoffgames_allteams_allyears:
                allplayoffgames_allteams_allyears.append(str1)


#### go through each team in each year, log url of all of their games
allgames_allteams_allyears = []
for t in allteams_allyears:
    stringt = str(t)
    newt = stringt[0:stringt.find('.')] + "_games.html"
    print(newt)
    url = "https://www.basketball-reference.com" + newt
    gamessiteinfo = requests.get(url)
    gamesoup = BeautifulSoup(gamessiteinfo.text, "html.parser")
    for possible in gamesoup.find_all('a'):
        str1 = str(possible.get('href'))
        if str1.find('/boxscores/') > -1 and str1.find('.html') > -1:
            if str1 not in allgames_allteams_allyears and str1 not in allplayoffgames_allteams_allyears:
                allgames_allteams_allyears.append(str1)

print(len(allgames_allteams_allyears))
print(len(set(allgames_allteams_allyears)))

textfile= open("allgames.txt","w")
for element in allgames_allteams_allyears:
    textfile.write(element + "\n")
textfile.close()
