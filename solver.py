def find_coordinates(puzzle: list, size: int):
	for y in range(size):
		for x in range(size):
			if puzzle[y][x] == '0':
				return (x, y)


def manhattanDistance(flatten: list, goal: list, size: int, element: int):
	p_index = flatten.index(str(element))
	p1, p2 = p_index%size, p_index//size
	q_index = goal.index(element)
	q1, q2 = q_index%size, q_index//size
	return abs(p1 - q1) + abs(p2 - q2)


def getScore(puzzle: list, goal: list, size: int):
	score = 0
	flatten = [j for sub in puzzle for j in sub]
	for i in range(size**2):
		score += manhattanDistance(flatten, goal, size, i)
	return score


def move_up(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y - 1][x]
	temp[y][x], temp[y - 1][x] = temp[y - 1][x], temp[y][x]
	return temp, act


def move_down(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y + 1][x]
	temp[y][x], temp[y + 1][x] = temp[y + 1][x], temp[y][x]
	return temp, act


def move_left(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y][x - 1]
	temp[y][x], temp[y][x - 1] = temp[y][x - 1], temp[y][x]
	# print (temp)
	# print (state)
	return temp, act


def move_right(state: list, size: int, x: int, y: int):
	temp = [l[:] for l in state]
	act = temp[y][x + 1]
	temp[y][x], temp[y][x + 1] = temp[y][x + 1], temp[y][x]
	return temp, act


def insertState(temp: list, goal: list, size: int, states: list, all_states: list, moves: list, scores: int, action: str, copy: list):
	if temp in all_states:
		return states, moves, scores
	index = states.index(copy)
	new_move = moves[index][:]
	new_move.append(action)
	new_score = getScore(temp, goal, size) * (size-2) + len(new_move)
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
	if (len(scores) >= size * 10):
		states.pop(-1)
		moves.pop(-1)
		scores.pop(-1)
	return states, moves, scores



def solv(puzzle: list, size: int, goal: list) -> list:
	states = [puzzle, ]
	all_states = [puzzle, ]
	moves = [[]]
	scores = [getScore(puzzle, goal, size) * (size-2), ]

	good = False
	action = ''


	# t = 0
	while (True):
		copy = [l[:] for l in states[0]]
		x, y = find_coordinates(states[0], size)
		if (y > 0):
			index = states.index(copy)
			temp, action = move_up(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy)
			all_states.append([l[:] for l in temp])
		if (y < size - 1):
			index = states.index(copy)
			temp, action = move_down(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy)
			all_states.append([l[:] for l in temp])
		if (x > 0):
			index = states.index(copy)
			temp, action = move_left(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy)
			all_states.append([l[:] for l in temp])
		if (x < size - 1):
			index = states.index(copy)
			temp, action = move_right(states[index], size, x, y)
			states, moves, scores = insertState(temp, goal, size, states, all_states, moves, scores, action, copy)
			all_states.append([l[:] for l in temp])
		index = states.index(copy)
		states.pop(index)
		moves.pop(index)
		scores.pop(index)
		if scores[0] - len(moves[0]) == 0:
			print(len(scores))
			print (states[0])
			return moves[0]
		# print((scores[0] - len(moves[0])) // 2)