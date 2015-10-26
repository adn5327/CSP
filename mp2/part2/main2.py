import time

currentBoard = None #will be a list initialized
scores = None # will be a list initialized
nodesExpanded = [0,0] #initialize this list to be zero for both players at start
mode = [1,1] #1 for minimax, 2 for alphabeta
total_time = [0,0]
total_moves = [0,0]

max_depthab = 4
max_depthmm = 3

minint = -10000
maxint = 10000

turn = 1

curplayer = 'blue'
otherplayer = 'green'

def main():
	all()
	# global turn
	# global mode
	# turn = 1
	# mode = [0,0]
	# start('Keren')
def all():
	all_one('Keren')
	all_one('Narvik')
	all_one('Sevastopol')
	all_one('Smolensk')
	all_one('Westerplatte')

def all_one(boardy):
	global turn
	global mode

	turn = 1
	mode =[1,1]

	print boardy
	print ('minimax vs minimax\n')
	start(boardy)

	turn = 1
	mode =[2,2]

	print boardy
	print ('alpha-beta vs alpha-beta\n')
	start(boardy)

	turn = 1
	mode =[1,2]
	print boardy
	print ('minimax vs alpha-beta -- minimax goes first\n')
	start(boardy)

	turn = 1
	mode =[2,1]
	print boardy
	print ('alpha-beta vs minimax -- alpha-beta goes first\n')
	start(boardy)


def start(boardy):
	global turn
	nodesExpanded[0] = 0
	nodesExpanded[1] = 0
	total_moves[0] = 0
	total_moves[1] = 0
	total_time[0] = 0
	total_time[1] = 0

	read_from_file(boardy)

	turn = 2
	curplayer = 'green'
	otherplayer = 'blue'
	setup_p1()

def formatted_print(boardy):
	for i in range(len(currentBoard)):
		string = ''
		otherstring = ''
		for j in range(len(currentBoard[i])):
			if currentBoard[i][j] == 1: string += 'B\t'
			elif currentBoard[i][j] == 2: string += 'G\t'
			else: string += 'N\t'
			otherstring += str(scores[i][j])
			otherstring += '\t'
		print '{}\t\t\t\t\t{}'.format(string, otherstring)

def playgame(turny):
	global currentBoard
	temp = None
	if(mode[2-turny] == 2):
		temp = alphabeta(currentBoard, scores, turny, 0, 1, 3-turn, minint, maxint)
	elif(mode[2-turny] == 1):
		temp = minimax(currentBoard, scores, turny, 0 , 1, 3-turn)
	elif(mode[2-turny] == 0):
		formatted_print(currentBoard)
		#they will externally think that it is X, but internally it is Y -- they are flipped
		y = int(input('Enter X Coordinate >>: '))
		x = int(input('Enter Y Coordinate >>: '))
		temp = (0,x,y)

	movetoi = temp[1]
	movetoj = temp[2]
	# print(movetoi)
	# print (movetoj)
	# print currentBoard[movetoi][movetoj]
	if currentBoard[movetoi][movetoj] == -1:
		currentBoard[movetoi][movetoj] = 3-turny
		taker = can_take(currentBoard, 3-turny, movetoi, movetoj)
		# print taker
		if taker[0]:
			currentBoard = take_it(currentBoard, turny, movetoi, movetoj)
			# print('hello')

def setup_p1():
	global turn
	global curplayer
	global otherplayer
	global currentBoard
	total_moves[2-turn] += 1
	start = time.time()
	playgame(turn)
	done = time.time()
	total_time[2-turn] += done-start
	# print(currentBoard)
	if isFull(currentBoard):
		print_winner()
		return
	else:
		turn = 3 -turn
		temp = curplayer
		curplayer = otherplayer
		otherplayer = temp
		setup_p2()

