import random

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
		self.direction_blocked = False
		self.sight = ['0','0','0','0','0','0','0','0']
		self.life = 3
		self.health_path = [0,0]
		self.looking = False
		self.next = 0 #to keep the value of the second direction when near a portal
		self.blocked_alt = 0
		self.last_last_direction = self.last_direction
		self.deadCount = 0

	#change the value in the string to indicate a wall
	def change_val(self, index, val):
		#print "change ", index, "in ", self.string_moves[self.player_Coord[1]][self.player_Coord[0]], "to", val
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
			elif temp[x] =='4':
				count += 1
			elif temp[x] == '5':
				count += 1

		target = "".join(temp)

		return count

	#sends a move for the framework
	def get_decision(self, old_sight = [], verbose = True):
		for x in range (8):
			self.sight[x] = old_sight[x]
		return self.choose_direction()

	#decides which direction to move
	def choose_direction(self):
		
		#check for dead ends
		for x in range(4):
			if self.sight[x] == '1':
				self.deadCount += 1
			if self.deadCount >= 3:
				self.direction_blocked = False
				if self.sight[0] == '1' and self.sight[1] == '1' and self.sight[2] == '1':
					print "DEAD END"
					self.direction_blocked = True
					self.blocked_alt = 4
					self.alt = 4
					self.last_last_direction = self.last_direction
					self.last_direction = self.directions[self.alt]
					return self.directions[self.alt]

				elif self.sight[0] == '1' and self.sight[1] == '1' and self.sight[3] == '1':
					print "DEAD END"
					self.direction_blocked = True
					self.blocked_alt = 3
					self.alt = 3
					self.last_last_direction = self.last_direction
					self.last_direction = self.directions[self.alt]
					return self.directions[self.alt]
				elif self.sight[0] == '1' and self.sight[2] == '1' and self.sight[3] == '1':
					print "DEAD END"
					self.direction_blocked = True
					self.blocked_alt = 2
					self.alt = 2
					self.last_last_direction = self.last_direction
					self.last_direction = self.directions[self.alt]
					return self.directions[self.alt]
				elif self.sight[1] == '1' and self.sight[2] == '1' and self.sight[3] == '1':
					print "DEAD END"
					self.direction_blocked = True
					self.blocked_alt = 1
					self.alt = 1
					self.last_last_direction = self.last_direction
					self.last_direction = self.directions[self.alt]
					return self.directions[self.alt]

			#if portal was already detected, go to that direction
			if self.next != 0:
				self.alt = self.next
				self.last_last_direction = self.last_direction
				self.last_direction = self.directions[self.alt]
				return self.directions[self.alt]
			else:
				#check for portal first
				sight_count = 0
				while sight_count < 8:
					if self.sight[sight_count] == '3':
						if sight_count == 0:
							self.alt = 1 #go up into portal
						elif sight_count == 1:
							self.alt = 2 #go down into portal
						elif sight_count == 2:
							self.alt = 3 #go right into portal
						elif sight_count == 3:
							self.alt = 4 #go left into portal

						elif sight_count == 4:
							self.alt = 1 #go up and set self.next to left into portal
							self.next = 4

						elif sight_count == 5:
							self.alt = 2 #go down and set self.next to left into portal
							self.next = 4

						elif sight_count == 6:
							self.alt = 1 #go up and set self.next to right into portal
							self.next = 3

						elif sight_count == 7:
							self.alt = 2 #go down and set self.next to right into portal
							self.next = 3
						self.last_last_direction = self.last_direction
						self.last_direction = self.directions[self.alt]
						return self.directions[self.alt]
					sight_count += 1 #increment sight_count

		#self.alt = random.randint(1,4)
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

			if (self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] == '0' and self.sight[0] != '1') or self.sight[0] == '3':
				self.alt = 1
				self.last_last_direction = self.last_direction
				self.last_direction = self.directions[self.alt]
				return self.directions[self.alt]
			elif (self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] == '0' and self.sight[1] != '1') or self.sight[1] == '3':
				self.alt = 2
				self.last_last_direction = self.last_direction
				self.last_direction = self.directions[self.alt]
				return self.directions[self.alt]
			elif (self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] == '0' and self.sight[2] != '1') or self.sight[2] == '3':
				self.alt = 3
				self.last_last_direction = self.last_direction
				self.last_direction = self.directions[self.alt]
				return self.directions[self.alt]
			elif (self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] == '0' and self.sight[3] != '1') or self.sight[3] == '3':
				self.alt = 4
				self.last_last_direction = self.last_direction
				self.last_direction = self.directions[self.alt]
				return self.directions[self.alt]
			else:
				self.alt = random.randint(1,4)
				while self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '1':
					self.alt = random.randint(1,4)
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][self.alt] == '0':
						self.last_last_direction = self.last_direction
						self.last_direction = self.directions[self.alt]
						return self.directions[self.alt]
					self.alt = random.randint(1,4)

			self.num_moves += 1

		else:
			self.alt = 0

			while True:
				if self.allow_back == True:
					if self.alt == 1:
						self.total_movement[1] += 1
					elif self.alt == 2:
						self.total_movement[1] -= 1
					elif self.alt == 3:
						self.total_movement[0] -= 1
					elif self.alt == 4:
						self.total_movement[0] += 1
					break
				elif self.total_movement[0] > 0: #if need move right
					#print "in right"
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
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
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							#print "right down down"
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							#print "right down left"
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up' :
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
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							#print "right up up"
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							#print "right up left"
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
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
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
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
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
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
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
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
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							#print "down down"
							self.alt = 2 # move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
					elif self.total_movement[0] < 0: #if need move left
						#print "down left"	
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'		
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
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
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
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
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][1] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]-1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'up':
							self.alt = 1 #move up
							self.opp_direction = 'down'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] += 1
								break
							else:
								self.stuck_move = 'up'
					elif self.total_movement[0] < 0: #if need move left
						#print "up left"
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
							self.alt = 4 # move left
							self.opp_direction = 'right'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] += 1
								break
							else:
								self.stuck_move = 'left'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 #move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
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
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][3] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]+1][0] == '3') and self.stuck_move != 'right':
							self.alt = 3 # move right
							self.opp_direction = 'left'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[0] -= 1
								break
							else:
								self.stuck_move = 'right'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][2] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]]) > 1 or self.string_moves[self.player_Coord[1]+1][self.player_Coord[0]][0] == '3') and self.stuck_move != 'down':
							self.alt = 2 #move down
							self.opp_direction = 'up'
							if self.last_direction != self.opp_direction or self.allow_back == True:
								self.total_movement[1] -= 1
								break
							else:
								self.stuck_move = 'down'
						elif self.string_moves[self.player_Coord[1]][self.player_Coord[0]][4] != '1' and (self.count_paths(self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1]) > 1 or self.string_moves[self.player_Coord[1]][self.player_Coord[0]-1][0] == '3') and self.stuck_move != 'left':
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
				elif self.alt == 4:
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
				elif self.alt == 4:
					self.total_movement[0] += 1
				
				self.num_rounds = 1

			#put the final direction on the end
			self.past_directions.append(self.directions[self.alt])

		#print "life: ", self.life, "move: ", self.directions[self.alt]
		
		#round 1: if the agent is at 1 health and the next move would kill it
		#rest total_movement and randomly select a move that doesn't kill
		if self.num_rounds == 1:
			while self.life <= 1 and self.sight[self.alt-1] == '4':
				self.alt = random.randint(1,4)

		#round 2: if the agent is at 1 health and the next move would kill it
		#rest total_movement and randomly select a move that doesn't kill
		if self.num_rounds == 2 and self.life <= 1 and self.sight[self.alt-1] == '4':

			skip = 0

			if self.looking == False:
				self.looking = True
				self.health_path = self.search_move(0, '5')
				#print "health path: ", self.health_path, " and player: ", self.player_Coord
				self.health_path[0] = self.health_path[0] - self.player_Coord[0]
				self.health_path[1] = self.health_path[1] - self.player_Coord[1]

				#print "health at: ", self.health_path
					
				temp = self.total_movement
				self.total_movement = self.health_path
				self.health_path = temp

				print "to health: ", self.total_movement

				#print "new movement: ", self.total_movement

				skip = 1

			while self.sight[self.alt-1] == '4' or self.sight[self.alt-1] == '1':
				if skip != 1:
					if self.alt == 1:
						self.total_movement[1] -= 1
					elif self.alt == 2:
						self.total_movement[1] += 1
					elif self.alt == 3:
						self.total_movement[0] += 1
					elif self.alt == 4:
						self.total_movement[0] -= 1

				skip = 0

				self.alt = random.randint(1,4)

				if self.alt == 1:
					self.total_movement[1] += 1
				elif self.alt == 2:
					self.total_movement[1] -= 1
				elif self.alt == 3:
					self.total_movement[0] -= 1
				elif self.alt == 4:
					self.total_movement[0] += 1

				#print "new move: ", self.directions[self.alt]

		self.allow_back = False
		self.stuck_move = 'wait'		
		self.direction_blocked = self.last_direction 
		self.last_last_direction = self.last_direction
		self.last_direction = self.directions[self.alt]

		#print "move: ", self.directions[self.alt]

		return self.directions[self.alt]

	def put_result(self, result):

		self.last_result = result

		#set values of current space from framework sight
		if self.num_rounds == 1:
			#print self.sight
			for x in range (5):
				y=x+1
				if y < 5:
					self.change_val(y, self.sight[x])

		#Mark dead ends
		if self.direction_blocked == True:
			print self.last_direction
			if self.last_direction == 'up':
				self.change_val(2, '1')
			elif self.last_direction == 'down':
				self.change_val(1, '1')
			elif self.last_direction == 'right':
				self.change_val(4, '1')
			elif self.last_direction == 'left':
				self.change_val(3, '1')
			print "Marked dead end"
			self.direction_blocked = False
			self.blocked_alt = 0
			self.deadCount = 0

		#if the move resulted in a wall, mark it in the list
		#else create new index if needed and move the player
		if result == 'wall':
			direction_blocked = True
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

			if result == 'death':
				if self.num_rounds == 2:
					self.change_val(0, '0')
				self.change_val(0, '4')
				self.life -= 1
			elif result == 'life':
				self.change_val(0, '5')
				self.life += 1
				if self.looking == True:
					portal_loc = self.search_move(0, '3')
					print "player: ", self.player_Coord, " portal: ", portal_loc

					self.total_movement[0] = portal_loc[0] - self.player_Coord[0]
					self.total_movement[1] = portal_loc[1] - self.player_Coord[1]

					print "to portal:", self.total_movement
					self.looking = False

		if result == 'portal':
			self.change_val(0, '3')
			print "Round", self.num_rounds, "found portal in", self.num_moves, "moves."
			print "Agent finished with ", self.life, "health points."
			#set up for second round
			if self.num_rounds == 1:
				self.health_path = self.search_move(0, '5')
				#print "health at: ", self.health_path

				self.print_memory()
				self.player_Coord = self.search_move(0, '1')
				#print "after portal: ", self.player_Coord
				self.num_moves = 0
				self.life = 3
				print "to portal: ", self.total_movement
			self.num_rounds += 1

		print "at: ", self.player_Coord, " with right(+)/left(-): ", self.total_movement[0], "with down(+)/up(-): ", self.total_movement[1]
		#print "end round life: ", self.life
		#print "move ", self.last_direction, "resulted in ", self.last_result
		#print ""