from sys import argv
from collections import defaultdict
from array import array
from sys import stdout
_word_directory = "words/wordlist/"

#Print out the search trace if true, if false just print solution(s) (if found)
_trace = False
# This global variable holds the size of the array
_n_array_size = 0
# Using a dictionary to store lists of words for every category
# string (category) --> list of words for that category
_categories = defaultdict(list)

# maps a string (category) --> list of three integers - the SLOTS
_slots = defaultdict(list)


# values from category id
_solution_template = list()

#merely maps integer id of category to the actual string ()
_category_ids = defaultdict()

#at the end of infrastructure generation, this will hold the number of categories (1 indexed)
_num_categories = 0

_solution_array = list()

# List of lists that will hold valid domain values (for the puzzle's index)
_domain = list()

_solution_map = list()

__author__ = 'Jakub Klapacz <jklapac2@illinois.edu> and Abhishek Nigam <adnigam2@illinois.edu>'





'''
	@Parameter	:	category_id = integer representing category_id
				:	index = integer representing the letter at position index
	@Returns 	: 	list of letters in every index'th position in all words of a category
'''
def get_letter_list(category_id, index):
	word_list = _categories[_category_ids[category_id]]
	letter_list = list()
	for word in word_list:
		letter_list.append(word[index])
	return letter_list

'''
	@Parameter	:	category_id = integer representing category_id
				: 	index = index in solution array
	@returns 	: 	position 
	Given a category id (int) and the index in the solution array
	This function returns which position in the category is 
	associated with that index.
'''
def cat_index_to_pos(category_id, index):
	cat = _slots[_category_ids[category_id]]
	for i in range(3):
		if cat[i] == index:
			return i
	return -1

'''
	@Parameter	:	index = integer that corresponds to the index in the solution array
	@Return 	: 	actual_list = list of domain values for the given index
	Function that returns a list of domain values that are valid for every category
	associated with the index. 
'''
def get_domain_values(index):
	possible_lists = list()
	for category_id in _solution_template[index]:
		letter_index = cat_index_to_pos(category_id, index)
		possible_lists.append(get_letter_list(category_id, letter_index))
	actual_list = set(possible_lists[0]).intersection(*possible_lists)
	actual_list = list(actual_list)
	actual_list.sort()
	return actual_list

'''
	Function to generate the domain for every solution index (letter based)
'''
def create_domain():
	for i in range(len(_solution_array)):
		_domain.append(get_domain_values(i))
	# print(len(_solution_array))
	# print()
	# print(_domain)
	# print()
	# print(_solution_template)

def is_consistent():
	pass

def is_consistent_word(category, word, check_against):
	idx_list = _slots[category]
	# print(category)
	# stdout.write(''.join(check_against))
	for i in range(len(idx_list)):
		idx_val = check_against[idx_list[i]]
		if(idx_val != '0' and idx_val != word[i]): 
			# quit()
			# print(False)
			# stdout.write('\n') 
			return False


	# print(True)

	# stdout.write('\n') 

	return True

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
	create_domain()
	letter_search_helper(0)

def letter_search_helper(index):
	if(index == len(_domain)):
		choose_print()

	if(index >= len(_domain)): return False

	for each_letter in _domain[index]:
		_solution_array[index] = each_letter
		letter_search_helper(index+1)

	return True

	
# After generating a list of potential letters for a bucket:
# 1. Start at first bucket
# 2. Pop a letter of the list of possible values for that bucket
# 3. Check if assigning that letter to that bucket is possible
# 		Do so using the is consistent method
# 4. If it is consistent:
# 		Assign that letter
# 		Call recursive backtracking on the next bucket
# 5. If it is not consistent
#		return -- that way you try a different value for that current bucket
# If you have a found a solution (AKA all buckets are filled & isconsistent)
# 		print solution
# 		return -- that way you try a different value for that current bucket
'''
	Does backtracking search on the puzzle using a word assignment
'''
def word_search():
	word_search_helper(0, _solution_array)

