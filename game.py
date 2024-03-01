import sys
import argparse
import pygame
# from frame import Frame


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


# class Puzzle:
# 	def __init__(self, screen):
# 		self.screen = screen
# 		self.running = True
# 		self.FPS = pygame.time.Clock()
# 		self.is_arranged = False
# 		self.font = pygame.font.SysFont("Courier New", 33)
# 		self.background_color = (255, 174, 66)
# 		self.message_color = (17, 53, 165)


# 	def _draw(self, frame):
# 		# frame.draw(self.screen)
# 		pygame.display.update()


# 	def main(self, frame_size):
# 		self.screen.fill("white")
# 		frame = Frame(frame_size)
# 		self._instruction()
# 		while self.running:
# 			for event in pygame.event.get():
# 				if event.type == pygame.QUIT:
# 					self.running = False
# 			self._draw(frame)
# 			self.FPS.tick(30)
# 		pygame.quit()


def modify_puzzle(x, y, puzzle, size):
	if (puzzle[y][x] == '0'):
		return False
	if (y+1 < size and puzzle[y+1][x] == '0'):
		puzzle[y+1][x], puzzle[y][x] = puzzle[y][x], puzzle[y+1][x]
		return True
	if (y-1 >= 0 and puzzle[y-1][x] == '0'):
		puzzle[y-1][x], puzzle[y][x] = puzzle[y][x], puzzle[y-1][x]
		return True
	if (x+1 < size and puzzle[y][x+1] == '0'):
		puzzle[y][x+1], puzzle[y][x] = puzzle[y][x], puzzle[y][x+1]
		return True
	if (x-1 >= 0 and puzzle[y][x-1] == '0'):
		puzzle[y][x-1], puzzle[y][x] = puzzle[y][x], puzzle[y][x-1]
		return True
	return False


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("file", type=str)
	args = parser.parse_args()

	f = open(args.file, "r")
	original = f.read()
	puzzle, size = extract_puzzle(original)
	flatten = [j for sub in puzzle for j in sub]
	no_zero = [n for n in flatten if n != '0']

	pygame.init()
	pygame.font.init()
	my_font = pygame.font.SysFont('Courier New', 30)

	window_size = (150*size, 150*size)
	screen = pygame.display.set_mode(window_size)
	pygame.display.set_caption("n-puzzle")


	pygame.display.update()
	text = []
	for i in range (1, size*size):
		text.append(my_font.render(f'{i}', True, (255, 255, 255)))

	running = True
	while running:
		screen.fill((0,0,0))
		for e, txt in enumerate(text):
			i = flatten.index(str(e+1))
			# print()
			screen.blit(text[e], ((i%size) * 150 + 70, (i//size) * 150 + 70))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = event.pos
				x, y = x//150, y//150
				if modify_puzzle(x, y, puzzle, size) == True:
					flatten = [j for sub in puzzle for j in sub]
					no_zero = [n for n in flatten if n != '0']
		pygame.display.update()
	pygame.quit()
