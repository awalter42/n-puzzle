#https://theory.stanford.edu/~amitp/GameProgramming/Variations.html
#https://en.wikipedia.org/wiki/A*_search_algorithm

def findCoordinates(puzzle: list, size: int, n: str):
	for y in range(size):
		for x in range(size):
			if puzzle[y][x] == n:
				return (x, y)


def manhattanDistance(flatten: list, goal: list, size: int, element: int):
	p_index = flatten.index(str(element))
	p1, p2 = p_index%size, p_index//size
	q_index = goal.index(element)
	q1, q2 = q_index%size, q_index//size
	return abs(p1 - q1) + abs(p2 - q2)


def	misplacedTiles(flatten: list, goal: list):
	score = 0
	for i, t in enumerate(flatten):
		if t != str(goal[i]):
			score += 1
	return score


def	linearConflict(flatten: list, puzzle: list, goal: list, size: list):
	nb_conflict = 0
	built_goal = [goal[size*i:size*(i+1)] for i in range(size + 1)]

	for y, l in enumerate(puzzle):
		for i, e in enumerate(l):
			try:
				goal_index = built_goal[y].index(int(e))
				if goal_index > i:
					for element in l[i:goal_index + 1]:
						try:
							ele_index = built_goal[y].index(int(element))
							if ele_index <= i:
								nb_conflict += 1
						except:
							pass
			except:
				pass

	r_puzzle = list(zip(*puzzle[::-1]))
	r_goal = list(zip(*built_goal[::-1]))

	for y, l in enumerate(r_puzzle):
		for i, e in enumerate(l):
			try:
				goal_index = r_goal[y].index(int(e))
				if goal_index > i:
					for element in l[i:goal_index + 1]:
						try:
							ele_index = r_goal[y].index(int(element))
							if ele_index <= i:
								nb_conflict += 1
						except:
							pass
			except:
				pass

	return (nb_conflict * 2)

			
def getScore(puzzle: list, goal: list, size: int, heuristic: int):
	score = 0
	flatten = [j for sub in puzzle for j in sub]
	if heuristic == 0:
		for i in range(size**2):
			score += manhattanDistance(flatten, goal, size, i)

	elif heuristic == 1:
		score = misplacedTiles(flatten, goal)

	elif heuristic == 2:
		for i in range(size**2):
			score += manhattanDistance(flatten, goal, size, i)
		score += linearConflict(flatten, puzzle, goal, size)

	return score


def moveUp(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y - 1][x]
	temp[y][x], temp[y - 1][x] = temp[y - 1][x], temp[y][x]
	return temp, act


def moveDown(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y + 1][x]
	temp[y][x], temp[y + 1][x] = temp[y + 1][x], temp[y][x]
	return temp, act


def moveLeft(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y][x - 1]
	temp[y][x], temp[y][x - 1] = temp[y][x - 1], temp[y][x]
	return temp, act


def moveRight(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y][x + 1]
	temp[y][x], temp[y][x + 1] = temp[y][x + 1], temp[y][x]
	return temp, act


def insertState(temp: list, goal: list, size: int, states: list, all_states: list, moves: list, scores: int, action: str, copy: list, heuristic: int):
	if temp in all_states:
		return states, moves, scores
	index = states.index(copy)
	new_move = moves[index][:]
	new_move.append(action)
	new_score = getScore(temp, goal, size, heuristic) * (size-2) + len(new_move)
	for i, s in enumerate(scores):
		if new_score <= s:
			states.insert(i, temp)
			moves.insert(i, new_move)
			scores.insert(i, new_score)
			if (len(scores) >= size * 10):
				states.pop(-1)
				moves.pop(-1)
				scores.pop(-1)
			return states, moves, scores
	states.append(temp)
	moves.append(new_move)
	scores.append(new_score)
	return states, moves, scores



def solv(puzzle: list, size: int, goal: list, heuristic: int) -> list:
	states = [puzzle, ]
	all_states = [puzzle, ]
	moves = [[]]
	scores = [getScore(puzzle, goal, size, heuristic) * (size-2), ]
	action = ''
	selection = 0


	while (True):
		selection += 1
		copy = [l[:] for l in states[0]]
		x, y = findCoordinates(states[0], size, '0')
		if (y > 0):
			index = states.index(copy)
			temp, action = moveUp(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy, heuristic)
			all_states.append([l[:] for l in temp])
		if (y < size - 1):
			index = states.index(copy)
			temp, action = moveDown(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy, heuristic)
			all_states.append([l[:] for l in temp])
		if (x > 0):
			index = states.index(copy)
			temp, action = moveLeft(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy, heuristic)
			all_states.append([l[:] for l in temp])
		if (x < size - 1):
			index = states.index(copy)
			temp, action = moveRight(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy, heuristic)
			all_states.append([l[:] for l in temp])

		index = states.index(copy)
		states.pop(index)
		moves.pop(index)
		scores.pop(index)

		states[:size*10]
		moves[:size*10]
		scores[:size*10]

		if scores[0] - len(moves[0]) == 0:
			return moves[0], len(all_states), selection
