import sys
import argparse
from solvability import isSolvable
from solver import solv


def make_goal(s):
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


def extract_puzzle(original: str)->list:
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
			print("problem")
			exit()
		else:
			it += 1
	return [puzzle, size]


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("file", type=str)
	args = parser.parse_args()

	f = open(args.file, "r")
	original = f.read()

	puzzle, size = extract_puzzle(original)
	goal = make_goal(size)

	if (not isSolvable(puzzle, goal, size)):
		print ("puzzle is unsolvable")
		exit()

	print(f"!!!!!!!{solv(puzzle, size, goal)}")

