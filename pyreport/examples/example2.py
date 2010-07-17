#!/usr/bin/env python
from scipy import *
from pylab import *
#! Bifurcation diagram of a mapping
#!============================================================================
#!
#! We are interested in the long term behavior of a sequence created by a
#! the iteration of map.
#!
#! The logistic map
#!-------------------
f = lambda x,r : r * x * ( 1 -x )
#! The logistic map is parametrised by "r"
x = linspace( 0, 1, 20 )
rlist = linspace( 2, 4, 5 )
hold(True)
for r in rlist:  plot(x, f(x,r), label = 'r = %.2f' % r)
legend()
xlabel('x')
ylabel('f(x)')
plot(x,x,color=(0.5,0.5,0.5), label = ' ')
show()
#! Behavior of the sequence
#!---------------------------
#! The sequence is created by iteration of the map over an initial value:
X = [0.1, ]
for i in arange(0,9):   X += [f(X[-1],2)]
print array(X)
#! The sequence converges to a stable fixed point if it has one, but can
#! also oscillated between different unstable fixed points, or have no
#! stable long term behavior, exibiting chaos.
X = [ 0.1 * ones_like(rlist), ]
for i in arange(0,30):   X += [ f(X[ -1], rlist) ]
X = vstack(X)
figure()
for i, r in enumerate(rlist):
    subplot( rlist.size, 1, i+1)
    plot( X[ :, i], label = 'r = %.2f' % r)
    ylim ( 0, 1)
    yticks('')
    xticks('')
    legend( loc = 10 )
show()
#! Bifurcation diagram
#!----------------------
#! To study the lont term behavior of the sequence we can plot the values
#! it visit after many iterations, as a function of the parameter
rlist = linspace( 2, 4, 800)
X = [ 0.5 * ones_like(rlist), ]
for i in arange(0,10000):   X += [ f(X[ -1], rlist) , ]
X = hsplit( vstack(X[-2000:]), rlist.size)
from scipy import stats
H = map( lambda Z : stats.histogram( Z, defaultlimits=(0,1), numbins=300 )[0],X)
H = map( lambda Z : 1-Z/Z.max(), H )
H = vstack(H)
figure()
imshow( rot90(H), aspect = 'auto' , extent = [2, 4, 0, 1])
bone()
xlabel('r')
ylabel(r'$X_{n \rightarrow \infty}$')
show()
