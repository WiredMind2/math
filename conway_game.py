import pygame
import time
import random

class Conway_Game:
	def __init__(self):
		pygame.init()
		pygame.font.init()

		self.size = (1000, 1000)
		self.screen = pygame.display.set_mode(self.size)
		self.font = pygame.font.Font(None, 20)
		
		pygame.display.set_caption("Conway's Game of Life")

		self.bounds = (100, 100)
		self.factor = (self.size[0] / self.bounds[0], self.size[1] / self.bounds[1])
		self.cells = [[False for _ in range(self.bounds[0])] for _ in range(self.bounds[1])]

		if True: # Shapes
			glider = (
				(0, 2),
				(1, 0),
				(1, 2),
				(2, 1),
				(2, 2)
			)

			block = (
				(0, 0),
				(0, 1),
				(1, 0),
				(1, 1)
			)

			diehard = (
				(block, 0, 1),
				(5, 2),
				(6, 0),
				(6, 2),
				(7, 2)
			)

			gosper_glider_gun_1 = (
				(0, 2),
				(0, 3),
				(0, 4),
				(1, 1),
				(1, 5),
				(2, 0),
				(2, 6),
				(3, 0),
				(3, 6),
				(4, 3),
				(5, 1),
				(5, 5),
				(6, 2),
				(6, 3),
				(6, 4),
				(7, 3),
			)

			gosper_glider_gun_2 = (
				(block, 0, 2),
				(block, 0, 3),
				(2, 1),
				(2, 5),
				(4, 0),
				(4, 1),
				(4, 5),
				(4, 6),
			)

			gosper_glider_gun = (
				(block, 0, 4),
				(block, 34, 2),
				(gosper_glider_gun_1, 10, 2),
				(gosper_glider_gun_2, 20, 0)
			)

			almosymmetric = (
				(0, 1),
				(0, 2),
				(0, 5),
				(0, 6),
				(1, 1),
				(1, 4),
				(1, 6),
				(2, 2),
				(3, 6),
				(4, 0),
				(4, 1),
				(5, 6),
				(5, 7),
				(6, 1),
				(7, 3),
				(7, 5),
				(8, 3)
			)

			self.shapes = []
			for n in ("glider", "diehard", "block", "gosper_glider_gun", "almosymmetric"):
				self.shapes.append((n, locals()[n]))


			random_shape = lambda :((x, y) for y in range(self.bounds[1]) for x, cell in enumerate(random.choices((True, False), k=self.bounds[0])) if cell)

		# self.add_shape(glider, 4, 4)
		# self.add_shape(diehard, 50, 50)
		# self.add_shape(gosper_glider_gun, 4, 4)
		self.add_shape(random_shape(), 0, 0)

		self.frame = 0
		self.shape_id = 0
		self.draw()

		delay = 0.1

		loop = True
		paused = False
		mousehold = False
		last = time.time()
		while loop:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						paused = not paused
					elif event.key == pygame.K_RIGHT:
						if not paused:
							paused = True
						self.update_cells()
						self.draw()
					elif event.key == pygame.K_r:
						self.add_shape(random_shape(), 0, 0)
						self.draw()
					elif event.key == pygame.K_k:
						self.cells = [[False for _ in range(self.bounds[0])] for _ in range(self.bounds[1])]
						self.draw()
					elif event.key == pygame.K_h:
						click = pygame.mouse.get_pos()
						x, y = int(click[0] // self.factor[0]), int(click[1] // self.factor[1])
						self.add_shape(self.shapes[self.shape_id][1], x, y)
						self.draw()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 4:
						self.shape_id += 1
						if self.shape_id >= len(self.shapes) - 1:
							self.shape_id = 0
						self.draw()
					elif event.button == 5:
						self.shape_id -= 1
						if self.shape_id < 0:
							self.shape_id = len(self.shapes) - 1
						self.draw()
					elif event.button in (1, 3):
						mousehold = True
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button in (1, 3):
						mousehold = False
				if mousehold:
					click = pygame.mouse.get_pos()
					x, y = int(click[0] // self.factor[0]), int(click[1] // self.factor[1])
					if pygame.mouse.get_pressed()[0]:
						self.cells[x][y] = True
					elif pygame.mouse.get_pressed()[2]:
						self.cells[x][y] = False
					self.draw()
			if not paused and time.time() - last >= delay:
				if self.update_cells():
					self.draw()
					last = time.time()
				else:
					paused = True
		pygame.quit()

	def draw(self):
		self.screen.fill((255, 255, 255))
		for x, row in enumerate(self.cells):
			for y, cell in enumerate(row):
				if cell is True:
					pos = (x * self.factor[0], y * self.factor[1])
					pygame.draw.rect(self.screen, (0, 0, 0), (int(pos[0]), int(pos[1]), int(self.factor[0]), int(self.factor[1])))

		text = self.font.render(str(self.frame) + " - " + self.shapes[self.shape_id][0], True, (10, 10, 10))
		textpos = text.get_rect(x=10, y=10)
		self.screen.blit(text, textpos)

		pygame.display.flip()

	def update_cells(self):
		offsets = ((0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2))
		new_on, new_off = set(), set()
		for x, row in enumerate(self.cells):
			for y, cell in enumerate(row):
				if cell is True:
					adj = 0
					for off_x, off_y in offsets:
						c_x, c_y = x + off_x - 1, y + off_y - 1
						if 0 <= c_x < self.bounds[0] and 0 <= c_y < self.bounds[1] and self.cells[c_x][c_y] is True:
							adj += 1
							if adj > 3:
								new_off.add((x, y))
								break
					if adj < 2:
						new_off.add((x, y))
				else:
					adj = 0
					for off_x, off_y in offsets:
						c_x, c_y = x + off_x - 1, y + off_y - 1
						if 0 <= c_x < self.bounds[0] and 0 <= c_y < self.bounds[1] and self.cells[c_x][c_y] is True:
							adj += 1
					if adj == 3:
						new_on.add((x, y))
		if len(new_on) + len(new_off) == 0:
			return False

		self.frame += 1
		for x, y in new_on:
			self.cells[x][y] = True
		for x, y in new_off:
			self.cells[x][y] = False
		return True

	def add_shape(self, shape, x, y):
		for data in shape:
			if len(data) == 2:
				s_x, s_y = data
				self.cells[s_x + x][s_y + y] = True
			elif len(data) == 3:
				s_shape, s_x, s_y = data
				self.add_shape(s_shape, s_x + x, s_y + y)  

Conway_Game()