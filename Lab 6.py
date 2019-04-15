# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 10:09:45 2019
CS 2302 - Data Structures
Instructor:Olac Fuentes
Lab 6, Disjoint Set Forests
Creates a random labyrinth by making use of the Forest's characteristics
TA:Anindita Nath
@author: Hugo Chavez
"""

# Starting point for program to build and draw a maze
# Modify program using disjoint set forest to ensure there is exactly one
# simple path joiniung any two cells
# Programmed by Olac Fuentes
# Last modified March 28, 2019

import matplotlib.pyplot as plt
import numpy as np
import random

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)
    
#-------------------------------------------------------------------------------
def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # returns a True value if the roots are different
    ri = find(S,i) 
    rj = find(S,j) 
    if ri!=rj: # Do nothing if i and j belong to the same set 
        S[rj] = ri  # Make j's root point to i's root
        return True
    return False
        
def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    # returns a True value if the roots are different 
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
        return True
    return False
        
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    # returns a True value if the roots are different
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri
        return True
    return False

def one_Forest(S):
    #checks if the Forest has more than one root 
    count = 0        
    for i in range(len(S)):
        if S[i] < 0:
            count +=1
    if count == 1:
        return True
    return False
#--------------------------------------------------------
def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w


        
plt.close("all") 
maze_rows = 10
maze_cols = 15

forest = DisjointSetForest(maze_rows * maze_cols)

walls = wall_list(maze_rows,maze_cols)

draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 

'''
# Builds maze with standard union
while not one_Forest(forest): #!= 1:
    d = random.randint(0, len(walls)-1)
    if union(forest, walls[d][0],walls[d][1]):
        print('removing wall ',walls[d])
        walls.pop(d)
'''
# Builds maze with union by size compression
while not one_Forest(forest): #!= 1:
    d = random.randint(0, len(walls)-1)
    if union_by_size(forest, walls[d][0],walls[d][1]):
        print('removing wall ',walls[d])
        walls.pop(d)

draw_maze(walls,maze_rows,maze_cols) 
