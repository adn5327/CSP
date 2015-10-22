from sys import argv
from collections import defaultdict
from array import array
_word_directory = "words/wordlist/"

# This global variable holds the size of the array
_n_array_size = 0
# Using a dictionary to store lists of words for every category
_categories = defaultdict(list)
# Maps a category to the list of spaces in the dictionary
_slots = defaultdict(list)
_solution_template = list()
_category_ids = defaultdict()
_solution_array = list()

__author__ = 'Jakub Klapacz <jklapac2@illinois.edu> and Abhishek Nigam <adnigam2@illinois.edu>'


def is_consistent():
	pass

# to check if it's consistent for the letter based implementation
# when looking at a bucket -- look at every category 
# see if that category has the index of your bucket
# if it does, check whether its the first/second/third index of the category's word (_slots var)
# check whether the assingment including that bucket is valid
# XXX, X__, X_X, __X, XX_, etc
# if at the end you havent returned false, return true

# for the word based implementation
# put a word in place, and then check if their are still possibilities for other words
# do that by analyzing each bucket that you've modified(?!)
# and see if there are still possible words that can be placed in them

# in the other case -- you could look at every category that has not been assigned yet (or only the ones your current category affects!)
# for each of those categories, look at every word and see if it could fit. 
# if you come across a category for which no word fits, then you return false!
# if at the end you haven't returned false, then return true


'''
	Does backtracking search on the puzzle using a letter assignment
'''
def letter_search():
	pass

'''
	Does backtracking search on the puzzle using a word assignment
'''
def word_search():
	pass

'''
	@Parameter : assignment_type = specify which assignment to use for searching
	
	Performs a backtracking search on the puzzle
'''
def backtracking_search(assignment_type):
	# print(_solution_template)
	print(assignment_type)
	assignment_type = "test"
	if assignment_type == 'word':
		word_search()
	else:
		letter_search()

'''
	@Returns:	True if solution assignment
				False otherwise

	Checks for a solution assignment to variables.
		Goes through the necessary categories and checks
		if the word made up of the characters at the 
		related position belongs to that category.
		If it does not, returns false.
		Otherwise it tries the rest of the words.
'''
def is_solution():
	consistent = True
	for category_n in _slots:
		positions = _slots[category_n]
		word = ""
		for index in positions:
			word += _solution_array[index]
		if word not in _categories[category_n]:
			consistent = False
			return consistent
	consistent = True
	return consistent


'''
	Proof of concept for consistency checking, should not be used to actually solve puzzle
'''
def brute():
	while(not is_solution()):
		print(_solution_array)
		if _solution_array[3] == 'Z':
			return
		if _solution_array[2] == 'Z':
			_solution_array[3] = chr(ord(_solution_array[3])+ 1)
			_solution_array[2] = 'A'
		if _solution_array[1] == 'Z':
			_solution_array[2] = chr(ord(_solution_array[2])+ 1)
			_solution_array[1] = 'A'

		_solution_array[1] = chr(ord(_solution_array[1])+ 1)


	print(_solution_array)



'''
	@Parameter	: category = string
	@Returns	: Nothing

	Opens the appropriate <category>.txt file and
		reads all words from the file. Maps this 
		list to corresponding category.
'''
def get_word_list(category):
	cat_filename = _word_directory + category + ".txt"
	category_file = open(cat_filename, "r")
	wordlist = list()
	for line in category_file.readlines():
		wordlist.append(line.rstrip())
	_categories[category] = wordlist
	category_file.close()

'''
	@Parameter	: filename = string
	@Returns	: Nothing

	Will open filename, extract array size
		information and then will load into the wordlist
		dictionary the words from the appropriate category 
		file. Avoids keeping all words from all categories 
		when they aren't necessary.
'''
def process_puzzle(filename):
	if(filename == None):
		raise Exception("No puzzle file provided")
	puzzle_file = open(filename, "r")
	line = puzzle_file.readline()
	_n_array_size = int(line)
	for i in range(_n_array_size + 1):
		_solution_template.append([])
		_solution_array.append('A')
	_solution_array[0] = 0
	lines = puzzle_file.readlines()
	category_id = 0
	for line in lines:
		line = line.rstrip()
		line = line.replace(" ", "")
		category, spots = line.split(":", 1)
		spots = spots.split(",")
		_categories[category] = list()
		_category_ids[category] = category_id
		for index in spots:
			_solution_template[int(index)].append(category_id)
		_slots[category] = list(map(int, spots))
		category_id += 1

	for category in _categories:
		get_word_list(category)

	puzzle_file.close()

def main():
	if(len(argv) != 3):
		print("Usage: main.py <puzzles/puzzle(#).txt> [word] [letter]")
		return
	puzzle_name = argv[1]
	version = argv[2]
	process_puzzle(puzzle_name)
	backtracking_search(version)
	print(version)

if __name__ == "__main__":
	main()
