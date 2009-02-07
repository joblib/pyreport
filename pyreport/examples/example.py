#!/usr/bin/env python
import numpy as np
import pylab as pl

#from pylab import imshow
#!
#! Some graphical explorations of the Julia sets with python and pyreport
#!#########################################################################
#$
#$ We start by defining a function J:
#$ \[ J_c : z \rightarrow z^2 + c \]
#$

def J(c):
    return lambda z : z**2 + c

x, y = np.ogrid[-1:1:0.002, -1:1:0.002]
z = x + y*1j

#! If we study the divergence of function J under repeated iteration
#! depending on its inital conditions we get a very pretty graph
thresh_time = np.zeros_like(z)
for i in range(40):
    z = J(0.285)(z)
    thresh_time += (z*np.conj(z) > 4)
pl.figure(0)
pl.axes([0, 0, 1, 1])
pl.axis('off')
pl.imshow(thresh_time.real, cmap=pl.cm.bone)
pl.show()

#! We can also do that systematicaly for other values of c:
pl.axes([0, 0, 1, 1])
pl.axis('off')
pl.rcParams.update({'figure.figsize': [10.5, 5]})
c_values = (0.285 + 0.013j, 0.45 - 0.1428j, -0.70176 -0.3842j,
            -0.835-0.2321j, -0.939 +0.167j, -0.986+0.87j)

for i, c in enumerate(c_values):
    thresh_time = np.zeros_like(z)
    z = x + y*1j
    for n in range(40):
        z = J(c)(z)
        thresh_time += z*np.conj(z) > 4
    pl.subplot(2, 3, i+1)
    pl.imshow(thresh_time.real)
    pl.axis('off')
pl.show()
