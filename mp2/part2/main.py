from sys import argv
from collections import defaultdict
from array import array
from Queue import PriorityQueue
from sys import maxint
import copy

depth_minimax = 3
depth_alphabeta = 4


__author__ = 'Jakub Klapacz <jklapac2@illinois.edu> and Abhishek Nigam <adnigam2@illinois.edu>'

class Action(object):
	def __init__(self, blitz, to_space, value):
		self.blitz = blitz
		self.to_space = to_space
		self.value = value
		# this would be value of the action

	def __eq__(self, other):
		x = other[0]
		y = other[1]
		return x == to_space[0] and y == to_space[1]

class Board(object):
	def __init__(self, player1, player2, scores_matrix, pos_matrix, free_list):
		self.player1 = player1
		self.player2 = player2
		self.free_list = list(free_list)
		self.scores_matrix = list(scores_matrix)
		self.pos_matrix = list(pos_matrix)
		self.edge = len(scores_matrix)
		self.turn = 1

	def __str__(self):
		outputStr = ""
		for y in range(len(self.scores_matrix)):
			outputStr += str(self.scores_matrix[y]) + "\t" + str(self.pos_matrix[y]) + "\n"
		outputStr += str(self.player1) + str(self.player2)
		return outputStr

class Player(object):
	def __init__(self, color, player_type):
		self.score = 0
		self.color = color
		self.type = player_type
		self.positions = list()

	def __str__(self):
		 return "Player: \n" \
		 	"\tColor: {}\n" \
		 	"\tScore: {}\n" \
		 	"\tPlaytype: {}\n".format(self.color, self.score, self.type)


class Board_space(object):
	def __init__(self, x, y, value, owner):
		self.x = x
		self.y = y
		self.value = value
		self.owner = owner

	def __str__(self):
		pair = (self.x, self.y)
		outputStr = str(pair) + " Value = " + str(self.value) + " Owner = " + str(self.owner)
		return outputStr

	def __lt__(self, other):
		return self.value < other.value

	def __eq__(self, other):
		if(type(other) is Board_space):
			x = other.x
			y = other.y
		elif(type(other) is Action):
			if(type(other.to_space) is Board_space):
				x = other.to_space.x
				y = other.to_space.y
			else:
				x = other.to_space[0]
				y = other.to_space[1]
		else:
			x = other.x
			y = other.y
		return self.x == x and self.y == y

def apply_action(board, action):
	if(board.turn == 1): board.turn =2
	else: board.turn = 1

def out_of_bounds(space, board):
	x = space[0]
	y = space[1]
	if (x < 0 or x >= board.edge or y < 0 or y >= board.edge):
		return True
	else:
		return False

def get_adjacent(space, board):
	space_list = list()
	potential = list()
	if(space is Board_space):
		x = space.x
		y = space.y
	else:
		x = space[0]
		y = space[1]
	potential.append((x, y + 1))
	potential.append((x, y - 1))
	potential.append((x + 1, y))
	potential.append((x - 1, y))
	for space in potential:
		if(out_of_bounds(space, board) == False):
			space_list.append(space)





def get_all_actions(board):
	enemy = None
	player = None
	if(board.turn == 1):
		enemy = board.player2
		player = board.player1
	else:
		enemy = board.player1
		player = board.player2
	action_list = list()
	adjacent_list = list()
	
	for space in player.positions:
		neighbor_list = get_adjacent(space, board)
		for neighbor in neighbor_list:
			if neighbor not in adjacent_list and neighbor in board.free_list:
				adjacent_list.append(neighbor)
	for space in adjacent_list:
		neighbor_list = get_neighbors(space, board)
		for neighbor in neighbor_list:
			if neighbor in enemy.positions:
				combined_value = board.scores_matrix[neighbor[1]][neighbor[0]] + board.scores_matrix[space[1]][space[0]]
				curr_action = Action(True, space, combined_value)
				action_list.append(curr_action)
	for space in board.free_list:
		if space not in action_list:
			action_list.append(Action(False, space, board.scores_matrix[space.y][space.x]))
	return action_list


	

def minimax(board):
	potential_actions = get_all_actions(board)
	# if not potential_actions: 
	# 	# should this really return this???
	# 	return cur_utility(board)

	max_action = potential_actions[0]

	for each_action in potential_actions:
		applier_board = copy.deepcopy(board)
		apply_action(applier_board, each_action)
		if minimax_min(applier_board, 0) > max_action.value:
			max_action = each_action

	return max_action
	

def minimax_max(board, depth):
	if terminal_state_mm(board, depth): return cur_utility(board)
	v = -maxint -1
	potential_actions = get_all_actions(board)
	for each_action in potential_actions:
		applier_board = copy.deepcopy(board)
		apply_action(applier_board, each_action)
		v = max(v, minimax_min(applier_board, depth+1))
	return v


def minimax_min(board, depth):
	if terminal_state_mm(board, depth): return cur_utility(board)
	v = maxint
	potential_actions = get_all_actions(board)
	for each_action in potential_actions:
		applier_board = copy.deepcopy(board)
		apply_action(applier_board, each_action)
		v = min(v, minimax_max(applier_board, depth+1))
	return v



def alpha_beta_search(board):
	deep_copy_board = copy.deepcopy(board)

	potential_val = max_value(deep_copy_board, -maxint -1, maxint, 0)

	#search through get all actions and find action with val closest to potential_val
	potential_actions = get_all_actions(board)
	# if not potential_actions:
	# 	#what should this actually return here???
	# 	return cur_utility(board)

	# cloest_action = potential_actions[0]

	for each_action in potential_actions:
		if(each_action.value == potential_val):
			return each_action

	#should never reach this
	return None