def word_search_helper(category_int, passed_array):
	local_array = list(passed_array)
	if(category_int == _num_categories):
		# if(at_full_assignment()):
		global _solution_array
		_solution_array = list(local_array)
		choose_print()
		# return
	if(category_int >= _num_categories): return	

	cur_category = _category_ids[category_int]
	checker_array = list(local_array)
	# if(at_full_assignment()):
		# print(checker_array)
	for each_word in _categories[cur_category]:
		if(is_consistent_word(cur_category, each_word, checker_array)):
			# print(each_word)
			assign_word(cur_category, each_word, local_array)
			# print(' '.join(_solution_array))
			# stdout.write('\n')
			word_search_helper(category_int+1, local_array)

	return


def assign_word(cur_category, each_word, passed_array):
	idx_list = _slots[cur_category]
	for i in range(len(idx_list)):
		passed_array[idx_list[i]] = each_word[i]






def at_full_assignment():
	for x in _solution_array:
		if(x == '0'): 
			return False
	return True

'''
	@Parameter : assignment_type = specify which assignment to use for searching
	
	Performs a backtracking search on the puzzle
'''
def backtracking_search(assignment_type):

	if assignment_type == 'word':
		word_search()
	else:
		letter_search()
		# print(_domain)

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


def choose_print():
	if(is_solution()):
		print_solution()
		_solution_map.append(_solution_array)
		# print(_solution_array)
		return True
	if(_trace): stdout.write("Backtracking\n")
	return False

def print_solution():
	stdout.write("(Found result: ")
	stdout.write(''.join(_solution_array)) 
	stdout.write(')\n')

'''
	Proof of concept for consistency checking, should not be used to actually solve puzzle
'''
def brute():
	# while(not is_solution()):
	# 	print(_solution_array)
	# 	if _solution_array[3] == 'Z':
	# 		return
	# 	if _solution_array[4] == 'Z':
	# 		_solution_array[3] = chr(ord(_solution_array[3])+ 1)
	# 		_solution_array[4] = 'A'
	# 	if _solution_array[3] == 'Z':
	# 		_solution_array[2] = chr(ord(_solution_array[3])+ 1)
	# 		_solution_array[3] = 'A'		
	# 	if _solution_array[2] == 'Z':
	# 		_solution_array[3] = chr(ord(_solution_array[3])+ 1)
	# 		_solution_array[2] = 'A'
	# 	if _solution_array[1] == 'Z':
	# 		_solution_array[2] = chr(ord(_solution_array[2])+ 1)
	# 		_solution_array[1] = 'A'

	# 	_solution_array[1] = chr(ord(_solution_array[1])+ 1)
	
	print(is_solution())
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
	global _n_array_size
	_n_array_size = int(line)
	for i in range(_n_array_size):
		_solution_template.append([])
		_solution_array.append('0')
	lines = puzzle_file.readlines()
	global _num_categories
	for line in lines:
		line = line.rstrip()
		line = line.replace(" ", "")
		category, spots = line.split(":", 1)
		spots = spots.split(",")
		_categories[category] = list()
		_category_ids[_num_categories] = category
		for index in spots:
			_solution_template[int(index) - 1].append(_num_categories)
		_slots[category] = list(map(int, spots))
		_slots[category][:] = [x - 1 for x in _slots[category]]
		_num_categories += 1


	for category in _categories:
		get_word_list(category)
	puzzle_file.close()

def main():
	if(len(argv) != 4):
		print("Usage: main.py <puzzles/puzzle(#).txt> {[word], [letter]} {[trace], [notrace]}")
		return
	puzzle_name = argv[1]
	version = argv[2]
	if(argv[3] == "trace"):
		global _trace
		_trace = True
	process_puzzle(puzzle_name)
	backtracking_search(version)
	

if __name__ == "__main__":
	main()