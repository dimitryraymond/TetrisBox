from Enginev1A import *
from random import *
class Snake(object):
	def __init__(self):
		object.__init__(self)
		self.setInitialVariables()

	def setInitialVariables(self):
		self.numOfPlayers = 2
		self.player1Length = 5
		self.player1Position = [[15 - i, 5, 0] for i in range(self.player1Length)]
		self.player1Direction = "E"
		self.player1Color = [(255 - (64 / self.player1Length) * i, 0, 0) for i in range(self.player1Length)]	

	def getEvents(self):
		for self.event in pygame.event.get():
			pass
		
	def checkForQuit(self):
		if self.event.type == pygame.QUIT or (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_ESCAPE):
			pygame.display.quit()
			pygame.quit()
			keepGoing = False
		else:
			keepGoing = True
		return keepGoing

	def setPlayerCount(self, players):
		self.numOfPlayers = players
		
	def setDirection(self):
		if self.event.type == pygame.KEYDOWN:
			if self.event.key == pygame.K_RIGHT and self.player1Direction != "W":
				self.player1Direction = "E"
			elif self.event.key == pygame.K_LEFT and self.player1Direction != "E":
				self.player1Direction = "W"
			elif self.event.key == pygame.K_UP and self.player1Direction != "S":
				self.player1Direction = "N"
			elif self.event.key == pygame.K_DOWN and self.player1Direction != "N":
				self.player1Direction = "S"
			elif self.event.key == pygame.K_PAGEUP and self.player1Direction != "I":
				self.player1Direction = "O"
			elif self.event.key == pygame.K_PAGEDOWN and self.player1Direction != "O":
				self.player1Direction = "I"

	def moveHead(self):
		if self.player1Direction == "E":
			self.player1Position[0][0] += 1
		elif self.player1Direction == "W":
			self.player1Position[0][0] -= 1
		elif self.player1Direction == "N":
			self.player1Position[0][1] -= 1
		elif self.player1Direction == "S":
			self.player1Position[0][1] += 1
		elif self.player1Direction == "I":
			self.player1Position[0][2] += 1
		elif self.player1Direction == "O":
			self.player1Position[0][2] -= 1
		else:
			print("no direction for player 1")
		
	def moveBody(self):
		for i in range((self.player1Length - 1), 0, -1):
			self.player1Position[i] = [self.player1Position[i - 1][0], self.player1Position[i - 1][1], self.player1Position[i - 1][2]]

	def checkBorders(self):
		if self.player1Position[0][0] < 0:
			self.player1Position[0][0] = 31
		elif self.player1Position[0][0] > 31:
			self.player1Position[0][0] = 0
		elif self.player1Position[0][1] < 0:
			self.player1Position[0][1] = 31
		elif self.player1Position[0][1] > 31:
			self.player1Position[0][1] = 0
		elif self.player1Position[0][2] < 0:
			self.player1Position[0][2] = 31
		elif self.player1Position[0][2] > 31:
			self.player1Position[0][2] = 0
	
display = Tetris()
display.setSpeed(20)
snake = Snake()

keepGoing = True
while(keepGoing):
	snake.getEvents()
	snake.setDirection()
	snake.moveBody()
	snake.moveHead()
	snake.checkBorders()
	
	for i in range(snake.player1Length):
		display.addCube(snake.player1Position[i], snake.player1Color[i])

	display.flip()
	display.resetCubes()
	
	keepGoing = snake.checkForQuit()
