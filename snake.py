from Enginev3 import *
import pygame
from random import randint

class Snake(object):
	def __init__(self, players = 2, winLength = 15):
		object.__init__(self)
		self.setKeepGoing(True)
		self.setPlayerCount(players)
		self.definePlayerCoords()
		self.defineControls()
		self.setColors()
		self.setFood()
		self.setWinLength(winLength)

	def definePlayerCoords(self):
		self.playerLength = [5 for player in range(self.numOfPlayers)]
		self.playerPosition = [[[15 - i, int((32/(self.numOfPlayers + 1) * (player + 1) - 0.5)), 15] for i in range(self.playerLength[player])]
				       for player in range(self.numOfPlayers)]
		self.playerDirection = ["E" for player in range(self.numOfPlayers)]
		self.shadowTail = [[15 - self.playerLength[player], int((32/(self.numOfPlayers + 1) * (player + 1) - 0.5)), 15] for player in range(self.numOfPlayers)]
		
	def getEvents(self):
		for self.event in pygame.event.get():
			pass
		
	def defineControls(self):
		self.playerControls = [[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_PAGEUP, pygame.K_PAGEDOWN],
				       [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e],
				       [pygame.K_KP8, pygame.K_KP5, pygame.K_KP4, pygame.K_KP6, pygame.K_KP7, pygame.K_KP9],
				       [0, 0, 0, 0, 0, 0],
				       [0, 0, 0, 0, 0, 0],
				       [0, 0, 0, 0, 0, 0]
				       ]
	def setColors(self):
		self.playerColor = [[0 for i in range(self.playerLength[player])]for player in range(self.numOfPlayers)]
		self.playerColorGradient = [[255 - (64 / self.playerLength[player] * i) for i in range(self.playerLength[player])]
					    for player in range(self.numOfPlayers)]

		self.playerColor[0] = [(self.playerColorGradient[0][i], 0, 0) for i in range(self.playerLength[0])]
		if(self.numOfPlayers > 1):
			self.playerColor[1] = [(0, self.playerColorGradient[1][i], 0) for i in range(self.playerLength[1])]
			if(self.numOfPlayers > 2):
				self.playerColor[2] = [(0, 0, self.playerColorGradient[2][i]) for i in range(self.playerLength[2])]
				if(self.numOfPlayers > 3):
					self.playerColor[3] = [(self.playerColorGradient[3][i],
								self.playerColorGradient[3][i], 0) for i in range(self.playerLength[3])]
					if(self.numOfPlayers > 4):
						self.playerColor[4] = [(self.playerColorGradient[4][i], 0,
									self.playerColorGradient[4][i]) for i in range(self.playerLength[4])]
						if(self.numOfPlayers > 5):
							self.playerColor[5] = [(0, self.playerColorGradient[5][i],
										self.playerColorGradient[5][i]) for i in range(self.playerLength[5])]
	
	def setFood(self):
		self.foodPosition = [[randint(0, 31), randint(0, 31), randint(0, 31)] for player in range(self.numOfPlayers)]
		self.foodColor = [(0, 0, 0) for player in range(6)]
		self.foodColor[0] = (255, 0, 0)
		self.foodColor[1] = (0, 255, 0)
		self.foodColor[2] = (0, 0, 255)
		self.foodColor[3] = (255, 255, 0)
		self.foodColor[4] = (255, 0, 255)
		self.foodColor[5] = (0, 255, 255)
		
	def checkForQuit(self):
		if self.event.type == pygame.QUIT or (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_ESCAPE):
			self.setKeepGoing(False)
			print("User quit the game")

	def setPlayerCount(self, players):
		self.numOfPlayers = players
		
	def setDirection(self):
		if self.event.type == pygame.KEYDOWN:
			for player in range(self.numOfPlayers):
				if self.event.key == self.playerControls[player][0] and self.playerDirection[player] != "S":
					self.playerDirection[player] = "N"
				elif self.event.key == self.playerControls[player][1] and self.playerDirection[player] != "N":
					self.playerDirection[player] = "S"
				elif self.event.key == self.playerControls[player][2] and self.playerDirection[player] != "E":
					self.playerDirection[player] = "W"
				elif self.event.key == self.playerControls[player][3] and self.playerDirection[player] != "W":
					self.playerDirection[player] = "E"
				elif self.event.key == self.playerControls[player][4] and self.playerDirection[player] != "I":
					self.playerDirection[player] = "O"
				elif self.event.key == self.playerControls[player][5] and self.playerDirection[player] != "O":
					self.playerDirection[player] = "I"			

	def moveHead(self):
		for player in range(self.numOfPlayers):
			if self.playerDirection[player] == "E":
				self.playerPosition[player][0][0] += 1
			elif self.playerDirection[player] == "W":
				self.playerPosition[player][0][0] -= 1
			elif self.playerDirection[player] == "N":
				self.playerPosition[player][0][1] -= 1
			elif self.playerDirection[player] == "S":
				self.playerPosition[player][0][1] += 1
			elif self.playerDirection[player] == "I":
				self.playerPosition[player][0][2] += 1
			elif self.playerDirection[player] == "O":
				self.playerPosition[player][0][2] -= 1
			else:
				print("no direction for player ", player)
		
	def moveBody(self):
		for player in range(self.numOfPlayers):
			self.shadowTail[player] = self.playerPosition[player][self.playerLength[player] - 1]
			for i in range((self.playerLength[player] - 1), 0, -1):
				self.playerPosition[player][i] = [self.playerPosition[player][i - 1][0],
								  self.playerPosition[player][i - 1][1],
								  self.playerPosition[player][i - 1][2]]

	def checkBorders(self):
		for player in range(self.numOfPlayers):
			if self.playerPosition[player][0][0] < 0:
				self.playerPosition[player][0][0] = 31
			elif self.playerPosition[player][0][0] > 31:
				self.playerPosition[player][0][0] = 0
			elif self.playerPosition[player][0][1] < 0:
				self.playerPosition[player][0][1] = 31
			elif self.playerPosition[player][0][1] > 31:
				self.playerPosition[player][0][1] = 0
			elif self.playerPosition[player][0][2] < 0:
				self.playerPosition[player][0][2] = 31
			elif self.playerPosition[player][0][2] > 31:
				self.playerPosition[player][0][2] = 0

	def replaceFood(self, player):
		self.foodPosition[player] = [randint(0, 31), randint(0, 31), randint(0, 31)]

	def increaseSize(self, player):
		self.playerLength[player] += 1
		self.playerPosition[player].append(self.shadowTail[player])
		self.setColors()

	def checkForDinner(self):
		for player in range(self.numOfPlayers):
			if self.playerPosition[player][0] == self.foodPosition[player]:
				print(player, "ate his food")
				self.increaseSize(player)
				self.replaceFood(player)

	def checkForSteal(self):
		for playerA in range(self.numOfPlayers):
			for playerB in range(playerA + 1, self.numOfPlayers, 1):
				if self.playerPosition[playerA][0] == self.foodPosition[playerB]:
					self.increaseSize(playerA)
					self.replaceFood(playerB)
					print(playerA, " ate ", playerB, "'s food", sep = "")

	def checkForCollision(self):
		for playerA in range(self.numOfPlayers):
			for playerB in range(self.numOfPlayers):
				for i in range(1, self.playerLength[playerB], 1):
					if self.playerPosition[playerA][0] == self.playerPosition[playerB][i] and playerA != playerB:
						print(playerA, " ran into ", playerB, " at ", i, sep = "")
						self.setKeepGoing(False)
						
		for playerA in range(self.numOfPlayers):
			for playerB in range(playerA, self.numOfPlayers, 1):
				if self.playerPosition[playerA][0] == self.playerPosition[playerB][0] and playerA != playerB:
					print(playerA, " and ", playerB, " bumped heads.", sep = "")
					self.setKeepGoing(False)
				
	def setWinLength(self, winLength):
		self.winLength = winLength

	def getWinLength(self):
		return self.winLength

	def checkForWinCondition(self):
		for player in range(self.numOfPlayers):
			if self.playerLength[player] == self.getWinLength():
				print(player, "reached the winnning length")
				self.setKeepGoing(False)

	def setKeepGoing(self, bool):
		self.keepGoing = bool

	def getKeepGoing(self):
		return self.keepGoing

def main():	
	display = Tetris(caption = "Snake")
	display.setSpeed(20)
	game = Snake(players = 3, winLength = 7)
	game.getEvents()

	while(game.getKeepGoing()):
		game.getEvents()
		game.setDirection()
		game.moveBody()
		game.moveHead()
		game.checkBorders()
		game.checkForDinner()
		game.checkForSteal()
		game.checkForCollision()
		game.checkForWinCondition()
		game.checkForQuit()
	
		for player in range(game.numOfPlayers):
			for i in range(game.playerLength[player]):
				display.addCube(game.playerPosition[player][i], game.playerColor[player][i])
			display.addCube(game.foodPosition[player], game.foodColor[player])

		display.flip()
		display.resetCubes()
	
	display.quitPygame()

main()
