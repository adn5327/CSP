from sys import argv
filename = argv[1]
file = open(filename)
for cur_line in file.readlines():
	cur_line = cur_line.rstrip()
	if(cur_line != "(Backtracking)"):
		print(cur_line)