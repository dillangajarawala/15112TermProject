#Dillan Gajarawala, Section M, dgajaraw

"""This file contains the forecasting algorithm that will be used to predict
the winner of a hypothetical game and the score."""

import random

def sumPlayerInfo(database,team,home=False):
    totalPoints = 0
    goalsAllowed = 0
    numGoalies = 0
    for player in database.players.find({"Team": team}):
        if player["Position"] != "G":
            totalPoints += player["Goals"]
        else:
            numGoalies += 1
            goalsAllowed += player["Goals Against Average"]
    goalsAllowed = goalsAllowed/numGoalies
    if home == True:
        homePoints = 25
        totalPoints += homePoints
    numGames = 82
    avgPoints = totalPoints/numGames
    return avgPoints - goalsAllowed

def basicAlgorithm(database,team1,team2):
    team1Pts = sumPlayerInfo(database,team1,True)
    team2Pts = sumPlayerInfo(database,team2)
    if team1Pts > team2Pts:
        winner = team1
        loser = team2
        winnerPts = team1Pts
        loserPts = team2Pts
    elif team2Pts > team1Pts:
        winner = team2
        loser = team1
        winnerPts = team2Pts
        loserPts = team1Pts
    else:
        winner,loser,winnerPts,loserPts = ifPtsEqual(team1Pts,team2Pts,team1,team2)
    winnerPts,loserPts = getScore(winnerPts,loserPts,database,winner,loser)
    return winner,int(winnerPts),int(loserPts)

def ifPtsEqual(team1Points,team2Points,team1,team2):
    half = 50
    if percentChance(half) == False:
        winner = team1
        loser = team2
        winnerPts = team1Points
        loserPts = team2Points
    else:
        winner = team2
        loser = team1
        winnerPts = team2Points
        loserPts = team1Points
    return (winner,loser,winnerPts,loserPts)

def percentChance(percent):
    maxPercentage = 99
    chance = random.randint(0, maxPercentage)
    if chance > percent:
        return False
    return True

def getScore(winnerPts,loserPts,database,winner,loser):
    while winnerPts < 0 or loserPts < 0:
        winnerPts += 1
        loserPts += 1
    baseWinnerScore = winnerPts//loserPts
    if baseWinnerScore >= 10:
        baseWinnerScore //= 10
    baseLoserScore = 0
    normalWinnerPts = round(winnerPts*100)
    normalLoserPts = round(loserPts*100)
    offset = gcd(normalWinnerPts,normalLoserPts)
    half = 50
    if percentChance(half):
        baseWinnerScore += offset
        baseLoserScore += offset
    winnerScore,loserScore = powerPlayGoals(baseWinnerScore,baseLoserScore,\
                                        database,winner,loser)
    return winnerScore,loserScore

def getTeamStats(database,team):
    for team in database.teams.find({"Team": team}):
        teamPPO = int(team["Power Play Opportunities"])
        teamPP = int(team["Power Play"])
        teamPK = int(team["Penalty Kill"])
    return teamPPO,teamPP,teamPK


def powerPlayGoals(winnerScore,loserScore,database,winner,loser):
    winnerPPO,winnerPP,winnerPK = getTeamStats(database,winner)
    loserPPO, loserPP, loserPK = getTeamStats(database, loser)
    if winnerPPO > loserPPO:
        powerPlay = winner
    elif loserPPO > winnerPPO:
        powerPlay = loser
    else:
        half = 50
        if percentChance(half): powerPlay = winner
        else: powerPlay = loser
    if powerPlay == winner:
        if percentChance(winnerPP) and not percentChance(loserPK):
            winnerScore += 1
    elif powerPlay == loser:
        if percentChance(loserPP) and not percentChance(winnerPK):
            loserScore += 1
    return winnerScore,loserScore

def gcd(x, y): #taken from the 112 Website
    if (y == 0):
        return x
    else:
        return gcd(y, x % y)