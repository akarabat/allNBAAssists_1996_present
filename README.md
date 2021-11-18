# allNBAAssists_1996_present
A dataset of every assist in the NBA since basketball-reference.com began tracking play-by-play data (1996-1997 season) with some programs to recreate the data and play with it


raw dataset not currently available. Too large for Github and its throwing me some weird errors that I don't understand yet. Will update.

NOTE - if you want this just message me on reddit (karabou_1) and I'll happily send it to you in a dropbox or something, it's not even a big file it's just too big for github and I don't feel like dealing with it


The raw dataset is reproducable from the programs, but it can over 2 hours to run


files run 1. findAllGames.py (prints out allgames.txt, which is included, so this doesn't need to be run)

2. allGamestoAllAssists.py (this prints out ~100 allassists_##.txt files) <- this is the program that takes a lot of time to run

3. combines all of the allassists_##.txt programs, reads them in and outputs assistfreq_all.csv (included) which lists the number of assists from player A to player B for any 2 players that had at least one assist in that time

4. niceprint.py prints tables 
