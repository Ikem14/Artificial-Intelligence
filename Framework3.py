import random
import pygame, sys
from pygame.locals import *
from FinalDF import *
#from DecisionFactory3 import *

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
MAPWIDTH = 10
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
#for row in range(1, MAPWIDTH-1, 2):
#	grid[row][MAPHEIGHT/2] = WALL
#for col in range(1, MAPHEIGHT-1, 2):
#	grid[MAPWIDTH/2][col] = WALL

grid[5][1] = WALL
grid[5][2] = WALL
grid[5][3] = WALL
grid[5][4] = WALL
grid[5][5] = WALL
grid[5][8] = WALL
grid[5][7] = WALL
grid[6][5] = WALL
grid[7][5] = WALL
grid[7][4] = WALL
grid[7][3] = WALL
grid[7][2] = WALL
grid[1][2] = WALL
grid[2][2] = WALL
grid[2][2] = WALL
grid[2][3] = WALL
grid[2][4] = WALL
grid[2][5] = WALL


#choose and set position for the portal
#j = random.randint(1,MAPWIDTH-2)
#k = random.randint(1,MAPHEIGHT-2)
j=8
k=8
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
#while(q == j and w == k):
#	q = random.randint(1,MAPWIDTH-2)
#	w = random.randint(1,MAPHEIGHT-2)
q=1
w=1
playerCoord = [q,w]
#up,  down, left, right, down and right, up and left, up and right , down and left
playerSur = ['0','0','0','0','0','0','0','0'] #player surrounding

#change the value in the playerSur string array
def change_playerSur(index, val):
	temp[index] = val
	playerSur[playerCoord[1]][playerCoord[0]] = "".join(temp)

#print "starting position: ", playerCoord

#DTPL to play game
while True:
	#to quit after portal is found
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	while(myDF.num_rounds < 3):
		playerCoord = [q,w]
		myDF.last_result = 'success'
		#continue until portal is found
		while myDF.last_result != 'portal':
			#to exit in middle of run
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			#communicate with framework
			else:
				#Get surroundings
				#############################################################
				x_var = playerCoord[0]
				y_var = playerCoord[1]

				#get up
				if grid[x_var][y_var - 1] == WALL:
					playerSur[0] = '1'
				elif grid[x_var][y_var - 1] == PORTAL:
					playerSur[0] = '3'
				elif grid[x_var][y_var - 1] == SPACE:
					playerSur[0] = '2'

				#get down
				if grid[x_var][y_var + 1] == WALL:
					playerSur[1] = '1'
				elif grid[x_var][y_var + 1] == PORTAL:
					playerSur[1] = '3'
				elif grid[x_var][y_var + 1] == SPACE:
					playerSur[1] = '2'

				#get right
				if grid[x_var + 1][y_var] == WALL:
					playerSur[2] = '1'
				elif grid[x_var + 1][y_var] == PORTAL:
					playerSur[2] = '3'
				elif grid[x_var + 1][y_var] == SPACE:
					playerSur[2] = '2'
				
				#get left
				if grid[x_var - 1][y_var] == WALL:
					playerSur[3] = '1'
				elif grid[x_var - 1][y_var] == PORTAL:
					playerSur[3] = '3'
				elif grid[x_var - 1][y_var] == SPACE:
					playerSur[3] = '2'

				#get up and left
				if grid[x_var - 1][y_var - 1] == WALL:
					playerSur[4] = '1'
				elif grid[x_var - 1][y_var - 1] == PORTAL:
					playerSur[4] = '3'
				elif grid[x_var - 1][y_var - 1] == SPACE:
					playerSur[4] = '2'
				
				#get down and left
				if grid[x_var - 1][y_var + 1] == WALL:
					playerSur[5] = '1'
				elif grid[x_var - 1][y_var + 1] == PORTAL:
					playerSur[5] = '3'
				elif grid[x_var - 1][y_var + 1] == SPACE:
					playerSur[5] = '2'
				
				#get up and right
				if grid[x_var + 1][y_var - 1] == WALL:
					playerSur[6] = '1'
				elif grid[x_var + 1][y_var - 1] == PORTAL:
					playerSur[6] = '3'
				elif grid[x_var + 1][y_var - 1] == SPACE:
					playerSur[6] = '2'

				#get down and right
				if grid[x_var + 1][y_var + 1] == WALL:
					playerSur[7] = '1'
				elif grid[x_var + 1][y_var + 1] == PORTAL:
					playerSur[7] = '3'
				elif grid[x_var + 1][y_var + 1] == SPACE:
					playerSur[7] = '2'

				#####################################################

				#get the decision from framework
				movement = myDF.get_decision(playerSur)
					
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

			#draw map with updated movement
			for r in range(MAPHEIGHT):
				for c  in range(MAPWIDTH):
					pygame.draw.rect(DISPLAYMAP, colors[grid[c][r]], (c * TILESIZE,r * TILESIZE, TILESIZE, TILESIZE))

			#set new PLAYERIMG position
			DISPLAYMAP.blit(PLAYERIMG, (playerCoord[0] * TILESIZE, playerCoord[1] * TILESIZE))

			#update the display with new PLAYERIMG position
			pygame.display.update()

			#delay between moves for clear demonstration
			#pygame.time.delay(200)