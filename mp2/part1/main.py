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

_search_iterations = 0
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

'''
	@Parameters	:	category_id = integer representing category to search in
					letter = letter that needs to be in a category's word's index position
					index = position in word that letter must appear
	@returns 	:	word_list = a list of words that have letter appearing at index 
'''
def pos_get_word_list(category_id, letter, index):
	all_words = _categories[_category_ids[category_id]]
	word_list = list()
	for word in all_words:
		if(word[index] == letter):
			word_list.append(word)
	return word_list

'''
	@Parameters	:	letter = letter assignment we want to make
					index = position in the solution array we want to check
					check_against = local copy of current solution array state
	@Returns 	:	True if assignment would be consistent, false otherwise
	This function determines whether choosing a letter assignment in a particular
		location in the solution function would be consistent/inconsistent
'''
def is_consistent_letter(letter, index, check_against):
	categories_list = _solution_template[index]
	for category_id in categories_list:
		letter_pos = _slots[_category_ids[category_id]].index(index)
		word_list = pos_get_word_list(category_id, letter, letter_pos)
		if (word_list == []):
			return False
		correct_word = ""
		for i in range(letter_pos):
			correct_word += check_against[_slots[_category_ids[category_id]][i]]
			if(any(correct_word in string for string in word_list) == False):
				return False

	return True

'''
	@Parameters :	category = string, represents category we want to check
					word = potential word assignment we want to make
					check_against = local copy of solution array
	@Returns 	:	True if consistent assignment, false otherwise
'''
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
	print("\nSearching in order of indicies in the solution array [0] ... [{}]".format(str(_n_array_size - 1)))
	if(_trace):
		stdout.write("root")
	letter_search_helper(0, _solution_array, 0)
	print("Search Iterations: " + str(_search_iterations) + "\n")

'''
	@Parameters 	:	index = index of solution array to work on (starts at 0)
						passed_array = local copy of solution
						depth = depth of recursion, which variable is being worked on
	@Returns 		: 	True if solution is found, otherwise returns false
	This function is a helper function for letter-based search.
'''
def letter_search_helper(index, passed_array, depth):
	global _search_iterations
	_search_iterations += 1
	local_array = list(passed_array)
	if(index == len(_domain)):
		global _solution_array
		_solution_array = list(local_array)
		return choose_print()

	if(index >= len(_domain)): return False
	checker_array = list(local_array)
	for each_letter in _domain[index]:
		if(is_consistent_letter(each_letter, index, checker_array)):
			local_array[index] = each_letter
			if(_trace):
				stdout.write("[" + str(depth) + "]")
				stdout.write("->" + each_letter)
			solution = letter_search_helper(index+1, local_array, depth+1)
			if(_trace and solution == False):
				stdout.write("(Backtracking)\n")
	return False

	
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
	stdout.write("\nSearching in order of categories: ")
	for i in range(_num_categories):
		stdout.write(_category_ids[i] + " ")
	stdout.write("\n")
	if(_trace):
		stdout.write("root")
	word_search_helper(0, _solution_array, 0)
	print("Search Iterations: " + str(_search_iterations) + "\n")

'''
	@Parameters 	:	category_int = integer of category we want to assign to (start with 0)
						passed_array = state of the solution array we want to operate on
						depth = depth of recursion, basically which category are we working on 
	@Returns 		: 	True if the assignment is a solution, false otherwise
	This is a helper function that searches for solution(s) to the puzzle using word assignments
'''
def word_search_helper(category_int, passed_array, depth):
	global _search_iterations
	_search_iterations += 1
	local_array = list(passed_array)
	if(category_int == _num_categories):
		# if(at_full_assignment()):
		global _solution_array
		_solution_array = list(local_array)
		return choose_print()
		# return
	if(category_int >= _num_categories): return	False
	cur_category = _category_ids[category_int]
	checker_array = list(local_array)
	# if(at_full_assignment()):
		# print(checker_array)
	for each_word in _categories[cur_category]:
		if(is_consistent_word(cur_category, each_word, checker_array)):
			# print(each_word)
			assign_word(cur_category, each_word, local_array)
			# for i in range(depth + 1):
				# stdout.write("")
				# stdout.write("(" + str(i) +")")
			if(_trace):
				stdout.write("[" + str(depth) + "]")
				stdout.write("->" + each_word)
			# print(' '.join(_solution_array))
			# stdout.write('\n')
			solution = word_search_helper(category_int+1, local_array, depth+1)
			if(_trace and solution == False):
				stdout.write("(Backtracking)\n")

	# stdout.write("\t(Backtracking)\n")
	return False

'''
	@Parameters 	:	cur_category = string, current category to be assigning to
						each_word = word that we want to assign into the solution array
						passed_array = local copy of solution array 
	This Function puts a category's word into the proper slots in the solution array
'''
def assign_word(cur_category, each_word, passed_array):
	idx_list = _slots[cur_category]
	for i in range(len(idx_list)):
		passed_array[idx_list[i]] = each_word[i]

'''
	@Returns :	False if any index in the solution array has not been assigned, true otherwise
'''
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

'''
	@returns 	: 	True if assignment is solution, false otherwise
	Helper function, calls solution checker and outputs some text.
'''
def choose_print():
	if(is_solution()):
		print_solution()
		_solution_map.append(_solution_array)
		# print(_solution_array)
		return True
	# if(_trace): stdout.write("Backtracking\n")
	if(_trace): 
		stdout.write("(Backtracking)\n")
	return False

'''
	Helper function to correctly format a found solution
'''
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

'''
	Main function, creates a puzzle based on .txt input and solves it
'''
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