import random
import pygame, sys
from pygame.locals import *
from DecisionFactory3 import *

myDF = DecisionFactory()

#tile and color values
SPACE = 1
WALL = 2
PORTAL = 3
BLUE = (25, 25, 112)
RED = (139, 26, 26)
GOLD = (255, 215, 0)

#dimensions of board
TILESIZE = 40
#MAPWIDTH = 20
#MAPHEIGHT = 15
MAPWIDTH = 15
MAPHEIGHT = 10

#colors to distinguish tiles
colors = {
	SPACE : BLUE,
	PORTAL : GOLD,
	WALL : RED
	}

#create a grid
grid = []
for row in range(MAPWIDTH):
	grid.append([])
	for col in range(MAPHEIGHT):
		grid[row].append(SPACE)

#set the wall border
for y in range(0, MAPHEIGHT):
	grid[0][y] = WALL
	grid[MAPWIDTH-1][y] = WALL
for x in range(0, MAPWIDTH):
	grid[x][0] = WALL
	grid[x][MAPHEIGHT-1] = WALL

#place interior walls
for row in range(1, MAPWIDTH-1, 2):
	grid[row][MAPHEIGHT/2] = WALL
for col in range(1, MAPHEIGHT-1, 2):
	grid[MAPWIDTH/2][col] = WALL

#choose and set position for the portal
j = random.randint(1,MAPWIDTH-2)
k = random.randint(1,MAPHEIGHT-2)
while grid[j][k] == WALL:
	j = random.randint(1,MAPWIDTH-2)
	k = random.randint(1,MAPHEIGHT-2)
grid[j][k] = PORTAL

#initialize pygame and map
pygame.init()
DISPLAYMAP = pygame.display.set_mode((MAPWIDTH * TILESIZE, MAPHEIGHT * TILESIZE))

#create and place the player not in the same place as portal
PLAYERIMG = pygame.image.load('Decision Factory Project/person.jpg').convert_alpha()
q = random.randint(1,MAPWIDTH-2)
w = random.randint(1,MAPHEIGHT-2)
while(q == j and w == k):
	q = random.randint(1,MAPWIDTH-2)
	w = random.randint(1,MAPHEIGHT-2)
	#q = MAPWIDTH/2
	#W = MAPHEIGHT/2
playerCoord = [q,w]


#DTPL to play game
while True:
	#to quit after portal is found
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	#continue until portal is found
	while myDF.last_result != 'portal':
		#to exit in middle of run
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		#communicate with framework
		else:
			#get the decision from framework
			movement = myDF.get_decision()
				
			#print movement

			#evaluate the decision and determine correct move
			if movement == 'right':
				if grid[playerCoord[0] + 1][playerCoord[1]] == WALL:
					myDF.put_result('wall')
				elif grid[playerCoord[0] + 1][playerCoord[1]] == PORTAL:
					playerCoord[0] += 1
					myDF.put_result('portal')
				else:
					playerCoord[0] += 1
					myDF.put_result('success')
			if movement == 'left':
				if grid[playerCoord[0] - 1][playerCoord[1]] == WALL:
					myDF.put_result('wall')
				elif grid[playerCoord[0] - 1][playerCoord[1]] == PORTAL:
					playerCoord[0] -= 1
					myDF.put_result('portal')
				else:
					playerCoord[0] -= 1
					myDF.put_result('success')
			if movement == 'up':
				if grid[playerCoord[0]][playerCoord[1] - 1] == WALL:
					myDF.put_result('wall')
				elif grid[playerCoord[0]][playerCoord[1] - 1] == PORTAL:
					playerCoord[1] -= 1
					myDF.put_result('portal')
				else:
					playerCoord[1] -= 1
					myDF.put_result('success')
			if movement == 'down':
				if grid[playerCoord[0]][playerCoord[1] + 1] == WALL:
					myDF.put_result('wall')
				elif grid[playerCoord[0]][playerCoord[1] + 1] == PORTAL:
					playerCoord[1] += 1
					myDF.put_result('portal')
				else:
					playerCoord[1] += 1
					myDF.put_result('success')

			#print myDF.last_result
			if(myDF.last_result == 'portal'):
				print "finished in", myDF.num_moves, "moves"

		#draw map with updated movement
		for r in range(MAPHEIGHT):
			for c  in range(MAPWIDTH):
				pygame.draw.rect(DISPLAYMAP, colors[grid[c][r]], (c * TILESIZE,r * TILESIZE, TILESIZE, TILESIZE))

		#set new PLAYERIMG position
		DISPLAYMAP.blit(PLAYERIMG, (playerCoord[0] * TILESIZE, playerCoord[1] * TILESIZE))

		#update the display with new PLAYERIMG position
		pygame.display.update()

		#delay between moves for clear demonstration
		pygame.time.delay(100)