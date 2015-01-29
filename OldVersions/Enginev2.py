#3D Tetris Engine
#by Dimitry Raymond
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 100)

import pygame
import math
from random import randint

class Tetris(object):
	def __init__(self, width = 640, height = 640, caption = "Test with 3D boxes 2.0"):
		object.__init__(self)
		pygame.init()
		self.clock = pygame.time.Clock()
		self.setSpeed(5)
		self.setWidth(width)
		self.setHeight(height)
		self.initVariables()
		self.setScreen(self.getWidth(), self.getHeight())
		self.setCaption(caption)
		self.setBackground()
		self.drawRoom()
		self.background = self.saveBackground()
		self.resetCubes()
		pygame.display.flip()
		
	def initVariables(self):
		self.cubes = []
		self.colors = []
		
	def setWidth(self, width):
		self.width = width
		
	def getWidth(self):
		return self.width

	def setHeight(self, height):
		self.height = height

	def getHeight(self):
		return self.height
	
	def setScreen(self, width, height):
		self.screen = pygame.display.set_mode((width, height))

	def setCaption(self, caption):
		pygame.display.set_caption(caption)

	def setBackground(self):
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0, 0, 0))

	def setSpeed(self, speed):
		self.speed = speed

	def getDepthConstant(self):
		return 100 - (0.2540983606557377 * 100) * 2
		
	def drawRoom(self, rgb = (255, 255, 255), fade = True, fadeLevel = 3, smoothness = 32):
		depthPercent = 100 - self.getDepthConstant()
		depth = depthPercent / 200
		boxPoints = [[self.screen.get_width() * depth, self.screen.get_height() * depth], [self.screen.get_width() * (1 - depth), self.screen.get_height() * depth]
				, [self.screen.get_width() * (1 - depth), self.screen.get_height() * (1 - depth)], [self.screen.get_width() * depth, self.screen.get_height() * (1 - depth)]]
		if(fade):
			rInitial = rgb[0]
			gInitial = rgb[1]
			bInitial = rgb[2]
			rIncrement = (rInitial - rInitial / fadeLevel) / smoothness
			gIncrement = (gInitial - gInitial / fadeLevel) / smoothness
			bIncrement = (bInitial - bInitial / fadeLevel) / smoothness
			for i in range(smoothness):
				r = rInitial - rIncrement * i
				g = gInitial - gIncrement * i
				b = bInitial - bIncrement * i
				firstConstant = depth * i / smoothness
				secondConstant = depth * (i + 1) / smoothness
				pygame.draw.line(self.screen, (r, g, b), (self.screen.get_width() * firstConstant, self.screen.get_height() * firstConstant), (self.screen.get_width() * secondConstant, self.screen.get_height() * secondConstant))
				pygame.draw.line(self.screen, (r, g, b), (self.screen.get_width() - self.screen.get_width() * firstConstant, self.screen.get_height() * firstConstant), (self.screen.get_width() - self.screen.get_width() * secondConstant, self.screen.get_height() * secondConstant))
				pygame.draw.line(self.screen, (r, g, b), (self.screen.get_width() - self.screen.get_width() * firstConstant, self.screen.get_height() - self.screen.get_height() * firstConstant), (self.screen.get_width() - self.screen.get_width() * secondConstant, self.screen.get_height() - self.screen.get_height() * secondConstant))
				pygame.draw.line(self.screen, (r, g, b), (self.screen.get_width() * firstConstant, self.screen.get_height() - self.screen.get_height() * firstConstant), (self.screen.get_width() * secondConstant, self.screen.get_height() - self.screen.get_height() * secondConstant))
				pygame.draw.lines(self.screen, (r, g, b), True, boxPoints)
		else:
			pygame.draw.line(self.screen, rgb, (0,0), (self.screen.get_width() * depth, self.screen.get_height() * depth))
			pygame.draw.line(self.screen, rgb, (self.screen.get_width(),0), (self.screen.get_width() * (1 - depth), self.screen.get_height() * depth))
			pygame.draw.line(self.screen, rgb, (self.screen.get_width(), self.screen.get_height()), (self.screen.get_width() * (1 - depth), self.screen.get_height() * (1 - depth)))
			pygame.draw.line(self.screen, rgb, (0, self.screen.get_height()), (self.screen.get_width() * depth, self.screen.get_height() * (1 - depth)))
			pygame.draw.lines(self.screen, rgb, True, boxPoints)


	def saveBackground(self):
		currentScreen = pygame.display.get_surface()
		currentScreen = currentScreen.convert()
		self.background = currentScreen
		return currentScreen

	def loadBackground(self):
		return self.screen.blit(self.background, (0, 0))

	def addCube(self, xyzPoint, rgb = (255, 255, 255)):
		self.cubes[xyzPoint[0]][xyzPoint[1]][xyzPoint[2]] = 1
		self.colors[xyzPoint[0]][xyzPoint[1]][xyzPoint[2]] = ((rgb[0], rgb[1], rgb[2]))

	def removeCube(self, xyzPoint):
		self.cubes[xyzPoint[0]][xyzPoint[1]][xyzPoint[2]] = 0

	def resetCubes(self):
		self.cubes = [[[0 for i in range(32)] for j in range(32)] for k in range(32)]
		self.colors = [[[0 for i in range(32)] for j in range(32)] for k in range(32)]

	def flip(self, inverted = False):
		self.clock.tick(self.speed)
		self.loadBackground()
		self.loadCubes(inverted)
		pygame.display.flip()

	def loadCubes(self, inverted = False):
		#this 'inverted' has a neat effect
		if(inverted):
			a = 0
			b = 32
			c = 1
		else:
			a = 31
			b = -1
			c = -1
		#draw cubes in order so that they don't get overwritten by underlying cubes
		for k in range(a, b, c):
			for j in range(16):
				for i in range(16):
					if(self.cubes[i][j][k] == 1):
						self.drawCube([i, j, k], self.colors[i][j][k])
				for i in range(31, 15, -1):
					if(self.cubes[i][j][k] == 1):
						self.drawCube([i, j, k], self.colors[i][j][k])
			for j in range(31, 15, -1):
				for i in range(16):
					if(self.cubes[i][j][k] == 1):
						self.drawCube([i, j, k], self.colors[i][j][k])
				for i in range(31, 15, -1):
					if(self.cubes[i][j][k] == 1):
						self.drawCube([i, j, k], self.colors[i][j][k])
			       
			
	def drawQuadrilateral(self, fourEndpoints, rgb = (0, 0, 255)):
		r = rgb[0]
		g = rgb[1]
		b = rgb[2]
		border = (rgb[0]/3*2, rgb[1]/3*2, rgb[2]/3*2)
		
		xcoord1 = fourEndpoints[0]
		ycoord1 = fourEndpoints[1]
		xcoord2 = fourEndpoints[2]
		ycoord2 = fourEndpoints[3]
		xcoord3 = fourEndpoints[4]
		ycoord3 = fourEndpoints[5]
		xcoord4 = fourEndpoints[6]
		ycoord4 = fourEndpoints[7]
		pygame.draw.polygon(self.screen, (r, g, b), [[xcoord1, ycoord1], [xcoord2, ycoord2], [xcoord3, ycoord3], [xcoord4, ycoord4]], 0)
		pygame.draw.polygon(self.screen, (border[0], border[1], border[2]) , [[xcoord1, ycoord1], [xcoord2, ycoord2], [xcoord3, ycoord3], [xcoord4, ycoord4]], 1)

	def drawCube(self, xyzPoint, rgb = (255, 0, 0)):
		x = xyzPoint[0]
		y = xyzPoint[1]
		z = xyzPoint[2]

		#use trig functions to find points 
		origin = [self.getWidth() / 2, self.getHeight() / 2]
		boxSize = self.getWidth() / 32
		multiplier = 1
		shift = 30
		
		frontSizeRatio = 1/pow((z + shift), multiplier)
		frontSizeRatio = frontSizeRatio * shift 
		frontSize = boxSize * frontSizeRatio
		x1 = origin[0] + frontSize * (x - 16)
		x2 = x1 + frontSize
		y1 = origin[1] + frontSize * (y - 16)
		y2 = y1 + frontSize

		backSizeRatio = 1/pow((z + 1 + shift), multiplier)
		backSizeRatio = backSizeRatio * shift 
		backSize = boxSize * backSizeRatio
		i1 = origin[0] + backSize * (x - 16)
		i2 = i1 + backSize
		j1 = origin[1] + backSize * (y - 16)
		j2 = j1 + backSize
		
		#lower color based on distance
		rInitial = rgb[0]
		gInitial = rgb[1]
		bInitial = rgb[2]
		rIncrement = (rInitial - rInitial / 2) / 32
		gIncrement = (gInitial - gInitial / 2) / 32
		bIncrement = (bInitial - bInitial / 2) / 32

		r = rInitial - rIncrement * z
		g = gInitial - gIncrement * z
		b = bInitial - bIncrement * z
		rgb = (r, g, b)
		
		#Cube Face Coords
		backFace = [i1, j1, i2, j1, i2, j2, i1, j2]
		frontFace = [x1, y1, x2, y1, x2, y2, x1, y2]
		rightFace = [x2, y1, i2, j1, i2, j2, x2, y2]
		leftFace = [x1, y1, i1, j1, i1, j2, x1, y2]
		topFace = [x1, y1, i1, j1, i2, j1, x2, y1]
		bottomFace = [x2, y2, i2, j2, i1, j2, x1, y2]

		if(x <= 15):
			self.drawQuadrilateral(rightFace, rgb)
		elif(x >= 16):
			self.drawQuadrilateral(leftFace, rgb)
		else:
			print("couldnt draw right or left face")
			
		if(y <= 15):
			self.drawQuadrilateral(bottomFace, rgb)
		elif(y >= 16):
			self.drawQuadrilateral(topFace, rgb)
		else:
			print("Couldn't draw top or bottom faces")

		self.drawQuadrilateral(frontFace, rgb)

		if(x == 0 and y == 0 and z == 31):
			print(x1/self.getWidth())
		
	def runShowcase(self, num = 0):
		keepGoing = True
		self.i = 0
		self.j = 0
		self.k = 0
		while(keepGoing):
			if(num == 0):
				length = 1000
				for index in range(length):
					i = randint(0, 31)
					j = randint(0, 31)
					k = randint(0, 31)
					r = randint(0, 255)
					g = randint(0, 255)
					b = randint(0, 255)
					self.addCube([i, j, k], (r, g, b))
					
			if(num == 1):
				for j in range(32):
					for k in range(32):
						self.addCube([self.i, j, k])
				self.i += 1
				if(self.i > 31):
					self.i = 0

			if(num == 2):
				i = self.i
				j = 0
				k = 0
				tempI = self.i

				for z in range(tempI + 1):
					for i in range(tempI, -1, -1):
						self.addCube([i, j, k])
						i -= 1
						j += 1
					tempI -= 1
					j = 0
					k += 1
				
				
				self.i +=1
				if(self.i > 31):
					self.i = 0

			self.flip()
			self.resetCubes()
			self.clock.tick(20)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					#pygame.display.quit()
					#pygame.quit()
					keepGoing = False
					  

def main():
	game = Tetris()			
	game.runShowcase(2)

if(__name__) == "__main__":
	main()
