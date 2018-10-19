# Dillan Gajarawala, Section M, dgajaraw

"""This file contains the run function that will actually execute the
program. There are several different modes/screens within the program."""

from pymongo import MongoClient
import importdata
import forecaster
from tkinter import *
import requests
import os

url = ('https://newsapi.org/v2/top-headlines?'
	   'sources=nhl-news&apiKey=2eb1c5b772e0418eac7b11b748c65297')

client = MongoClient()

nhl = client.test_db
nhl.players.delete_many({})

importdata.createDatabase(nhl)

def init(data):
	data.mode = "mainScreen"
	setPictures(data)
	setFilters(data)
	setPlayerStuff(data)
	setTeamStuff(data)
	data.viewY = 0
	data.scroll = data.height//10
	data.scroll2 = data.height//20
	data.scroll3 = data.height//30
	data.newsData = []
	setButtonStuff(data)
	setBackButtonStuff(data)
	setForecasterStuff(data)
	getAllTeams(nhl, data)
	getAllPlayers(nhl,data)
	setUpdateStuff(data)
	getAllLogos(data)
	setXPos(data)
	data.logo = None

def setFilters(data):
	data.conference = ""
	data.division = ""
	data.team = ""
	data.teams = []
	data.players = []

def setXPos(data):
	data.leftX = data.width//4
	data.rightX = 3*data.height//4

def setPictures(data):
	data.easternLogo = PhotoImage(file="images/eastern.gif")
	data.westernLogo = PhotoImage(file="images/western.gif")
	data.background = PhotoImage(file="images/mainview.gif")
	data.baseColor = PhotoImage(file="images/mainBackground.gif")

def setButtonStuff(data):
	offset = 200
	data.buttonOffset = (data.width - offset) // 10
	data.buttonX = data.width // 2
	button1Pos = 7
	button2Pos = 8
	data.button1Y = button1Pos * data.scroll
	data.button2Y = button2Pos * data.scroll
	data.buttonHeight = data.buttonOffset // 2
	data.buttonWidth = 2 * data.buttonOffset

def setBackButtonStuff(data):
	data.backButtonY = data.scroll//2
	data.backButtonHeight = data.buttonOffset // 3

def setForecasterStuff(data):
	data.homeTeam = ""
	data.awayTeam = ""
	data.homeTeamInput = True
	data.awayTeamInput = False
	data.homeTeamError = False
	data.awayTeamError = False
	data.winner = ""
	data.winnerPts = 0
	data.loserPts = 0

def setPlayerStuff(data):
	data.player = None
	data.playerName = ""
	data.number = None
	data.position = ""
	data.age = None
	data.experience = None
	data.goals = None
	data.assists = None
	data.goalsAgainst = None

def setTeamStuff(data):
	data.opportunities = 0
	data.powerPlay = 0
	data.penaltyKill = 0

def setUpdateStuff(data):
	data.entity = ""
	data.entityError = False
	data.updatePlayer = ""
	data.playerError = False
	data.updateTeam = ""
	data.teamError = False
	data.stat = ""
	data.playerStats = ["Team","Number","Name","Position","Age","Experience"]
	data.teamStats = ["Power Play", "Penalty Kill", "Power Play Opportunities"]
	data.statError = False
	data.updatedValue = ""
	data.valueError = False
	setUpdateInputValues(data)
	data.updated = False

def setUpdateInputValues(data):
	data.entityInput = True
	data.playerInput = False
	data.teamInput = False
	data.statInput = False
	data.valueInput = False


def getAllTeams(database, data):
	data.allTeams = set()
	for team in database.teams.find({}):
		data.allTeams.add(team["Team"])

def getAllPlayers(database,data):
	data.allPlayers = set()
	for player in database.players.find({}):
		data.allPlayers.add(player["Name"])

def getAllLogos(data):
	path = "images/logos"
	data.logos = dict()
	for filename in os.listdir(path):
		key = filename[:-4]
		data.logos[key] = path + "/" + filename

def mousePressed(event, data):
	if data.mode == "mainScreen": mainScreenMousePressed(event, data)
	elif data.mode == "conference": conferenceMousePressed(event, data)
	elif data.mode == "forecaster": forecasterMousePressed(event, data)
	elif data.mode == "division": divisionMousePressed(event, data, nhl)
	elif data.mode == "teamsScreen": teamsScreenMousePressed(event, data, nhl)
	elif data.mode == "playerScreen": playerScreenMousePressed(event, data)
	elif data.mode == "playerStats": playerStatsMousePressed(event,data)
	elif data.mode == "news": newsMousePressed(event,data)
	elif data.mode == "update": updateMousePressed(event,data)

