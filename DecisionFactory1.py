import random 
#import numpy as np

#DecisionFactory communicates with the framework
class DecisionFactory:
	def __init__(self , name='Davros' ):
		self.name = name
		self.directions = [ 'wait', 'up', 'down', 'right', 'left' ]
		self.last_result = 'success'
		self.last_direction = 'wait'
		self.num_moves = 0
		self.wrong_moves = [0, 0, 0, 0, 0]
		self.num_rounds = 1

	def get_decision(self, verbose = True):
		return self.choose_direction()

	def choose_direction(self):
		while self.last_result != 'portal':
			r = random.randint(1,4)

			#if this move resulted in a wall, choose a different one
			#while(self.directions[r] == self.last_direction and self.last_result == 'wall'):
			#	r = random.randint(1,4)

			while self.wrong_moves[r] == 1:
				r = random.randint(1,4)

			self.last_direction = self.directions[r]

			self.num_moves += 1

			return self.directions[r]

	def put_result(self, result):

		#if the move resulted in a wall, mark it in the list
		#else reset the list
		if result == 'wall':
			if self.last_direction == 'wait':
				self.wrong_moves[0] = 1
			elif self.last_direction == 'up':
				self.wrong_moves[1] = 1
			elif self.last_direction == 'down':
				self.wrong_moves[2] = 1
			elif self.last_direction == 'right':
				self.wrong_moves[3] = 1
			elif self.last_direction == 'left':
				self.wrong_moves[4] = 1
		elif result == 'portal':
			self.num_rounds += 1
			print "found portal in", self.num_moves, "moves."
		else:
			for x in range(5):
				self.wrong_moves[x] = 0

		self.last_result = result