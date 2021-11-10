
import pandas as pd

df = pd.read_csv("assistfreq_all_clean.csv")
#print(df)

def fullprint(dataframe, playerID):
    shooterDF = dataframe.loc[dataframe['shooterID'] == playerID]
    shooterDF = shooterDF.drop(['uniqueID', 'shooterName', 'shooterID', 'assisterID'], axis = 1)
    shooterDF = shooterDF.sort_values('counter', ascending=False)

    assisterDF = dataframe.loc[dataframe['assisterID'] == playerID]
    assisterDF = assisterDF.drop(['uniqueID','assisterName', 'shooterID', 'assisterID'], axis=1)
    assisterDF = assisterDF.sort_values('counter', ascending = False)

    print(shooterDF)
    print(assisterDF)

def shortprint(dataframe, playerID, num):
    shooterDF = dataframe.loc[dataframe['shooterID'] == playerID]
    shooterDF = shooterDF.drop(['uniqueID', 'shooterName', 'shooterID', 'assisterID'], axis = 1)
    shooterDF = shooterDF.sort_values('counter', ascending=False)

    assisterDF = dataframe.loc[dataframe['assisterID'] == playerID]
    assisterDF = assisterDF.drop(['uniqueID','assisterName', 'shooterID', 'assisterID'], axis=1)
    assisterDF = assisterDF.sort_values('counter', ascending = False)

    print(shooterDF.head(num))
    print(assisterDF.head(num))

def niceprint(dataframe, playerID, num):
    shooterDF = dataframe.loc[dataframe['shooterID'] == playerID]
    shooterDF = shooterDF.drop(['uniqueID', 'shooterName', 'shooterID', 'assisterID'], axis = 1)
    shooterDF = shooterDF.sort_values('counter', ascending=False)
    assisternames = shooterDF['assisterName'].tolist()
    assistercounter = shooterDF['counter'].tolist()

    assisterDF = dataframe.loc[dataframe['assisterID'] == playerID]
    assisterDF = assisterDF.drop(['uniqueID','assisterName', 'shooterID', 'assisterID'], axis=1)
    assisterDF = assisterDF.sort_values('counter', ascending = False)
    shooternames = assisterDF['shooterName'].tolist()
    shootercounter = assisterDF['counter'].tolist()

    print("| Assists TO Player | Player Name |")
    print("|:------:|:------:|")
    for x in range(0, num):
        print("| " + shooternames[x] + " | " + str(shootercounter[x]) + " |")

    print("\n")

    print("| Assists FROM Player | Player Name |")
    print("|:------:|:------:|")
    for x in range(0, num):
        print("| " + assisternames[x] + " | " + str(assistercounter[x]) + " |")

def mostconnectionsniceprint(df):
    dataframe = df.sort_values('counter', ascending=False)
    shooternames = dataframe['shooterName'].tolist()
    assisternames = dataframe['assisterName'].tolist()
    numberassists = dataframe['counter'].tolist()

    print("| Shooter | Assister | Number of assists |")
    print("|:------:|:------:|:------:|")
    for x in range(0,10):
        print("| " + shooternames[x] + " | " + assisternames[x] + " | " + str(numberassists[x]) + " |")

def toofromdiscrepency(df):
    df2 = df
    df2 = df2.drop(['shooterName', 'assisterName', 'uniqueID'], axis=1)
    df2 = df2.rename(columns={"counter" : "revcounter", "shooterID" : "tempID1", "assisterID": "tempID2"})
    df2 = df2.rename(columns={"tempID1" : "assisterID", "tempID2": "shooterID"})
    df3 = pd.merge(df, df2, how='left', left_on=['shooterID', 'assisterID'], right_on=['shooterID', 'assisterID'])
    df3['discrep'] = df3['counter'] - df3['revcounter']
    df3 = df3.sort_values('discrep', ascending=False)
    shooternames = df3['shooterName'].tolist()
    assisternames = df3['assisterName'].tolist()
    sizediscrep = df3['discrep'].tolist()

    print("| More Baskets | More Assists | Size of Discrepency |")
    print("|:------:|:------:|:------:|")
    for x in range(0,10):
        print("| " + shooternames[x] + " | " + assisternames[x] + " | " + str(int(sizediscrep[x])) + " |")

#fullprint(df, "malonka01")
#fullprint(df, "duncati01")
#fullprint(df, "duranke01")

#shortprint(df, "malonka01", 5)
#shortprint(df, "duncati01", 5)
#shortprint(df, "duranke01",5 )

niceprint(df, "jamesle01", 5)
niceprint(df, "anthoca01", 5)
niceprint(df, "beysa01", 5)
niceprint(df, "simmobe01", 5)

mostconnectionsniceprint(df)

pd.set_option("display.max_rows", 100, "display.max_columns", None)
toofromdiscrepency(df)


