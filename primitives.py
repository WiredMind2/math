# Plot the primitive of some functions

from matplotlib import pyplot as plt
import numpy as np


def prim(f, a, b=None):
	if b is None:
		a, b = 0, a

	x = np.arange(a, b)
	yf = f(x)
	yP = np.cumsum(yf)
	plt.plot(x, yf, '-')
	plt.plot(x, yP, '--')
	plt.show()

f = lambda x: np.exp(-x**2/2) # No primitive for that function
prim(f, 100)