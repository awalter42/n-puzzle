
def taxicabDistance(flatten: list, goal: list, size: int)->int:
	p_index = flatten.index('0')
	p1, p2 = p_index%size, p_index//size
	q_index = goal.index(0)
	q1, q2 = q_index%size, q_index//size
	return abs(p1 - q1) + abs(p2 - q2)


def nb_inversion(flatten: list, goal: list, size: int)->int:
	nb_inversion = 0
	for i in range(len(flatten)):
		vi = int(flatten[i])
		for j in range(i + 1, len(flatten)):
			vj = int(flatten[j])
			if (goal.index(vi) > goal.index(vj)):
				nb_inversion += 1
	return nb_inversion

def isSolvable(puzzle: list, goal: list, size: int)->bool:
	flatten = [j for sub in puzzle for j in sub]
	cab = taxicabDistance(flatten, goal, size)
	nbi = nb_inversion(flatten, goal, size)
	if nbi % 2 == cab % 2:
		return True
	return False

