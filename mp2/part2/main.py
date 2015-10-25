from sys import argv
from collections import defaultdict
from array import array

string_matrix = list()
matrix = list()

board_edge = 0

player1 = "green"
player2 = "blue"
player1type = "alphabeta"
player2type = "minimax"

__author__ = 'Jakub Klapacz <jklapac2@illinois.edu> and Abhishek Nigam <adnigam2@illinois.edu>'

#this should set up a game board and initialize the players
#this empties the lists if they are already full
def setup(filename):
	#sets up our six by six board
	# matrix = [[0 for x in range(6)] for x in range(6)]
	global string_matrix
	global matrix
	string_matrix[:] = []
	matrix[:] = []

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
	matrix = [map(int, x) for x in string_matrix]

	board_edge = len(matrix)
	for listy in matrix:
		print(listy)

	print()
	print(board_edge)

	board_file.close()
	# for line in board_file:
	# 	print line.split('\t')

def solutionGenerator():
	pass


def solveProblem(filename):
	setup(filename)
	solutionGenerator()

def main():
	if(len(argv) != 5):
		print("Running all game boards with default conditions")
		print("Player 1 - " + player1 + ", type " + player1type)
		print("Player 2 - " + player2 + ", type " + player2type)

	print("Player 1 goes first.")
	
	solveProblem('game_boards/Keren.txt')
	solveProblem('game_boards/Narvik.txt')
	solveProblem('game_boards/Sevastopol.txt')
	solveProblem('game_boards/Smolensk.txt')
	solveProblem('game_boards/Westerplatte.txt')


if __name__ == '__main__':
	main()