import random
import pygame, sys
from pygame.locals import *
from DecisionFactory3Change import *
#from FinalDF import *

myDF = DecisionFactory()

#tile and color values
SPACE = 1
WALL = 2
PORTAL = 3
DEATH = 4
LIFE = 5
BLUE = (25, 25, 112)
RED = (139, 26, 26)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#dimensions of board
TILESIZE = 50
MAPWIDTH = 11
MAPHEIGHT = 10

#colors to distinguish tiles
colors = {
	SPACE : BLUE,
	PORTAL : GOLD,
	WALL : RED,
	DEATH : BLACK,
	LIFE : WHITE
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


while True:
	map = input("Enter Map\n1. Empty\n2. Safe\n3. Danger\n4. Life\n")

	if map == 1:
		break
	elif map == 2:
		break
	elif map == 3:
		break
	elif map == 4:
		break
	else:
		map = 99
		print "Invalid Map."

	if map != 99:
		break

#place interior walls
#for row in range(1, MAPWIDTH-1, 2):
#	grid[row][MAPHEIGHT/2] = WALL
#for col in range(1, MAPHEIGHT-1, 2):
#	grid[MAPWIDTH/2][col] = WALL

#choose and set position for the portal
#j = random.randint(1,MAPWIDTH-2)
#k = random.randint(1,MAPHEIGHT-2)
#j=7
#k=4
#while grid[j][k] == WALL:
#	j = random.randint(1,MAPWIDTH-2)
#	k = random.randint(1,MAPHEIGHT-2)
#grid[j][k] = PORTAL

#initialize pygame and map
pygame.init()
DISPLAYMAP = pygame.display.set_mode((MAPWIDTH * TILESIZE, MAPHEIGHT * TILESIZE+50))

#create and place the player not in the same place as portal
PLAYERIMG = pygame.image.load('char.png').convert_alpha()
q = random.randint(1,MAPWIDTH-2)
w = random.randint(1,MAPHEIGHT-2)
#while(q == j and w == k):
#	q = random.randint(1,MAPWIDTH-2)
#	w = random.randint(1,MAPHEIGHT-2)
q=1
w=1
playerCoord = [q,w]
playerSur = ['0','0','0','0','0','0','0','0'] #player surrounding

INVFONT = pygame.font.Font(pygame.font.get_default_font(), 18)

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

		if map == 1:
			grid[7][4] = PORTAL
		elif map == 2:
			grid[7][4] = PORTAL
			grid[6][1] = WALL
			grid[6][2] = WALL
			grid[6][3] = WALL
			grid[6][4] = WALL
			grid[6][5] = WALL
			grid[6][8] = WALL
			grid[6][7] = WALL
			grid[7][5] = WALL
			grid[7][7] = WALL
			grid[8][5] = WALL
			grid[8][4] = WALL
			grid[8][3] = WALL
			grid[8][2] = WALL
			grid[2][2] = WALL
			grid[2][4] = WALL
			grid[2][5] = WALL
			grid[2][7] = WALL
			grid[3][2] = WALL
			grid[3][4] = WALL
			grid[3][5] = WALL
			grid[4][2] = WALL
			grid[4][3] = WALL
			grid[4][4] = WALL
			grid[4][5] = WALL
			grid[3][7] = WALL
			grid[4][7] = WALL
			grid[8][7] = WALL
			grid[2][8] = WALL
			grid[3][8] = WALL
			grid[4][8] = WALL
		elif map == 3:
			grid[7][4] = PORTAL
			grid[3][1] = DEATH
			grid[8][6] = DEATH
			grid[8][1] = DEATH
			grid[8][4] = WALL
			grid[2][6] = WALL
			grid[6][1] = WALL
			grid[6][2] = WALL
			grid[6][3] = WALL
			grid[6][4] = WALL
			grid[6][5] = WALL
			grid[6][8] = WALL
			grid[6][7] = WALL
			grid[7][5] = WALL
			grid[7][7] = WALL
			grid[8][5] = WALL
			grid[8][3] = WALL
			grid[8][2] = WALL
			grid[2][2] = WALL
			grid[2][4] = WALL
			grid[2][5] = WALL
			grid[2][7] = WALL
			grid[3][2] = WALL
			grid[3][5] = WALL
			grid[4][2] = WALL
			grid[4][3] = WALL
			grid[4][4] = WALL
			grid[4][5] = WALL
			grid[3][7] = WALL
			grid[4][7] = WALL
			grid[8][7] = WALL
		elif map == 4:
			grid[7][4] = PORTAL
			grid[3][1] = DEATH
			grid[8][6] = DEATH
			grid[8][1] = DEATH
			grid[3][4] = LIFE
			grid[8][4] = WALL
			grid[2][6] = WALL
			grid[6][1] = WALL
			grid[6][2] = WALL
			grid[6][3] = WALL
			grid[6][4] = WALL
			grid[6][5] = WALL
			grid[6][8] = WALL
			grid[6][7] = WALL
			grid[7][5] = WALL
			grid[7][7] = WALL
			grid[8][5] = WALL
			grid[8][3] = WALL
			grid[8][2] = WALL
			grid[2][2] = WALL
			grid[2][4] = WALL
			grid[2][5] = WALL
			grid[2][7] = WALL
			grid[3][2] = WALL
			grid[3][5] = WALL
			grid[4][2] = WALL
			grid[4][3] = WALL
			grid[4][4] = WALL
			grid[4][5] = WALL
			grid[3][7] = WALL
			grid[4][7] = WALL
			grid[8][7] = WALL

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
				if grid[x_var][y_var-1] == WALL:
					playerSur[0] = '1'
				elif grid[x_var][y_var-1] == PORTAL:
					playerSur[0] = '3'
				elif grid[x_var][y_var-1] == DEATH:
					playerSur[0] = '4'
				elif grid[x_var][y_var-1] == LIFE:
					playerSur[0] = '5'
				else: playerSur[0] = '2'

				#get down
				if grid[x_var][y_var+1] == WALL:
					playerSur[1] = '1'
				elif grid[x_var][y_var+1] == PORTAL:
					playerSur[1] = '3'
				elif grid[x_var][y_var+1] == DEATH:
					playerSur[1] = '4'
				elif grid[x_var][y_var+1] == LIFE:
					playerSur[1] = '5'
				else: playerSur[1] = '2'

				#get right
				if grid[x_var+1][y_var] == WALL:
					playerSur[2] = '1'
				elif grid[x_var+1][y_var] == PORTAL:
					playerSur[2] = '3'
				elif grid[x_var+1][y_var] == DEATH:
					playerSur[2] = '4'
				elif grid[x_var+1][y_var] == LIFE:
					playerSur[2] = '5'
				else: playerSur[2] = '2'

				#get left
				if grid[x_var-1][y_var] == WALL:
					playerSur[3] = '1'
				elif grid[x_var-1][y_var] == PORTAL:
					playerSur[3] = '3'
				elif grid[x_var-1][y_var] == DEATH:
					playerSur[3] = '4'
				elif grid[x_var-1][y_var] == LIFE:
					playerSur[3] = '5'
				else: playerSur[3] = '2'

				#get up and left
				if grid[x_var-1][y_var-1] == WALL:
					playerSur[4] = '1'
				elif grid[x_var-1][y_var-1] == PORTAL:
					playerSur[4] = '3'
				elif grid[x_var-1][y_var-1] == DEATH:
					playerSur[4] = '4'
				elif grid[x_var-1][y_var-1] == LIFE:
					playerSur[4] = '5'
				else: playerSur[4] = '2'

				#get down and left
				if grid[x_var-1][y_var+1] == WALL:
					playerSur[5] = '1'
				elif grid[x_var-1][y_var+1] == PORTAL:
					playerSur[5] = '3'
				elif grid[x_var-1][y_var+1] == DEATH:
					playerSur[5] = '4'
				elif grid[x_var-1][y_var+1] == LIFE:
					playerSur[5] = '5'
				else: playerSur[5] = '2'
				
				#get up and right
				if grid[x_var+1][y_var-1] == WALL:
					playerSur[6] = '1'
				elif grid[x_var+1][y_var-1] == PORTAL:
					playerSur[6] = '3'
				elif grid[x_var+1][y_var-1] == DEATH:
					playerSur[6] = '4'
				elif grid[x_var+1][y_var-1] == LIFE:
					playerSur[6] = '5'
				else: playerSur[6] = '2'

				#get down and right
				if grid[x_var+1][y_var+1] == WALL:
					playerSur[7] = '1'
				elif grid[x_var+1][y_var+1] == PORTAL:
					playerSur[7] = '3'
				elif grid[x_var+1][y_var+1] == DEATH:
					playerSur[7] = '4'
				elif grid[x_var+1][y_var+1] == LIFE:
					playerSur[7] = '5'
				else: playerSur[7] = '2'
				#####################################################

				#get the decision from framework
				movement = myDF.get_decision(playerSur)

				#evaluate the decision and determine correct move
				if movement == 'right':
					if grid[playerCoord[0] + 1][playerCoord[1]] == WALL:
						myDF.put_result('wall')
					elif grid[playerCoord[0] + 1][playerCoord[1]] == DEATH:
						myDF.put_result('death')
						grid[playerCoord[0] + 1][playerCoord[1]] = SPACE
						playerCoord[0] += 1
					elif grid[playerCoord[0] + 1][playerCoord[1]] == LIFE:
						myDF.put_result('life')
						playerCoord[0] += 1
					elif grid[playerCoord[0] + 1][playerCoord[1]] == PORTAL:
						playerCoord[0] += 1
						myDF.put_result('portal')
					else:
						playerCoord[0] += 1
						myDF.put_result('success')
				if movement == 'left':
					if grid[playerCoord[0] - 1][playerCoord[1]] == WALL:
						myDF.put_result('wall')
					elif grid[playerCoord[0] - 1][playerCoord[1]] == DEATH:
						myDF.put_result('death')
						grid[playerCoord[0] - 1][playerCoord[1]] = SPACE
						playerCoord[0] -= 1
					elif grid[playerCoord[0] - 1][playerCoord[1]] == LIFE:
						myDF.put_result('life')
						playerCoord[0] -= 1
					elif grid[playerCoord[0] - 1][playerCoord[1]] == PORTAL:
						playerCoord[0] -= 1
						myDF.put_result('portal')
					else:
						playerCoord[0] -= 1
						myDF.put_result('success')
				if movement == 'up':
					if grid[playerCoord[0]][playerCoord[1] - 1] == WALL:
						myDF.put_result('wall')
					elif grid[playerCoord[0]][playerCoord[1] - 1] == DEATH:
						myDF.put_result('death')
						grid[playerCoord[0]][playerCoord[1] - 1] = SPACE
						playerCoord[1] -= 1
					elif grid[playerCoord[0]][playerCoord[1] - 1] == LIFE:
						myDF.put_result('life')
						playerCoord[1] -= 1
					elif grid[playerCoord[0]][playerCoord[1] - 1] == PORTAL:
						playerCoord[1] -= 1
						myDF.put_result('portal')
					else:
						playerCoord[1] -= 1
						myDF.put_result('success')
				if movement == 'down':
					if grid[playerCoord[0]][playerCoord[1] + 1] == WALL:
						myDF.put_result('wall')
					elif grid[playerCoord[0]][playerCoord[1] + 1] == DEATH:
						myDF.put_result('death')
						grid[playerCoord[0]][playerCoord[1] + 1] = SPACE
						playerCoord[1] += 1
					elif grid[playerCoord[0]][playerCoord[1] + 1] == LIFE:
						myDF.put_result('life')
						playerCoord[1] += 1
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

			#display health
			placePosition = 10
			text = INVFONT.render(str('Health = '), True, GOLD, BLACK)
			health = INVFONT.render(str(myDF.life), True, GOLD, BLACK)
			DISPLAYMAP.blit(text,(10,MAPHEIGHT*TILESIZE+20))
			DISPLAYMAP.blit(health,(90, MAPHEIGHT*TILESIZE+20))

			#update the display with new PLAYERIMG position
			pygame.display.update()
			if myDF.num_rounds > 1:
				#delay between moves for clear demonstration
				pygame.time.delay(200)