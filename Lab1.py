# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 23:32:59 2019

@author: Hugo Chavez
"""

import matplotlib.pyplot as plt
import numpy as np
import math 

def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y
#Creates the 2D array required to draw the inverted 'v'
def triangle (x,y,dx):
    p = np.array([[x-dx,y-100],[x,y],[x+dx,y-100]])
    return p

#makes 2D array that gives the shape of a square with a center coordinate and corners based off of its 'radius'
def square(x,y,r):
    b = np.array([[x-r,y-r],[x-r,y+r],[x+r,y+r],[x+r,y-r],[x-r,y-r]])
    return b

#draws the "growing" circles
def draw_circle(ay,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        ay.plot(x,y,color='k')
        draw_circle(ay,n-1,[radius*w,0],radius*w,w)
        
#draws the concentric circles
def draw_circles(ax,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        #center circle
        draw_circles(ax,n-1,center,radius*w,w)
        #right circle
        draw_circles(ax,n-1,[center[0]+ (radius*.666),center[1]],radius*w,w)
        #left circle
        draw_circles(ax,n-1,[center[0] - (2*radius*w),center[1]],radius*w,w)
        #up circle
        draw_circles(ax,n-1,[center[0], center[1] + (2*radius*w)],radius*w,w)
        #down circle
        draw_circles(ax,n-1,[center[0], center[1] - (2*radius*w)],radius*w,w)
    
def draw_tree(aw,n,x,y,dx):
    if n>0:
        dx = dx/2
        
        #creates the inverted 'v' shape for the tree
        p = triangle(x,y,dx)
        
        aw.plot(p[:,0],p[:,1],color='k')
        
        draw_tree(aw,n-1,x+dx,y-100,dx)

        draw_tree(aw,n-1,x-dx,y-100,dx)
        
        
def draw_squares(az,n,p,w,r):
    if n>0:
        az.plot(p[:,0],p[:,1],color='k')
        
        #Uses a recursive call for each square corner to create the samller one
        q = square(-r,-r,r*w)
        draw_squares(az,n-1,q,w,r)
         
        q1 = square(-r,r,r*w)
        draw_squares(az,n-1,q1,w,r*w)
        
        q2 = square(r,r,r*w)
        draw_squares(az,n-1,q2,w,r)
        
        q3 = square(r,-r,r*w)
        draw_squares(az,n-1,q3,w,r)
        
        
plt.close("all") 

orig_size = 1000
fig, ax = plt.subplots()
fig, ay = plt.subplots()
fig, aw = plt.subplots()
fig, az = plt.subplots()

#Calls de square method and the concentric squares
p = square(0,0,500)
draw_squares(az,3,p,.5,500)

#calls the tree
draw_tree(aw,8,500,500,500)

#calls the growing circles
draw_circle(ay, 15, [100,0], 100,.9)

#draws the concentric circle
draw_circles(ax, 5, [100,100], 100,.3333)
ax.set_aspect(1.0)
ay.set_aspect(1.0)  
aw.set_aspect(1.0)
az.set_aspect(1.0)
#ax.axis('off')
plt.show()
fig.savefig('circles.png')
fig.savefig('tree.png')