from sys import argv
from collections import defaultdict
from array import array
from Queue import PriorityQueue
from sys import maxint

depth_minimax = 3
depth_alphabeta = 4


__author__ = 'Jakub Klapacz <jklapac2@illinois.edu> and Abhishek Nigam <adnigam2@illinois.edu>'

class ValAction(object):
	def __init__(action , move_value):
		self.action = action
		self.move_value = move_value
	def __str__(self):
		return "Action: {} has Value: {}".format(self.action, self.move_value)

class Board(object):
	def __init__(self, player1, player2, scores_matrix, pos_matrix):
		self.player1 = player1
		self.player2 = player2
		self.free_list = PriorityQueue()
		self.scores_matrix = list(scores_matrix)
		self.pos_matrix = list(pos_matrix)
		self.edge = len(scores_matrix)

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
		self.positions = PriorityQueue()

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

	def __lt__(self, other):
		return self.value > other.value

def get_all_actions(board):
	pass

def alpha_beta_search(board):
	max_obj(board, -maxint -1, maxint)
	return max_obj.action

def max_obj(board, lower, upper):
	pass

#this should set up a game board and initialize the players
#this empties the lists if they are already full
def setup(p1, p2, filename):
	#sets up our six by six board
	# matrix = [[0 for x in range(6)] for x in range(6)]
	string_matrix = list()
	string_matrix[:] = []
	scores_matrix = list()
	scores_matrix[:] = []
	free_list = PriorityQueue()
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
			free_list.put(space)
	
	pos_matrix = list()
	for y in range(len(scores_matrix)):
		pos_matrix.append([])
		for x in range(len(scores_matrix[y])):
			pos_matrix[y].append(0)

	board_file.close()
	return Board(p1, p2, scores_matrix, pos_matrix)
	# for line in board_file:
	# 	print line.split('\t')

def solutionGenerator(board):
	print(board)
	pass


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

	
	print("Player 1 goes first.")
	solveProblem(player1, player2, 'game_boards/Keren.txt')
	
	# solveProblem('game_boards/Narvik.txt')
	# solveProblem('game_boards/Sevastopol.txt')
	# solveProblem('game_boards/Smolensk.txt')
	# solveProblem('game_boards/Westerplatte.txt')


if __name__ == '__main__':
	main()