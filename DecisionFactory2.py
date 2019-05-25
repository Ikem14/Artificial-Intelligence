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
		self.string_moves = [['00000']]

	def change_val(current, index):
		temp = list(current.string_moves[current.player_Coord[1]][current.player_Coord[0]])
		temp[index] = '1'
		current.string_moves[current.player_Coord[1]][current.player_Coord[0]] = "".join(temp)

	def print_memory(self):
		for row in self.string_moves:
			for i in row:
				print i,
			print

	def get_decision(self, verbose = True):
		return self.choose_direction()

	def choose_direction(self):
		r = random.randint(1,4)

		#print 'before ', r
		#print 'value ', self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r]
		while self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
			r = random.randint(1,4)
			if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
				# Handles 'up' movement
				if r == '1':
					r = 2  #move down
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
						r = 3 #move right
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
							r = 4 #move left
				# handles 'down' movement
				if r == '2':
					r = 1 #move up
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
						r = 3 #move right
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
							r = 4 #move left

				# handles 'right' movement
				if r == '3':
					r = 4 #move left
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
						r = 1 #move up
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
							r = 2 #move down

				# handles 'left' movement
				if r == '4':
					r = 3 #move right
					if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
						r = 1 #move up
						if self.string_moves[self.player_Coord[1]][self.player_Coord[0]][r] == '1':
							r = 2 #move down
			#if random direction index in memory has a wall, select another direction

		#print 'after ', r

		self.last_direction = self.directions[r]
		self.past_directions.append(self.directions[r])
		self.num_moves += 1

		return self.directions[r]

	def put_result(self, result):

		#if the move resulted in a wall, mark it in the list
		#else reset the list
		if result == 'wall':
			if self.last_direction == 'wait':
				self.change_val(0)
			elif self.last_direction == 'up':
				self.change_val(1)
			elif self.last_direction == 'down':
				self.change_val(2)
			elif self.last_direction == 'right':
				self.change_val(3)
			elif self.last_direction == 'left':
				self.change_val(4)
		else:
			if self.last_direction == 'left' and self.player_Coord[0] != 0:
				self.player_Coord[0] -= 1
			elif self.last_direction == 'left' and self.player_Coord[0] == 0:
				for row in self.string_moves:
					row.insert(0,'00000')
			elif self.last_direction == 'right' and self.player_Coord[0] != (len(self.string_moves[0])-1):
				self.player_Coord[0] += 1
			elif self.last_direction == 'right' and self.player_Coord[0] == (len(self.string_moves[0])-1):
				for row in self.string_moves:
					row.append('00000')
				self.player_Coord[0] += 1
			elif self.last_direction == 'up' and self.player_Coord[1] != 0:
				self.player_Coord[1] -= 1
			elif self.last_direction == 'up' and self.player_Coord[1] == 0:
				self.string_moves.insert(0, [])
				for col in self.string_moves[1]:
					self.string_moves[0].append('00000')
			elif self.last_direction == 'down' and self.player_Coord[1] != (len(self.string_moves)-1):
				self.player_Coord[1] += 1
			elif self.last_direction == 'down' and self.player_Coord[1] == (len(self.string_moves)-1):
				self.string_moves.append([])
				for col in self.string_moves[0]:
					self.string_moves[len(self.string_moves)-1].append('00000')
				self.player_Coord[1] += 1

		print self.last_direction
		self.print_memory()

		self.last_result = result