def setup_p2():
	global turn
	global curplayer
	global otherplayer
	global currentBoard
	total_moves[2-turn] += 1
	start = time.time()
	playgame(turn)
	done = time.time()
	total_time[2-turn] += done-start
	# print(currentBoard)
	if isFull(currentBoard):
		print_winner()
		return
	else:
		turn = 3 -turn
		temp = curplayer
		curplayer = otherplayer
		otherplayer = temp
		setup_p1()

def minimax(board, scores, turny, minimax_val, depth, player):
	
	nodesExpanded[player-1] +=1
	if depth > max_depthmm or isFull(board):
		return (utility_func(board, player, scores), -1, -1)
	
	bestval = 0
	if minimax_val == 0:
		bestval = minint
	else:
		bestval = maxint

	x_coord = -1
	y_coord = -1

	# may want to move this to a numerical for loop
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == -1:
				temp_board = copy_board(board)
				temp_board[i][j] = 3 - turny #this player has captured the space!
				taker = can_take(temp_board, 3-turny, i, j)
				if taker[0]:
					take_it(temp_board, turny, i, j)
				result = minimax(temp_board, scores, 3-turny, 1-minimax_val, depth+1, player)
				if minimax_val == 0:
					if result[0] > bestval:
						bestval = result[0]
						x_coord = i
						y_coord = j
				else:
					if result[0] < bestval :
						bestval = result[0]
						x_coord = i
						y_coord = j
	return (bestval, x_coord, y_coord)

def alphabeta(board, scores, turny, minimax_val, depth, player, alpha, beta):
	nodesExpanded[player-1] += 1
	if depth > max_depthab or isFull(board):
		return (utility_func(board, player, scores), -1, -1)
	besti = 0
	bestj = 0
	if minimax_val == 0:
		besti = 1000
		bestj = 1000
	else:
		besti = -1
		bestj = -1
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == -1:
				temp_board = copy_board(board)
				temp_board[i][j] = 3-turny
				taker = can_take(temp_board, 3-turny, i, j)
				if taker[0]:
					take_it(temp_board, turny, i, j)

				result = alphabeta(temp_board, scores, 3-turny, 1-minimax_val, depth+1, player, alpha, beta)
				if minimax_val == 0:
					if alpha < result[0]:
						alpha = result[0]
						besti = i
						bestj = j
					if beta <= alpha:
						return (alpha, besti, bestj)
				else:
					if beta > result[0]:
						beta = result[0]
						besti = i
						bestj = j
					if beta <= alpha:
						return (beta, besti, bestj)
	if minimax_val == 0:
		return (alpha, besti, bestj)
	return (beta, besti, bestj)

def print_winner():
	p1 = score_calc(1)
	p2 = score_calc(2)

	if p1 > p2:
		print 'Blue wins'
	elif p2 > p1:
		print 'Green wins'
	else:
		print 'Tie game'

	print "Blue score:\t\t\t{}\tGreen score:\t{}".format(p1,p2)
	print "Blue moves:\t\t\t{}\tGreen moves:\t{}".format(total_moves[0], total_moves[1])
	print "Blue Average Nodes/Move:\t{}\tGreen Average Nodes/Move:\t{}".format(nodesExpanded[0]/total_moves[0], nodesExpanded[1]/total_moves[1])
	print "Blue Average Time/Move:\t{}\tGreen Average Time/Move:\t{}".format(total_time[0]/total_moves[0], total_time[0]/total_moves[0])
	global currentBoard
	formatted_print(currentBoard)
	
	print('\n\n')

	return

def score_calc(player):
	scorey = 0
	for i in range(len(currentBoard)):
		for j in range(len(currentBoard[i])):
			if currentBoard[i][j] == player:
				scorey += scores[i][j]
	return scorey



def can_take(board, turny, i, j):
	if i-1>=0 :
		if board[i-1][j] == turny: return (True, i-1, j)
	if i+1 <len(board) :
		if board[i+1][j] == turny: return (True, i+1, j)
	if j-1 >= 0 :
		if board[i][j-1] == turny: return (True, i, j-1)
	if j+1 < len(board):
		if board[i][j+1] == turny: return (True, i, j+1)
	return (False, -1, -1)

