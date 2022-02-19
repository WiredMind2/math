from multiprocessing import Pool

# def get_pixel(d):
# 	x, y = d
# 	cx = (x * (XMAX - XMIN) / LARGEUR + XMIN)
# 	cy = (y * (YMIN - YMAX) / HAUTEUR + YMAX)
# 	xn = 0
# 	yn = 0
# 	n = 0
# 	while (xn * xn + yn * yn) < 4:
# 		tmp_x = xn
# 		tmp_y = yn
# 		xn = tmp_x * tmp_x - tmp_y * tmp_y + cx
# 		yn = 2 * tmp_x * tmp_y + cy
# 		n += 1
# 		if n >= MAX_ITERATION:
# 			return (x, y, True)
# 	return (x, y, False)

# MAX_ITERATION = 100
# XMIN, XMAX, YMIN, YMAX = -2, +0.5, -1.25, +1.25
# LARGEUR, HAUTEUR = 1000, 1000
# ORIGIN_X, ORIGIN_Y, END_X, END_Y = 0, 0, LARGEUR - 0, HAUTEUR - 0
# FACTOR_X, FACTOR_Y = (END_Y - ORIGIN_Y) / LARGEUR, (END_X - ORIGIN_X) / HAUTEUR
# if __name__ == "__main__":
# 	import pygame
# 	pygame.init()
# 	screen = pygame.display.set_mode((LARGEUR - ORIGIN_X, HAUTEUR - ORIGIN_Y))
# 	screen.fill((0, 0, 0))
# 	pygame.display.set_caption("Fractale de Mandelbrot")

# 	with Pool() as p:
# 		out = p.map(get_pixel, ((x, y) for y in range(ORIGIN_X, END_X) for x in range(ORIGIN_Y, END_Y)))

# 		for x, y, p in out:
# 			if p:
# 				screen.set_at((int(x * FACTOR_X), int(y * FACTOR_Y)), (255, 255, 255))		

# 	pygame.display.flip()
# 	loop = True
# 	while loop:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				loop = False
# 	pygame.quit()
import pygame

class Mandelbrot:
	def __init__(self):
		self.MAX_ITERATION = 50
		self.LARGEUR, self.HAUTEUR = 500, 500
		self.ZOOM, self.CENTER = 1, (0.5, 0.5)

		self.ModuleMax = 4

		pygame.init()
		self.screen = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))
		pygame.display.set_caption("Fractale de Mandelbrot")

		print(self.CENTER, self.ZOOM, self.bounds_from_zoom(self.ZOOM, self.CENTER))
		self.draw()

		loop = True
		while loop:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop = False
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					fac_x, fac_y = pos[0] / self.LARGEUR, pos[1] / self.HAUTEUR
					print(self.CENTER, self.ZOOM, fac_x, fac_y)
					self.CENTER = (fac_x, fac_y)
					self.ZOOM += 1
					self.draw()
		pygame.quit()

	def intervalle(self, min, max, nbInter):
		inter = (max-min)/(nbInter-1)
		tab = [min]*(nbInter)
		for i in range (0,nbInter):
			tab[i] = min + (inter*i)
		return tab

	def Mandelbrot(self, x,y):
		nombre = x+(y*1j)
		i = 1
		z = nombre
		c = nombre
		appartient = True
		while i <= self.MAX_ITERATION and appartient==True :

			if abs(z)>self.ModuleMax :
				appartient = False
			z = (z*z)+c
			i += 1
			
		return int(appartient)

	def ensembleMandelbrot(self, Xmin,Xmax,Ymin,Ymax):
		tabx = self.intervalle(Xmin,Xmax,self.LARGEUR)
		taby = self.intervalle(Ymin,Ymax,self.HAUTEUR)
		img_nb = [[0]*len(taby) for i in range (len(tabx))]
		for j in range (len(taby)):
			for i in range (len(tabx)):
				img_nb[len(tabx)-1-j][i] = self.Mandelbrot(tabx[i],taby[j])
		return (tabx, taby, img_nb)

	def bounds_from_zoom(self, ZOOM, CENTER):
		START, SIZE = (-2, -1.25), (2.5, 2.5)

		SIZE_ZOOM = (SIZE[0] / ZOOM, SIZE[1] / ZOOM)
		ZOOM_CENTER = (SIZE_ZOOM[0] / 2, SIZE_ZOOM[1] / 2)
		CENTER_OFF = (SIZE[0] * CENTER[0] + START[0], SIZE[1] * CENTER[1] + START[1])
		START_ZOOM = (CENTER_OFF[0] - ZOOM_CENTER[0], CENTER_OFF[1] - ZOOM_CENTER[1])

		XMIN, XMAX, YMIN, YMAX = START_ZOOM[0], START_ZOOM[0] + SIZE_ZOOM[0], START_ZOOM[1], START_ZOOM[1] + SIZE_ZOOM[1]
		return XMIN, XMAX, YMIN, YMAX

	def draw(self):

		XMIN, XMAX, YMIN, YMAX = self.bounds_from_zoom(self.ZOOM, self.CENTER)

		tabX, tabY, img = self.ensembleMandelbrot(XMIN, XMAX, YMIN, YMAX)

		self.screen.fill((0, 0, 0))
		for x_i, x, y_i, y in ((x_i, x, y_i, y) for x_i, x in enumerate(tabX) for y_i, y in enumerate(tabY)):
			if img[y_i][x_i] == 1:
				self.screen.set_at((x_i, y_i), (255,255,255))
		pygame.display.flip()

Mandelbrot()