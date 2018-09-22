#Dillan Gajarawala, Section M, dgajaraw

"""This file contains the function that will read the accompanying csv files
and import them into the mongodb database"""
import os

def readFile(path): #taken from the 112 Website
	with open(path, "rt") as f:
		return f.read()

def getFileInfo(path):
	splitFileContents = []
	fileContents = readFile(path)
	for line in fileContents.splitlines():
		splitFileContents.append(line.split(","))
	return splitFileContents

def importPlayerData(content,database):
	for player in content:
		dataRow = {}
		dataRow["Team"] = player[1]
		dataRow["Number"] = int(player[2])
		dataRow["Name"] = player[3]
		dataRow["Position"] = player[4]
		dataRow["Age"] = int(player[5])
		dataRow["Experience"] = int(player[6])
		if dataRow["Position"] == "G":
			dataRow["Goals Against Average"] = float(player[7])
			database.players.insert_one(dataRow)
			continue
		dataRow["Goals"] = int(player[7])
		dataRow["Assists"] = int(player[8])
		database.players.insert_one(dataRow)

def importTeamData(content,database):
	for team in content:
		dataRow = {}
		dataRow["Conference"] = team[0]
		dataRow["Division"] = team[1]
		dataRow["Team"] = team[2]
		dataRow["Power Play Opportunities"] = team[3]
		dataRow["Power Play"] = team[4]
		dataRow["Penalty Kill"] = team[5]
		database.teams.insert_one(dataRow)

def inputPlayerData(database):
	for filename in os.listdir("PlayerData"):
		if "csv" in filename:
			path = "PlayerData" + "/" + filename
			fileInfo = getFileInfo(path)
			importPlayerData(fileInfo, database)

def inputTeamData(database):
	fileInfo = getFileInfo("TeamData.txt")
	importTeamData(fileInfo,database)

def createDatabase(database):
	if database.players.count() == 0:
		inputPlayerData(database)
	if database.teams.count() == 0:
		inputTeamData(database)