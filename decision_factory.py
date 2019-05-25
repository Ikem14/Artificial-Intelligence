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
		self.current_moves = [0,0,0,0,0]
		self.past_moves = [[[0,0,0,0,0]]]

	def get_decision(self, verbose = True):
		return self.choose_direction()

	def choose_direction(self):
		r = random.randint(1,4)

		#while self.current_moves[r] == 1:
		#	r = random.randint(1,4)

		if self.last_direction != 'wait' and self.last_direction != 'wall':
			print self.player_Coord[1], self.player_Coord[0]
			print self.past_moves


		#while self.past_moves[self.player_Coord[1]][self.player_Coord[0]][r] == 1:
			#r = random.randint(1,4)

		self.last_direction = self.directions[r]
		self.past_directions.append(self.directions[r])
		self.num_moves += 1

		return self.directions[r]

	def put_result(self, result):

		#if the move resulted in a wall, mark it in the list
		#else reset the list
		if result == 'wall':
			if self.last_direction == 'wait':
				self.current_moves[0] = 1
			elif self.last_direction == 'up':
				self.current_moves[1] = 1
			elif self.last_direction == 'down':
				self.current_moves[2] = 1
			elif self.last_direction == 'right':
				self.current_moves[3] = 1
			elif self.last_direction == 'left':
				self.current_moves[4] = 1
		else:
			#self.past_moves[self.player_Coord[1]][self.player_Coord[0]] = self.current_moves
			#self.current_moves = [0,0,0,0,0]
			print self.last_direction

			if self.last_direction == 'left' and self.player_Coord[0] != 0:
				self.player_Coord[0] -= 1
			elif self.last_direction == 'left' and self.player_Coord[0] == 0:
				for i in xrange(len(self.past_moves)):
					self.past_moves[i].insert(0, [0,0,0,0,0])
			elif self.last_direction == 'right' and self.player_Coord[0] != len(self.past_moves[0]):
				self.player_Coord[0] += 1
			elif self.last_direction == 'right' and self.player_Coord[0] == len(self.past_moves[0]):
				for i in xrange(len(self.past_moves)):
					self.past_moves[i].insert(len(self.past_moves[0], [0,0,0,0,0]))
				self.player_Coord[0] += 1
			elif self.last_direction == 'up' and self.player_Coord[1] != 0:
				self.player_Coord[1] -= 1
			elif self.last_direction == 'up' and self.player_Coord[1] == 0:
				#for col in self.past_moves[0]:
				#	col.insert(0, [0,0,0,0,0])
				for i in xrange(len(self.past_moves[0])):
					self.past_moves[i].insert(0, [0,0,0,0,0])
			elif self.last_direction == 'down' and self.player_Coord[1] != len(self.past_moves):
				self.player_Coord[1] += 1
			elif self.last_direction == 'down' and self.player_Coord[1] == len(self.past_moves):
				#for col in self.past_moves[0]:
				#	col.insert(len(self.past_moves, [0,0,0,0,0]))
				for i in xrange(len(self.past_moves[0])):
					self.past_moves[i].insert(len(self.past_moves, [0,0,0,0,0]))
				self.player_Coord[1] += 1

		self.last_result = result

	def print_memory(self):
		print self.past_moves
		print len(self.past_moves)
		print len(self.past_moves[0])