def checkButtonXBounds(event, data):
	if event.x > data.buttonX - data.buttonWidth and event.x < data.buttonX \
			+ data.buttonWidth:
		return True

def checkMainButtonCol1XBounds(event,data):
	if event.x > data.leftX - data.buttonWidth and event.x<data.leftX \
			+ data.buttonWidth:
		return True

def checkMainButtonCol2XBounds(event,data):
	if event.x > data.rightX - data.buttonWidth and event.x < \
			data.rightX + data.buttonWidth:
		return True

def backButtonPressed(event, data):
	if checkButtonXBounds(event, data):
		if event.y > data.backButtonY - data.backButtonHeight and event.y < \
				data.backButtonY + data.backButtonHeight:
			return True
	return False

def keyPressed(event, data):
	if data.mode == "playerScreen":
		playerScreenKeyPressed(event, data)
	elif data.mode == "forecaster":
		forecasterKeyPressed(event, data, nhl)
	elif data.mode == "news":
		newsKeyPressed(event,data)
	elif data.mode == "update":
		updateKeyPressed(event,data,nhl)

def timerFired(data):
	pass

def createButton(canvas, x, y, height, width, message):
	canvas.create_rectangle(x-width,y-height,x+width,y+height,\
							outline="white")
	canvas.create_text(x, y, text=message, font="Helvetica 20", fill="white")

def redrawAll(canvas, data):
	if data.mode == "mainScreen": mainScreenRedrawAll(canvas, data)
	elif data.mode == "conference": conferenceRedrawAll(canvas, data)
	elif data.mode == "forecaster": forecasterRedrawAll(canvas, data)
	elif data.mode == "division": divisionRedrawAll(canvas, data)
	elif data.mode == "teamsScreen": teamsScreenRedrawAll(canvas, data)
	elif data.mode == "playerScreen": playerScreenRedrawAll(canvas, data)
	elif data.mode == "playerStats": playerStatsRedrawAll(canvas,data)
	elif data.mode == "news": newsRedrawAll(canvas,data)
	elif data.mode == "update": updateRedrawAll(canvas,data)

####################################
# mainScreen mode
####################################

def mainScreenMousePressed(event, data):
	if checkMainButtonCol1XBounds(event,data):
		if event.y > data.button1Y - data.buttonHeight and event.y < \
				data.button1Y + data.buttonHeight:
			data.mode = "conference"
		elif event.y > data.button2Y - data.buttonHeight and event.y < \
				data.button2Y + data.buttonHeight:
			data.mode = "update"
	elif checkMainButtonCol2XBounds(event,data):
		if event.y > data.button1Y - data.buttonHeight and event.y < \
				data.button1Y + data.buttonHeight:
			data.mode = "news"
			getNewsInfo(data)
		elif event.y > data.button2Y - data.buttonHeight and event.y < \
				data.button2Y + data.buttonHeight:
			data.mode = "forecaster"