def take_it(board, turny, i, j):
	if i-1>=0 :
		if board[i-1][j] == turny: board[i-1][j] = 3 -turny
	if i+1 <len(board) :
		if board[i+1][j] == turny: board[i+1][j] = 3 -turny
	if j-1 >= 0 :
		if board[i][j-1] == turny: board[i][j-1] = 3 -turny
	if j+1 < len(board):
		if board[i][j+1] == turny: board[i][j+1] = 3 -turny
	# print(board)
	return board


def isFull(board):
	for listy in board:
		for val in listy:
			if val == -1:
				return False
	return True

def utility_func(board, player, scores):
	p1 = 0
	p2 = 0
	for i in range(len(currentBoard)):
		for j in range(len(currentBoard)):
			if board[i][j] == 1: p1 += scores[i][j]
			elif board[i][j] == 2: p2 += scores[i][j]

	if player == 1:
		return p1 -p2
	elif player == 2:
		return p2 -p1

def copy_board(board):
	new_list = list()
	for i in range(len(board)):
		new_list.append(list())
		for j in range(len(board)):
			ijval = board[i][j]
			new_list[i].append(ijval)

	return new_list

def read_from_file(board_name):
	global scores
	global currentBoard

	currentBoard = list()
	currentBoard[:] = []
	scores = list()
	scores[:] = []

	if(board_name == None):
		raise Exception("No board provided!!!")
	board_file = open('game_boards/' + board_name + '.txt', "r")

	#this puts every line into a matrix
	string_matrix = list()
	all_lines = board_file.read().splitlines()
	for listy in all_lines:
		string_matrix.append(listy.split())
	
	# matrix finally holds the game board 
	# elements can be accessed with int_matrix[0][0]
	# each row is a list
	# coordinates are therefore y,x -- 0 indexed
	
	scores = [map(int, x) for x in string_matrix]
	for i in range(len(scores)):
		 currentBoard.append([])
		 for j in range(len(scores[i])):
		 	currentBoard[i].append(-1)



def setBoard(boardy):
	global scores
	global currentBoard

	if boardy == 'Keren':
		scores = [ [1, 1,	1,	1,	1,	1],[1,	1,	1,	1,	1,	1],[1,	1,	1,	1,	1,	1],[1,	1,	1,	1,	1,	1],[1,	1,	1,	1,	1,	1],[1,	1,	1,	1,	1,	1]]
		currentBoard = [ [-1, -1,-1,-1,	-1,	-1],[-1,-1,	-1,	-1,	-1,	-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]]
	elif boardy == 'Narvik':
		scores = [[99,1,99,1,99,1],[1,99,1,99,1,99],[99,1,99,1,99,1],[1,99,1,99,1,99],[99,1,99,1,99,1],[1,99,1,99,1,99]]
		currentBoard = [ [-1, -1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]]

	elif boardy == 'Sevastopol':
		scores = [[1,1,1,1,1,1],[2,2,2,2,2,2],[4,4,4,4,4,4],[8,8,8,8,8,8],[16,16,16,16,16,16],[32,32,32,32,32,32]]
		currentBoard = [ [-1, -1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,	-1]]

	elif boardy == 'Smolensk':
		scores = [[66,76,28,66,11,9],[31,39,50,8,33,14],[80,76,39,59,2,48],[50,73,43,3,13,3],[99,45,72,87,49,4],[80,63,92,28,61,53]]
		currentBoard = [ [-1, -1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]]

	elif boardy == 'Westerplatte':
		scores = [[1,1,1,1,1,1],[1,3,4,4,3,1],[1,4,2,2,4,1],[1,4,2,2,4,1],[1,3,4,4,3,1],[1,1,1,1,1,1]]
		currentBoard = [ [-1, -1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]]


if __name__ == '__main__':
	main()