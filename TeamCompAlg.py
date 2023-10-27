import numpy as np
import sklearn as sk
import pandas as pd
import requests as rq

appearances = pd.read_csv("appearances.csv")
club_games = pd.read_csv("club_games.csv")
clubs = pd.read_csv("clubs.csv")
competitions = pd.read_csv("competitions.csv")
game_events = pd.read_csv("game_events.csv")
game_lineups = pd.read_csv("game_lineups.csv")
games = pd.read_csv("games.csv")
player_valuations = pd.read_csv("player_valuations.csv")
players = pd.read_csv("players.csv")


# "fc-arsenal"
def outcomescorebyplayer(playerid, gameid):
    rel=appearances.loc[(appearances["game_id"]==gameid) & (appearances["player_id"]==playerid)]
    relclubid=rel["player_club_id"].values[0]
    gamerow=games.loc[games["game_id"]==gameid]
    gamescore=gamerow["home_club_goals"].values[0] - gamerow["away_club_goals"].values[0]
    if (gamerow["home_club_id"].values[0]!=relclubid):
        gamescore = gamescore * -1
    return(gamescore)
def teamcompalg(teamcode, oppcode):
    myTeam = clubs.loc[clubs["club_code"] == teamcode]
    print(myTeam["club_id"].values[0])
    myPlayers = players.loc[
        (players["current_club_id"] == myTeam["club_id"].values[0]) & (players["last_season"] == 2023)]
    myPlayerIds = myPlayers["player_id"].values
    print(myPlayerIds)
    overallteamsimilarity=0
    overallrelatedoutcome=0
    overallteampotencyscore=0
    countpl=0
    for i in myPlayerIds:
        # print(i)
        countpl = countpl + 1
        overallplayersimilarity=0
        overallpotencyscore=0
        playerAppearances = appearances.loc[appearances["player_id"] == i]
        # print(playerAppearances)
        for j in playerAppearances["game_id"].values:
            # print(j)
            gamePlayers = appearances.loc[appearances["game_id"] == j]
            # print(gamePlayers)
            currentPlayerAppearance = playerAppearances.loc[playerAppearances["game_id"] == j]
            myTeamThen = gamePlayers.loc[
                gamePlayers["player_club_id"] == currentPlayerAppearance["player_club_id"].values[0]]
            # theirTeamThen=gamePlayers.loc[gamePlayers["player_club_id"]!=currentPlayerAppearance["player_club_id"].values[0]]
            # teamSimilarity=
            #print("My Team Then")
            #print(np.count_nonzero(myTeamThen["player_current_club_id"] == myTeam["club_id"].values[0]))
            #print(np.count_nonzero(myTeamThen["player_current_club_id"] == myTeam["club_id"].values[0]) / np.count_nonzero(myTeamThen))
            overallplayersimilarity += (np.count_nonzero(myTeamThen["player_current_club_id"] == myTeam["club_id"].values[0]) / np.count_nonzero(myTeamThen))
            overallrelatedoutcome += ((np.count_nonzero(myTeamThen["player_current_club_id"] == myTeam["club_id"].values[0]) / np.count_nonzero(myTeamThen)))
            overallpotencyscore += ((np.count_nonzero(myTeamThen["player_current_club_id"] == myTeam["club_id"].values[0]) / np.count_nonzero(myTeamThen)))*outcomescorebyplayer(i, j)
            print(overallpotencyscore)
        overallteamsimilarity += overallplayersimilarity
        overallteampotencyscore += overallpotencyscore
        print("Count: "+str(countpl))
        print("Overall Player Similarity: " + str(overallplayersimilarity))
        print("Overall Team Similarity: "+str(overallteamsimilarity))
        print("Overall Team Potency " + str(overallteampotencyscore))
        #print("Adjusted Team Similarity: " + str(overallteamsimilarity / 25))



teamcompalg("fc-arsenal", "tottenham-hotspur")
#teamcompalg("tottenham-hotspur", "fc-arsenal")
#outcomescorebyplayer(112515,2698330)
