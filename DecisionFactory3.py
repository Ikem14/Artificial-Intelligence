import random
import copy

#DecisionFactory communicates with the framework
class DecisionFactory:
	def __init__(self , name='Davros' ):
		self.name = name
		self.directions = [ 'wait', 'up', 'down', 'right', 'left' ]
		self.last_result = 'success'
		self.last_direction = 'wait'
		self.past_directions = ['wait']
		self.num_moves = 0
		self.player_Coord = [0,0]
		self.string_moves = [['10000']]
		#left value is horizontal movement. right value is vertical movement
		self.total_movement = [0,0]
		self.num_rounds = 1
		self.opp_direction = 'wait'
		self.stuck_move = 'wait'
		self.allow_back = False
		self.repeat_count = 0
		self.alt = random.randint(1,4) #for alternating directions
		#self.straight_count = 0
		self.direction_blocked = False
		self.sight = ['0','0','0','0','0','0','0','0']

	#change the value in the string to indicate a wall
	def change_val(self, index, val):
		temp = list(self.string_moves[self.player_Coord[1]][self.player_Coord[0]])
		#print index
		temp[index] = val
		self.string_moves[self.player_Coord[1]][self.player_Coord[0]] = "".join(temp)

	#displays the grid made in the DF
	def print_memory(self):
		for row in self.string_moves:
			for i in row:
				print i,
			print

	#searches array for value
	def search_move(self, index, val):
		for x in range(len(self.string_moves)):
					for y in range(len(self.string_moves[0])):
						if self.string_moves[x][y][index] == val:
							a = [y, x]
							return a

	def count_paths(self, target):
		temp = list(target)
		count = 0

		for x in range(5):
			if temp[x] == '2':
				count += 1

		target = "".join(temp)

		return count

	#sends a move for the framework
	def get_decision(self, old_sight = [], verbose = True):
		#- - -
		#- * -
		#- - -
		#up,  up and right, up and left, left, right, down and right, down, down and left
		for x in range (8):
			self.sight[x] = old_sight[x]
		print self.sight
		return self.choose_direction()

	#decides which direction to move
	def choose_direction(self):
		if self.stuck_move == 'up':
			self.direction_blocked = True
		elif self.stuck_move == 'down':
			self.direction_blocked = True
		elif self.stuck_move == 'right':
			self.direction_blocked = True
		elif self.stuck_move =='left':
			self.direction_blocked = True
		else:
			self.direction_blocked = False


		if self.num_rounds == 1:

			#explore the unexplored around the agent first
			#go up first, then down. then go Right, and then left
			#always goes up first if its free
			if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '0':
				self.alt = 1
			elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '0':
				self.alt = 2
			elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '0':
				self.alt = 3
			elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '0':
				self.alt = 4

			#if the last movement(direction) was a success, keep direction the same
			elif self.last_result == 'success':
				#keep the direction the same
				#if self.last_direction == 'up' and self.up_count < 1: 
				if self.last_direction == 'up' and self.direction_blocked == False:
					self.alt = 1
				#elif self.last_direction == 'down' and self.down_count < 1:
				elif self.last_direction == 'down' and self.direction_blocked == False: 
					self.alt = 2
				#elif self.last_direction == 'right' and self.right_count < 1: 
				elif self.last_direction == 'right' and self.direction_blocked == False:
					self.alt = 3
				#elif self.last_direction == 'left' and self.left_count < 1: 
				elif self.last_direction == 'left' and self.direction_blocked == False:
					self.alt = 4
				else:
					self.alt = random.randint(1,4)
			
			else:
				#straight_count = 0
				self.alt = random.randint(1,4)
			#prevent the agent from making the same wrong move twice
				while self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
					self.alt = random.randint(1,4)
						
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
						# handles 'up' movement
						if self.alt == '1':
							self.alt = 2  #move down
							if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
								self.alt = 3 #move right
								if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
									self.alt = 4 #move left
						# handles 'down' movement
						if self.alt == '2':
							self.alt = 1 #move up
							if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
								self.alt = 3 #move right
								if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
									self.alt = 4 #move left

						# handles 'right' movement
						if self.alt == '3':
							self.alt = 4 #move left
							if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
								self.alt = 1 #move up
								if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
									self.alt = 2 #move down

						# handles 'left' movement
						if self.alt == '4':
							self.alt = 3 #move right
							if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
								self.alt = 1 #move up
								if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
									self.alt = 2 #move down

			self.num_moves += 1	
		####################################################################################################	
		else:
			
			self.alt = 0

			#print self.total_movement
			#print "at: ", self.string_moves[self.player_Coord[1]][self.player_Coord[0]]

			while True:
				if self.allow_back == True:
					if self.alt == 1:
						self.total_movement[1] += 1
					elif self.alt == 2:
						self.total_movement[1] -= 1
					elif self.alt == 3:
						self.total_movement[0] -= 1
					elif self.alt ==4:
						self.total_movement[0] += 1
					break
				elif self.total_movement[0] > 0: #if need move right
					#print "in right"
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
						#print "right right"
						self.alt = 3 #move right
						self.opp_direction = 'left'
						if self.last_direction != self.opp_direction or self.allow_back == True:
							self.total_movement[0] -= 1
							break
						else:
							self.stuck_move = 'right'
					elif self.total_movement[1] > 0: #if need move down
						#print "right down"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							#print "right down down"
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							#print "right down left"
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up' :
							#print "right down up"
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						else:
							self.allow_back = True
					elif self.total_movement[1] <= 0: #if need move up
						#print "right up"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							#print "right up up"
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							#print "right up left"
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							#print "right up down"
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						else:
							self.allow_back = True
				elif self.total_movement[0] < 0: #if need move left
					#print "in left"
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
						#print "left left"
						self.alt = 4 # move left
						self.opp_direction = 'right'
						if self.last_direction != self.opp_direction or self.allow_back == True:
							self.total_movement[0] += 1
							break
						else:
							self.stuck_move = 'left'
					elif self.total_movement[1] > 0: #if need move down
						#print "left down"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						else:
							self.allow_back = True
					elif self.total_movement[1] <= 0: #if need move up
						#print "left up"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						else:
							self.allow_back = True
				elif self.total_movement[1] > 0:#if need move down
					#print "in down"
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
					elif self.total_movement[0] < 0: #if need move left
						#print "down left"	
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'		
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						else:
							self.allow_back = True
					elif self.total_movement[0] >= 0: #if need move right
						#print "down right"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						else:
							self.allow_back = True
				elif self.total_movement[1] < 0: #if need move up
					#print "in up"
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
					elif self.total_movement[0] < 0: #if need move left
						#print "up left"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 #move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						else:
							self.allow_back = True
					elif self.total_movement[0] >= 0: #if need move right
						#print "up right"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 #move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '2' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						else:
							self.allow_back = True

			self.num_moves += 1

		#for second round
		if self.num_rounds != 1:
			#check if the agent is stuck in a loop
			if self.num_moves > 3:
				if self.past_directions[self.num_moves-4] == self.directions[self.alt]:
					self.repeat_count += 1
				else:
					self.repeat_count = 0

				#print "repeat count:", self.repeat_count

			#in the rare scenario where the agent gets stuck in a 4 move loop
			#choose a random direction to exit loop
			if self.repeat_count > 4:
				#undo the change made
				if self.alt == 1:
					self.total_movement[1] -= 1
				elif self.alt == 2:
					self.total_movement[1] += 1
				elif self.alt == 3:
					self.total_movement[0] += 1
				elif self.alt ==4:
					self.total_movement[0] -= 1
				#pick a new direction
				self.alt = random.randint(1,4)
				while self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
					self.alt = random.randint(1,4)
				if self.alt == 1:
					self.total_movement[1] += 1
				elif self.alt == 2:
					self.total_movement[1] -= 1
				elif self.alt == 3:
					self.total_movement[0] -= 1
				elif self.alt ==4:
					self.total_movement[0] += 1
				self.repeat_count = 0
			#put the final direction on the end
			self.past_directions.append(self.directions[self.alt])

		#set DF variables based on move that was chosen
		#print "move:", self.directions[r]	
		#print self.total_movement
		#self.print_memory()
		#print ""

		self.allow_back = False
		self.stuck_move = 'wait'		
		self.direction_blocked = self.last_direction 
		self.last_direction = self.directions[self.alt]

		return self.directions[self.alt]

	def put_result(self, result):
		#if the move resulted in a wall, mark it in the list
		#else create new index if needed and move the player
		if result == 'wall':
			direction_blocked = True
			if self.last_direction == 'up':
				self.change_val(1,'1')
			elif self.last_direction == 'down':
				self.change_val(2, '1')
			elif self.last_direction == 'right':
				self.change_val(3, '1')
			elif self.last_direction == 'left':
				self.change_val(4, '1')
			self.last_result = result
		else:
			if self.last_direction == 'left' and self.player_Coord[0] != 0:
				self.change_val(4,'2')
				self.player_Coord[0] -= 1
				if self.num_rounds == 1:
					self.total_movement[0] -= 1
				self.change_val(3,'2')
			elif self.last_direction == 'left' and self.player_Coord[0] == 0:
				self.change_val(4,'2')
				for row in self.string_moves:
					row.insert(0,'00000')
				if self.num_rounds == 1:
					self.total_movement[0] -= 1
				self.change_val(3, '2')
			elif self.last_direction == 'right' and self.player_Coord[0] != (len(self.string_moves[0])-1):
				self.change_val(3,'2')
				self.player_Coord[0] += 1
				if self.num_rounds == 1:
					self.total_movement[0] += 1
				self.change_val(4, '2')
			elif self.last_direction == 'right' and self.player_Coord[0] == (len(self.string_moves[0])-1):
				self.change_val(3,'2')
				for row in self.string_moves:
					row.append('00000')
				self.player_Coord[0] += 1
				if self.num_rounds == 1:
					self.total_movement[0] += 1
				self.change_val(4, '2')
			elif self.last_direction == 'up' and self.player_Coord[1] != 0:
				self.change_val(1,'2')
				self.player_Coord[1] -= 1
				if self.num_rounds == 1:
					self.total_movement[1] -= 1
				self.change_val(2, '2')
			elif self.last_direction == 'up' and self.player_Coord[1] == 0:
				self.change_val(1,'2')
				self.string_moves.insert(0, [])
				for col in self.string_moves[1]:
					self.string_moves[0].append('00000')
				if self.num_rounds == 1:
					self.total_movement[1] -= 1
				self.change_val(2, '2')
			elif self.last_direction == 'down' and self.player_Coord[1] != (len(self.string_moves)-1):
				self.change_val(2,'2')
				self.player_Coord[1] += 1
				if self.num_rounds == 1:
					self.total_movement[1] += 1
				self.change_val(1, '2')
			elif self.last_direction == 'down' and self.player_Coord[1] == (len(self.string_moves)-1):
				self.change_val(2,'2')
				self.string_moves.append([])
				for col in self.string_moves[0]:
					self.string_moves[len(self.string_moves)-1].append('00000')
				self.player_Coord[1] += 1
				if self.num_rounds == 1:
					self.total_movement[1] += 1
				self.change_val(1, '2')
			self.last_result = result
		if result == 'portal':
			self.last_result = result
			self.change_val(0, '3')
			print "Round", self.num_rounds, "found portal in", self.num_moves, "moves."
			#self.print_memory()
			#print self.total_movement
			self.num_rounds += 1
			self.player_Coord = self.search_move(0, '1')
			self.num_moves = 0


		#print self.last_result
		#print self.last_direction
		#self.print_memory()
		#print ""
		#print self.total_movement