def mainScreenRedrawAll(canvas, data):
	canvas.create_image(data.width//2,data.height//2,image=data.background)
	title = "The Interactive NHL Experience"
	canvas.create_text(data.width // 2, data.scroll, text=title, \
					   font="Helvetica 26", fill="white")
	button1 = "Player Database"
	button2 = "Update Database"
	button3 = "NHL News"
	button4 = "Game Forecaster"
	createButton(canvas, data.leftX, data.button1Y, data.buttonHeight, \
				 data.buttonWidth, button1)
	createButton(canvas, data.leftX, data.button2Y, data.buttonHeight, \
				 data.buttonWidth, button2)
	createButton(canvas, data.rightX, data.button1Y, data.buttonHeight, \
				 data.buttonWidth, button3)
	createButton(canvas,data.rightX,data.button2Y,data.buttonHeight, \
				 data.buttonWidth, button4)

####################################
# forecaster mode
####################################

def forecasterMousePressed(event, data):
	if backButtonPressed(event, data):
		data.mode = "mainScreen"
		setForecasterStuff(data)

def forecasterKeyPressed(event, data, database):
	if data.homeTeamInput and event.keysym == "Return":
		checkValidHomeTeam(data)
	elif data.homeTeamInput:
		addCharactersToHomeTeam(event, data)
	elif data.awayTeamInput and event.keysym == "Return":
		checkValidAwayTeam(data)
	elif data.awayTeamInput:
		addCharactersToAwayTeam(event, data)
	if not data.homeTeamInput and not data.awayTeamInput:
		data.winner, data.winnerPts, data.loserPts = \
			forecaster.basicAlgorithm(database, data.homeTeam, data.awayTeam)

def checkValidTeam(data, team):
	if team not in data.allTeams:
		return False
	return True

def checkValidHomeTeam(data):
	if not checkValidTeam(data, data.homeTeam):
		data.homeTeamError = True
		data.homeTeam = ""
	else:
		data.homeTeamInput = False
		data.awayTeamInput = True

def checkValidAwayTeam(data):
	if not checkValidTeam(data, data.awayTeam):
		data.awayTeamError = True
		data.awayTeam = ""
	else:
		data.awayTeamInput = False

def addCharactersToHomeTeam(event, data):
	if event.keysym.isalpha():
		if event.keysym == "space":
			data.homeTeam += " "
		elif event.keysym == "BackSpace":
			data.homeTeam = data.homeTeam[:-1]
		else:
			data.homeTeam += event.char

def addCharactersToAwayTeam(event, data):
	if event.keysym.isalpha():
		if event.keysym == "space":
			data.awayTeam += " "
		elif event.keysym == "BackSpace":
			data.awayTeam = data.awayTeam[:-1]
		else:
			data.awayTeam += event.keysym

def displayWinnerAndScore(canvas, data):
	if data.winner != "":
		if not data.winnerPts == data.loserPts:
			message = "Winner: " + data.winner
		else:
			message = "It's a Tie!"
		pos = 5
		canvas.create_text(data.width//2,pos*data.scroll,text=message, \
						   font="Helvetica 24", fill="white")
		pos = 6
		score = "Score: " + str(data.winnerPts) + " - " + str(data.loserPts)
		canvas.create_text(data.width//2,pos*data.scroll,text=score, \
						   font="Helvetica 20", fill="white")

def showPrompts(canvas, data):
	if data.homeTeamInput:
		if data.homeTeamError:
			command = "You have entered an invalid team.\nEnter a valid" + \
					  " team and Press ENTER when done."
		else:
			command="Please enter the desired Home Team.\nPress ENTER when"+\
					  " done."
		pos = 4
		canvas.create_text(data.width//2,pos*data.scroll2,text=command,
						   justify=CENTER, fill="white")
	elif data.awayTeamInput:
		if data.awayTeamError:
			command = "You have entered an invalid team.\nEnter a valid" + \
					  " team and Press ENTER when done."
		else:
			command="Please enter the desired Away Team.\nPress ENTER when"+\
					  " done."
		pos = 6
		canvas.create_text(data.width//2,pos*data.scroll2,text=command,
						   justify=CENTER, fill="white")

def displayUserPrompts(canvas, data):
	homeTeam = "Home Team: " + data.homeTeam
	awayTeam = "Away Team: " + data.awayTeam
	showPrompts(canvas, data)
	pos = 5
	canvas.create_text(data.width // 2, pos * data.scroll2,text=homeTeam, \
					   font="Helvetica 16", fill="white")
	pos = 7
	canvas.create_text(data.width // 2, pos * data.scroll2,text=awayTeam, \
					   font="Helvetica 16", fill="white")

def forecasterRedrawAll(canvas, data):
	canvas.create_image(data.width//2,data.height//2,image=data.baseColor)
	title = "Game Forecaster"
	canvas.create_text(data.width // 2, data.scroll, text=title, \
					   font="Helvetica 26", fill="white")
	createButton(canvas,data.buttonX,data.backButtonY,data.backButtonHeight, \
				 data.buttonWidth, "Back")
	displayUserPrompts(canvas, data)
	displayWinnerAndScore(canvas, data)

####################################
# news mode
####################################

def newsMousePressed(event,data):
	if backButtonPressed(event, data):
		data.mode = "mainScreen"
		data.viewY = 0
		data.newsData = []

def newsKeyPressed(event, data):
	offset = 3
	maxNews = len(data.newsData)-1
	maxNewsCoord = (2 + maxNews) * offset + (maxNews*offset)
	maxNewsY = (maxNewsCoord+2)*data.scroll3
	if event.keysym == "Up" and data.viewY > 0:
		data.viewY -= data.scroll
	elif event.keysym == "Down" and data.viewY + data.height < maxNewsY:
		data.viewY += data.scroll

def getNewsInfo(data):
	response = requests.get(url)
	newsData = response.json()
	for article in newsData["articles"]:
		info = dict()
		info["title"] = article["title"]
		info["link"] = article["url"]
		data.newsData.append(info)

def drawNewsData(canvas,data):
	offset = 3
	for i in range(len(data.newsData)):
		title = data.newsData[i]["title"]
		link = "URL: " + data.newsData[i]["link"]
		coord = (2 + i) * offset + (i*offset)
		titlePos = coord * data.scroll3
		urlPos = (coord + 1) * data.scroll3
		canvas.create_text(data.width//2,titlePos-data.viewY, text=title, fill="white")
		canvas.create_text(data.width//2,urlPos-data.viewY,text=link, fill="white")

def newsRedrawAll(canvas,data):
	canvas.create_image(data.width//2,data.height//2,image=data.baseColor)
	title = "NHL News"
	canvas.create_text(data.width//2,data.scroll-data.viewY, text=title, \
					   font="Helvetica 26", fill="white")
	createButton(canvas, data.buttonX,data.backButtonY-data.viewY,
				 data.backButtonHeight,data.buttonWidth, "Back")
	drawNewsData(canvas,data)

####################################
# update mode
####################################

def updateMousePressed(event,data):
	if backButtonPressed(event, data):
		data.mode = "mainScreen"
		setUpdateStuff(data)

def updateKeyPressed(event,data,database):
	if data.entityInput and event.keysym == "Return":
		checkValidEntity(data)
	elif data.entityInput:
		addCharactersToEntity(event,data)
	elif data.teamInput and event.keysym == "Return":
		checkValidUpdatedTeam(data)
	elif data.teamInput:
		addCharactersToTeam(event,data)
	elif data.playerInput and event.keysym == "Return":
		checkValidPlayer(data,database)
	elif data.playerInput:
		addCharactersToPlayer(event,data)
	elif data.statInput and event.keysym == "Return":
		checkValidStat(data)
	elif data.statInput:
		addCharactersToStat(event,data)
	elif data.valueInput and event.keysym == "Return":
		checkValidValue(data,database)
		if not data.valueError:
			updateDatabase(data,database)
	elif data.valueInput:
		addCharactersToValue(event,data)

def updateDatabase(data,database):
	if data.entity == "Player":
		database.players.update_one({"Name":data.updatePlayer}, \
					{"$set": {data.stat: data.updatedValue}})
	elif data.entity == "Team":
		database.teams.update_one({"Team":data.updateTeam},\
					{"$set": {data.stat: data.updatedValue}})
	data.updated = True

def addCharactersToEntity(event,data):
	if event.keysym.isalpha():
		if event.keysym == "space":
			data.entity += " "
		elif event.keysym == "BackSpace":
			data.entity = data.entity[:-1]
		else:
			data.entity += event.char

def addCharactersToTeam(event,data):
	if event.keysym.isalpha():
		if event.keysym == "space":
			data.updateTeam += " "
		elif event.keysym == "BackSpace":
			data.updateTeam = data.updateTeam[:-1]
		else:
			data.updateTeam += event.char

def addCharactersToPlayer(event,data):
	if event.keysym.isalpha():
		if event.keysym == "space":
			data.updatePlayer += " "
		elif event.keysym == "BackSpace":
			data.updatePlayer = data.updatePlayer[:-1]
		else:
			data.updatePlayer += event.char

def addCharactersToStat(event,data):
	if event.keysym.isalpha():
		if event.keysym == "space":
			data.stat += " "
		elif event.keysym == "BackSpace":
			data.stat = data.stat[:-1]
		else:
			data.stat += event.char

def addCharactersToValue(event,data):
	if event.keysym == "space":
		data.updatedValue += " "
	elif event.keysym == "BackSpace":
		data.updatedValue = data.updatedValue[:-1]
	else:
		data.updatedValue += event.char

def checkValidEntity(data):
	if data.entity != "Player" and data.entity != "Team":
		data.entityError = True
		data.entity = ""
	else:
		data.entityInput = False
		if data.entity == "Team":
			data.teamInput = True
		else:
			data.playerInput = True

def checkValidUpdatedTeam(data):
	if data.updateTeam not in data.allTeams:
		data.teamError = True
		data.updateTeam = ""
	else:
		data.teamInput = False
		data.statInput = True

def checkValidPlayer(data,database):
	if data.updatePlayer not in data.allPlayers:
		data.playerError = True
		data.updatePlayer = ""
	else:
		data.playerInput = False
		data.statInput = True
		addExtraStats(data,database)

def addExtraStats(data,database):
	for player in database.players.find({"Name":data.updatePlayer}):
		if player["Position"] == "G":
			data.playerStats.append("Goals Against Average")
		else:
			data.playerStats.append("Goals")
			data.playerStats.append("Assists")

def checkValidStat(data):
	if data.entity == "Team":
		if data.stat not in data.teamStats:
			data.statError = True
			data.stat = ""
		else:
			data.statInput = False
			data.valueInput = True
	else:
		if data.stat not in data.playerStats:
			data.statError = True
			data.stat = ""
		else:
			data.statInput = False
			data.valueInput = True

def checkValidValue(data,database):
	if data.entity == "Player":
		checkValidPlayerValue(data)
	elif data.entity == "Team":
		checkValidTeamValue(data,database)

def checkValidTeamValue(data,database):
	hundred = 100
	getTeamStuff(data,database)
	notInt = data.updatedValue.isdigit() == False
	greaterThanHundred = (data.stat == "Power Play" or \
	data.stat == "Penalty Kill") and int(data.updatedValue) >= hundred
	if notInt or greaterThanHundred:
		data.valueError = True
		data.updatedValue = ""


def checkValidPlayerValue(data):
	for player in nhl.players.find({"Name":data.updatePlayer}):
		age = player["Age"]
	positions = {"C","LW","RW","D","G"}
	intValues = {"Age","Number","Experience","Goals","Assists"}
	strValues = {"Name", "Team", "Position"}
	a = data.stat in intValues and data.updatedValue.isdigit() == False
	b = data.stat in strValues and data.updatedValue.isalpha() == False
	c = data.stat == "Position" and data.updatedValue not in positions
	d = data.stat == "Goals Against Average" and "." not in data.updatedValue
	e = data.stat == "Experience" and data.updatedValue >= age
	if a or b or c or d or e:
		data.valueError = True
		data.updatedValue = ""

def displayPlayerInputPrompts(canvas,data):
	if data.entity == "Player" and \
			(data.playerInput or len(data.updatePlayer) > 1):
		if not data.playerError:
			prompt = "Enter the player to be Updated\n" \
					 "If the player is a captain, add a '(C)'"
		else:
			prompt = "Invalid Player. Enter a valid Player Name"
		pos = 3
		canvas.create_text(data.width//2,pos*data.scroll,text=prompt,
						fill="white", font="Helvetica 18",justify=CENTER)
		pos = 7
		canvas.create_text(data.width // 2, pos * data.scroll2, \
					   text="Player: " + data.updatePlayer, fill="white")

def displayTeamInputPrompts(canvas,data):
	if data.entity == "Team" and (data.teamInput or len(data.updateTeam) > 1):
		if not data.teamError:
			prompt = "Enter the Team to be Updated"
		else:
			prompt = "Invalid Team. Enter a valid Team Name"
		pos = 3
		canvas.create_text(data.width//2,pos*data.scroll,text=prompt,
							   fill="white", font="Helvetica 18")
		pos = 7
		canvas.create_text(data.width // 2, pos * data.scroll2, \
						   text="Team: " + data.updateTeam, fill="white")

def displayEntityInputPrompts(canvas,data):
	if not data.entityError:
		prompt = "Do you want to update a Player or Team?"
	else:
		prompt = "Invalid Entry. Enter either 'Team' or 'Player'"
	canvas.create_text(data.width//2,2*data.scroll,text=prompt,
						   fill="white", font="Helvetica 18")
	pos = 5
	canvas.create_text(data.width // 2, pos * data.scroll2, \
	text="I want to update a: " + data.entity, fill="white")

def displayStatInputPrompts(canvas,data):
	if data.statInput or len(data.stat) > 1:
		if data.entity == "Team":
			displayTeamStatInputPrompts(canvas,data)
		else:
			displayPlayerStatInputPrompts(canvas,data)
		pos = 9
		canvas.create_text(data.width//2,pos*data.scroll2,\
						   text="Statistic: " + data.stat,fill="white")

def getTeamStatsPrompt(data):
	prompt = "Choose from "
	for i in range(len(data.teamStats)):
		if i == len(data.teamStats) - 1:
			prompt += ("and " + data.teamStats[i])
		else:
			prompt += data.teamStats[i] + ", "
	return prompt

def displayTeamStatInputPrompts(canvas,data):
	statsPrompt = getTeamStatsPrompt(data)
	if not data.statError:
		prompt = "Enter the Statistic to be Updated\n"
		prompt += statsPrompt
	else:
		prompt = "Invalid Statistic.\n"
		prompt += statsPrompt
	pos = 4
	canvas.create_text(data.width//2,pos*data.scroll,text=prompt, \
					   fill="white", justify=CENTER, font="Helvetica 18")

def getPlayerStatsPrompt(data):
	prompt = "Choose from "
	for i in range(len(data.playerStats)):
		if i == len(data.playerStats)-1:
			prompt += ("and " + data.playerStats[i])
		else:
			prompt += data.playerStats[i] + ", "
	return prompt

def displayPlayerStatInputPrompts(canvas,data):
	statsPrompt = getPlayerStatsPrompt(data)
	if not data.statError:
		prompt = "Enter the Statistic to be Updated\n"
		prompt += statsPrompt
	else:
		prompt = "Invalid Statistic.\n"
		prompt += statsPrompt
	pos = 4
	canvas.create_text(data.width // 2, pos * data.scroll, text=prompt, \
					   fill="white", justify=CENTER, font="Helvetica 18")

def displayValueInputPrompts(canvas,data):
	if data.valueInput or len(data.updatedValue) > 1:
		if not data.valueError:
			prompt = "Enter the new value for " + data.stat
		else:
			prompt = "Invalid Value. Enter the value for " + data.stat
		pos = 5
		canvas.create_text(data.width//2,pos*data.scroll,text=prompt,\
						   fill="white",font="Helvetica 18")
		pos = 11
		canvas.create_text(data.width//2,pos*data.scroll2,\
						   text="Value: " + data.updatedValue,fill="white")


def displayUpdatePrompts(canvas,data):
	displayEntityInputPrompts(canvas,data)
	displayTeamInputPrompts(canvas,data)
	displayPlayerInputPrompts(canvas,data)
	displayStatInputPrompts(canvas,data)
	displayValueInputPrompts(canvas,data)


def updateRedrawAll(canvas,data):
	canvas.create_image(data.width//2,data.height//2,image=data.baseColor)
	title = "Update the Database"
	canvas.create_text(data.width//2,data.scroll,text=title, \
					   font="Helvetica 26", fill="white")
	createButton(canvas,data.buttonX,data.backButtonY,data.backButtonHeight, \
				 data.buttonWidth, "Back")
	if not data.updated:
		displayUpdatePrompts(canvas,data)
	else:
		if data.entity == "Player":
			msg = data.updatePlayer + " has been updated"
		else:
			msg = "The " + data.updateTeam + " have been updated"
		pos = 5
		canvas.create_text(data.width//2,pos*data.scroll,text=msg,\
						fill="white",font="Helvetica 22")

####################################
# conference mode
####################################

def conferenceMousePressed(event, data):
	if checkButtonXBounds(event, data):
		if event.y > data.button1Y - data.buttonHeight and event.y < \
				data.button1Y + data.buttonHeight:
			data.conference = "Eastern"
			data.mode = "division"
		elif event.y > data.button2Y - data.buttonHeight and event.y < \
				data.button2Y + data.buttonHeight:
			data.conference = "Western"
			data.mode = "division"
	if backButtonPressed(event, data):
		data.mode = "mainScreen"

def conferenceRedrawAll(canvas, data):
	canvas.create_image(data.width//2,data.height//2,image=data.background)
	title = "Choose NHL Conference"
	canvas.create_text(data.width // 2, data.scroll, text=title, \
					   font="Helvetica 26", fill="white")
	button1 = "Eastern Conference"
	button2 = "Western Conference"
	createButton(canvas, data.buttonX, data.button1Y, data.buttonHeight, \
				 data.buttonWidth, button1)
	createButton(canvas, data.buttonX, data.button2Y, data.buttonHeight, \
				 data.buttonWidth, button2)
	createButton(canvas,data.buttonX,data.backButtonY,data.backButtonHeight, \
				 data.buttonWidth, "Back")

####################################
# division mode
####################################

def divisionMousePressed(event, data, database):
	if checkButtonXBounds(event, data):
		if event.y > data.button1Y - data.buttonHeight and event.y < \
				data.button1Y + data.buttonHeight:
			if data.conference == "Eastern":
				data.division = "Atlantic"
			else:
				data.division = "Central"
			data.mode = "teamsScreen"
			getTeams(database, data)
		elif event.y > data.button2Y - data.buttonHeight and event.y < \
				data.button2Y + data.buttonHeight:
			if data.conference == "Eastern":
				data.division = "Metropolitan"
			else:
				data.division = "Pacific"
			data.mode = "teamsScreen"
			getTeams(database, data)
	if backButtonPressed(event, data):
		data.mode = "conference"

def drawConferenceImages(canvas, data):
	if data.conference == "Eastern":
		button1 = "Atlantic"
		button2 = "Metropolitan"
		canvas.create_image(data.width//2,data.height//2, \
							image=data.easternLogo)
	else:
		button1 = "Central"
		button2 = "Pacific"
		canvas.create_image(data.width//2,data.height//2, \
							image=data.westernLogo)
	return button1,button2

def divisionRedrawAll(canvas, data):
	button1, button2 = drawConferenceImages(canvas, data)
	title = "Choose " + data.conference + " Conference Division"
	canvas.create_text(data.width // 2, data.scroll, text=title, \
					   font="Helvetica 26",fill="white")
	createButton(canvas, data.buttonX, data.button1Y, data.buttonHeight, \
				 data.buttonWidth, button1)
	createButton(canvas, data.buttonX, data.button2Y, data.buttonHeight, \
				 data.buttonWidth, button2)
	createButton(canvas,data.buttonX,data.backButtonY,data.backButtonHeight, \
				 data.buttonWidth, "Back")

####################################
# teamsScreen mode
####################################

def teamsScreenMousePressed(event, data, database):
	if backButtonPressed(event, data):
		data.mode = "division"
		data.teams = []
	for i in range(len(data.teams)):
		buttonY = 2 * data.scroll + i * data.scroll
		if checkButtonXBounds(event, data):
			if event.y > buttonY - data.backButtonHeight and event.y < \
					buttonY + data.backButtonHeight:
				data.mode = "playerScreen"
				data.team = data.teams[i]
				getPlayers(database, data)
				getTeamStuff(data,database)
				data.logo = PhotoImage(file=data.logos[data.team])


def getTeams(database, data):
	for row in database.teams.find({"Division": data.division}):
		data.teams.append(row["Team"])

def teamsScreenRedrawAll(canvas, data):
	canvas.create_image(data.width//2,data.height//2,image=data.baseColor)
	title = "Choose " + data.division + " Division Team"
	canvas.create_text(data.width // 2, data.scroll, text=title, \
					   font="Helvetica 26",fill="white")
	createButton(canvas,data.buttonX,data.backButtonY,data.backButtonHeight, \
				 data.buttonWidth, "Back")
	for i in range(len(data.teams)):
		buttonY = 2 * data.scroll + i * data.scroll
		createButton(canvas, data.buttonX, buttonY, data.backButtonHeight, \
					 data.buttonWidth, data.teams[i])

####################################
# playerScreen mode
####################################

def playerScreenMousePressed(event, data):
	if backButtonPressed(event, data):
		data.mode = "teamsScreen"
		data.team = ""
		data.players = []
	for i in range(len(data.players)):
		offset = 4
		playerY = offset * data.scroll + i * data.scroll
		if checkButtonXBounds(event, data):
			if event.y > playerY-data.viewY - data.backButtonHeight and \
				event.y < playerY-data.viewY + data.backButtonHeight:
				data.mode = "playerStats"
				data.player = data.players[i]
				getPlayerStuff(data)

def getPlayerStuff(data):
	data.playerName = data.player["Name"]
	data.number = data.player["Number"]
	data.position = data.player["Position"]
	data.age = data.player["Age"]
	data.experience = data.player["Experience"]
	if data.position == "G":
		data.goalsAgainst = data.player["Goals Against Average"]
	else:
		data.goals = data.player["Goals"]
		data.assists = data.player["Assists"]

def getTeamStuff(data,database):
	for team in database.teams.find({"Team":data.team}):
		data.opportunities = team["Power Play Opportunities"]
		data.powerPlay = team["Power Play"]
		data.penaltyKill = team["Penalty Kill"]

def playerScreenKeyPressed(event, data):
	maxPlayerY = 4*data.scroll + (len(data.players)-1)*data.scroll
	if event.keysym == "Up" and data.viewY > 0:
		data.viewY -= data.scroll
	elif event.keysym == "Down" and (data.viewY + data.height) \
			< maxPlayerY + data.backButtonHeight:
		data.viewY += data.scroll

def getPlayers(database, data):
	for row in database.players.find({"Team": data.team}):
		data.players.append(row)


def playerScreenRedrawAll(canvas, data):
	canvas.create_image(data.width//2,data.height//2,image=data.baseColor)
	title = data.team
	canvas.create_text(data.width//2,data.scroll-data.viewY,text=title, \
					   font="Helvetica 26",fill="white")
	createButton(canvas, data.buttonX, data.backButtonY - data.viewY, \
				 data.backButtonHeight, data.buttonWidth, "Back")
	powerPlayText = "Power Play: " + data.powerPlay + "%"
	penaltyKillText = "Penalty Kill:  " + data.penaltyKill + "%"
	canvas.create_text(data.leftX, 2 * data.scroll - data.viewY, \
					   text=powerPlayText, fill="white", font="Helvetica 18")
	canvas.create_text(data.rightX,2*data.scroll-data.viewY,\
					   text=penaltyKillText,fill="white",font="Helvetica 18")
	pos = 3
	canvas.create_text(data.width//2,pos*data.scroll-data.viewY,\
					   text="Players",fill="white",font="Helvetica 18")
	for player in data.players:
		index = data.players.index(player)
		offset = 4
		playerY = offset * data.scroll + index * data.scroll
		createButton(canvas,data.buttonX,playerY-data.viewY,
		data.backButtonHeight,data.buttonWidth,player["Name"])

####################################
# playerStats mode
####################################

def playerStatsMousePressed(event,data):
	if backButtonPressed(event, data):
		setPlayerStuff(data)
		data.mode = "playerScreen"
		data.viewY = 0

def drawStats(canvas,data):
	pos = 3
	canvas.create_text(data.leftX,2*data.scroll,fill="white",
	text="Age: " +str(data.player["Age"]),font="Helvetica 20")
	canvas.create_text(data.rightX,2*data.scroll,fill="white",
	text="No: " + str(data.player["Number"]),font="Helvetica 20")
	canvas.create_text(data.leftX,pos*data.scroll,fill="white",
	text="Position: " + data.player["Position"],font="Helvetica 20")
	canvas.create_text(data.rightX,pos*data.scroll,fill="white",
	text="Experience: " + str(data.player["Experience"]) + " Years",
					   font="Helvetica 20")
	pos = 4
	if data.player["Position"] == "G":
		canvas.create_text(data.width//2,pos*data.scroll,fill="white",
		text="Goals Against Average: " + \
		str(data.player["Goals Against Average"]),font="Helvetica 20")
	else:
		canvas.create_text(data.leftX,pos*data.scroll,fill="white",
		text="Goals: " + str(data.player["Goals"]), font="Helvetica 20")
		canvas.create_text(data.rightX,pos*data.scroll,fill="white",
		text="Assists: " + str(data.player["Assists"]),font="Helvetica 20")

def playerStatsRedrawAll(canvas,data):
	canvas.create_image(data.width//2,data.height//2,image=data.baseColor)
	title = data.player["Name"] + " Statistics"
	canvas.create_text(data.width//2,data.scroll,text=title, \
					   font="Helvetica 26",fill="white")
	createButton(canvas, data.buttonX, data.backButtonY, \
				 data.backButtonHeight, data.buttonWidth, "Back")
	drawStats(canvas,data)
	canvas.create_image(data.width//2,data.button1Y,image=data.logo)

####################################
# Run function
####################################

def run(width=300, height=300):  # taken from the 112 Website
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

	# Set up data and call init
	class Struct(object): pass

	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100  # milliseconds
	root = Tk()
	init(data)
	# create the root and the canvas
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
	mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
	keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(800, 800)
