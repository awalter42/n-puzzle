import sys
import argparse
from time import time
from solvability import isSolvable
from solver import solv, findCoordinates, getScore


class bcolors:
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	PURPLE = '\033[95m'
	ORANGE = '\033[93m'
	ENDC = '\033[0m'


def makeGoal(s):
	ts = s*s
	puzzle = [-1 for i in range(ts)]
	cur = 1
	x = 0
	ix = 1
	y = 0
	iy = 0
	while True:
		puzzle[x + y*s] = cur
		if cur == 0:
			break
		cur += 1
		if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y*s] != -1):
			iy = ix
			ix = 0
		elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y+iy)*s] != -1):
			ix = -iy
			iy = 0
		x += ix
		y += iy
		if cur == s*s:
			cur = 0

	return puzzle


def extractPuzzle(original: str)->list:
	size = -1

	tab = original.split('\n')
	puzzle = []
	for l in tab:
		try:
			sharp = l.index('#')
			l = l[:sharp]
		except:
			pass
		l = l.split()
		puzzle.append(l)
		if (len(l) > size):
			size = len(l)
	it = 0
	while it < len(puzzle):
		if len(puzzle[it]) <= 2:
			puzzle.pop(it)
		elif len(puzzle[it]) != size:
			print("there is a problem in the puzzle input")
			exit()
		else:
			it += 1
	if (len(puzzle) != size):
		print("there is a problem in the puzzle input")
		exit()
	flatten = [j for sub in puzzle for j in sub]
	for i in range (size*size):
		if str(i) not in flatten:
			print(f'{i} not in input')
			exit()
	return [puzzle, size]


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=str)
	parser.add_argument("-m", "--manhattan", action="store_true", default=False, help='manhattan distance')
	parser.add_argument("-H", "--hamming", action="store_true", default=False, help='hamming distance')
	parser.add_argument("-l", "--linear", action="store_true", default=False, help='manhattan distance with linear conflicts')
	args = parser.parse_args()

	if (args.manhattan and args.hamming) or (args.manhattan and args.linear) or (args.linear and args.hamming):
		print('cannot execute 2 or more heuristics at the same time')
		exit()

	heuristic = 0
	if args.hamming:
		heuristic = 1
	if args.linear:
		heuristic = 2

	f = open(args.file, 'r')
	original = f.read()

	puzzle, size = extractPuzzle(original)
	goal = makeGoal(size)

	if (not isSolvable(puzzle, goal, size)):
		print('puzzle is unsolvable')
		exit()

	if getScore(puzzle, goal, size, heuristic) == 0:
		print('puzzle is already solved')
		exit()

	start = time()
	moves, space, selection = solv(puzzle, size, goal, heuristic)
	end = time()

	print (f"Solving the puzzle took {bcolors.GREEN}{end - start}{bcolors.ENDC} seconds")
	print (f"The cost was {bcolors.BLUE}{len(moves)}{bcolors.ENDC} moves\n")
	print (f"{bcolors.PURPLE}{selection}{bcolors.ENDC} states were selected in the opened set")
	print (f"{bcolors.ORANGE}{space}{bcolors.ENDC} states were represented in the memory at the same time\n")

	for l in puzzle:
		print(' '.join(l))
	print()

	for m in moves:
		x1, y1 = findCoordinates(puzzle, size, '0')
		x2, y2 = findCoordinates(puzzle, size, m)
		puzzle[y1][x1], puzzle[y2][x2] = puzzle[y2][x2], puzzle[y1][x1]

		for l in puzzle:
			print(' '.join(l))
		print()