def max_value(board, alpha, beta, depth):
	if(terminal_state_ab(board,depth)): return cur_utility(board)
	v = -maxint-1

	potential_actions = get_all_actions(board)

	for each_action in potential_actions:
		applier_board = copy.deepcopy(board)
		apply_action(applier_board, each_action)
		v = max(v, min_value(applier_board, alpha, beta, depth+1))
		if v >= beta: return v
		alpha = max(alpha, v)

	return v

def min_value(board, alpha, beta, depth):
	if(terminal_state_ab(board, depth)): return cur_utility(board)
	
	v = maxint
	potential_actions = get_all_actions(board)

	for each_action in potential_actions:
		applier_board = copy.deepcopy(board)
		apply_action(applier_board, each_action)
		v = min(v, max_value(applier_board, alpha, beta, depth+1))
		if v <= alpha: return v
		beta = min(beta, v)

	return v


	

def cur_utility(board):
	pass


def terminal_state_mm(board, depth):
	if(depth > depth_minimax): return True
	potential_actions = get_all_actions(board)
	if not potential_actions:
		return True
	return False

def terminal_state_ab(board, depth):
	if(depth > depth_alphabeta): return True
	potential_actions = get_all_actions(board)
	if not potential_actions:
		return True
	return False

def take_action(board):
	action = None
	if(board.turn == 1):
		if(board.player1.type == 'alphabeta'):
			action = alpha_beta_search(board)
		elif(board.player1.type == 'minimax'):
			action = minimax(board)
		else:
			action = get_human_action(board)
			return
	else:
		if(board.player2.type == 'alphabeta'):
			action = alpha_beta_search(board)
		elif(board.player2.type == 'minimax'):
			action = minimax(board)
		else:
			action = get_human_action(board)
			return

	apply_action(board, action)

def get_human_action():
	print(board)
	x = int(input('Enter the X coordinate of your action:'))
	y = int(input('Enter the Y coordinate of your action:'))
	apply_action(board, (x,y))
	# implement the rest here


#this should set up a game board and initialize the players
#this empties the lists if they are already full
def setup(p1, p2, filename):
	#sets up our six by six board
	# matrix = [[0 for x in range(6)] for x in range(6)]
	string_matrix = list()
	string_matrix[:] = []
	scores_matrix = list()
	scores_matrix[:] = []
	free_list = list()
	#this reads the file
	if(filename == None):
		raise Exception("No board provided!!!")
	board_file = open(filename, "r")

	#this puts every line into a matrix
	all_lines = board_file.read().splitlines()
	for listy in all_lines:
		string_matrix.append(listy.split())
	
	# matrix finally holds the game board 
	# elements can be accessed with int_matrix[0][0]
	# each row is a list
	# coordinates are therefore y,x -- 0 indexed
	
	scores_matrix = [map(int, x) for x in string_matrix]

	for y in range(len(scores_matrix)):
		for x in range(len(scores_matrix[y])):
			space = Board_space(x, y, scores_matrix[y][x], None)
			free_list.append(space)
	
	pos_matrix = list()
	for y in range(len(scores_matrix)):
		pos_matrix.append([])
		for x in range(len(scores_matrix[y])):
			pos_matrix[y].append(0)

	board_file.close()
	return Board(p1, p2, scores_matrix, pos_matrix, free_list)


def solutionGenerator(board):
	print(board)
	play(board)
	print(board)


def play(board):
	potential_actions = get_all_actions(board)
	if not potential_actions: return
	take_action(board)
	play(board)
	return


def all():
	print('Running Keren')
	all_for_one_board('game_boards/Keren.txt')
	print('Running Narvik')
	all_for_one_board('game_boards/Narvik.txt')
	print('Running Sevastopol')
	all_for_one_board('game_boards/Sevastopol.txt')
	print('Running Smolensk')
	all_for_one_board('game_boards/Smolensk.txt')
	print('Running Westerplatte')
	all_for_one_board('game_boards/Westerplatte.txt')

def all_for_one_board(filename):
	print('minimax vs minimax')
	player1 = Player("blue", "minimax")
	player2 = Player("green", "minimax")
	solveProblem(player1, player2, filename)


	print('alphabeta vs alphabeta')
	player1 = Player("blue", "alphabeta")
	player2 = Player("green", "alphabeta")
	solveProblem(player1, player2, filename)

	print('minimax vs alphabeta, minimax goes first')
	player1 = Player("blue", "minimax")
	player2 = Player("green", "alphabeta")
	solveProblem(player1, player2, filename)

	print('alphabeta vs minimax, alphabeta goes first')
	player1 = Player("blue", "alphabeta")
	player2 = Player("green", "minimax")
	solveProblem(player1, player2, filename)


def solveProblem(p1, p2, filename):
	board = setup(p1, p2, filename)
	solutionGenerator(board)

def main():

	if(len(argv) != 5):
		print("Running all game boards with default conditions")
		player1 = Player("blue", "alphabeta")
		player2 = Player("green", "minimax")
	else:
		player1 = Player(argv[1], argv[2])
		player2 = Player(argv[3], argv[4])

	if(argv[2] == 'all'):
		all()
		return
	
	print("Player 1 goes first.")
	solveProblem(player1, player2, 'game_boards/Keren.txt')
	
	# solveProblem('game_boards/Narvik.txt')
	# solveProblem('game_boards/Sevastopol.txt')
	# solveProblem('game_boards/Smolensk.txt')
	# solveProblem('game_boards/Westerplatte.txt')


if __name__ == '__main__':
	main()