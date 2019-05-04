# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:09:45 2019
CS 2302 - Data Structures
Instructor:Olac Fuentes
Lab 7, Disjoint Set Forests
Creates a random labyrinth by making use of the Forest's characteristics, and makes 
use of the breadth first and depth first search algorithms to find a solution to the maze.
TA:Anindita Nath
@author: Hugo Chavez
""" 
import time
# Starting point for program to build and draw a maze
# Modify program using disjoint set forest to ensure there is exactly one
# simple path joiniung any two cells
# Programmed by Olac Fuentes
# Last modified March 28, 2019
import math
import matplotlib.pyplot as plt
import numpy as np
import random

#------------------------------------------------------------------------------
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    def peek(self):
        return self.items
    
    
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items) 
#------------------------------------------------------------------------------

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

def AL_rep(walls, row,col):
    AL = [ [] for i in range(row*col) ]
    walls1 = wall_list(row,col)
    count = len(walls)
    x = 0
    while count != 0:
        i=0
        while i < len(walls1):
            if walls[x] == walls1[i]:
                walls1.pop(i)
            i+=1
        x+=1
        count -= 1
    for i in range(row*col):
        for j in range(len(walls1)):
            if i == walls1[j][0]:
                AL[i].append(walls1[j][1])
                AL[walls1[j][1]].append(i)
    return AL
            
    

def Breadth_First_Search(AL,end):
    q = Queue()
    prev = np.zeros(len(AL),dtype=np.int)-1
    visited = np.zeros(len(AL),dtype=bool)
    q.enqueue(0)
    visited[0] = True
    
    while not q.isEmpty():
        smt = int(q.dequeue())
        for i in range(len(AL[smt])):
            if not visited[AL[smt][i]]:
                visited[AL[smt][i]] = True
                prev[AL[smt][i]] = smt
                q.enqueue(AL[smt][i])
          
    currentV = end
    lis=[]
    if visited[end]:
        while prev[currentV] != -1:
            lis.append(currentV)
            currentV = prev[currentV]
            
        lis.append(0)
        lis.reverse()
        return lis
    print('Path to end of the maze not possible')

def Depth_First_Search(AL,end):
    s = Stack()
    prev = np.zeros(len(AL),dtype=np.int)-1
    visited = np.zeros(len(AL),dtype=bool)
    s.push(0)
    visited[0] = True
    
    while not s.isEmpty():
        current = int(s.pop())
        for i in range(len(AL[current])):
            if not visited[AL[current][i]]:
                visited[AL[current][i]] = True
                prev[AL[current][i]] = current
                s.push(AL[current][i])
          
    currentV = end
    lis=[]
    if visited[end]:
        while prev[currentV] != -1:
            lis.append(currentV)
            currentV = prev[currentV]
            
        lis.append(0)
        lis.reverse()
        return lis
    print('Path to end of the maze not possible')

def Depth_First_SearchR(path,AL,current,end,visited):
    if current == end:
        path.append(end)
        return path
    if current not in visited:
        visited.append(current)
        for i in range(len(AL[current])):
            p = []
            p.append(current)
            pat = Depth_First_SearchR(path+p,AL,AL[current][i],end,visited)
            if pat:
                return pat            
    return ('Path to end of the maze not possible')
#------------------------------------------------------------------------------
   
plt.close("all") 
maze_rows = 3
maze_cols = 3

print('The number of rows', maze_rows,', the number of columns',maze_cols,'and the number of cells:', maze_rows*maze_cols)

m = int(input('Enter the number of walls to remove:'))

forest = DisjointSetForest(maze_rows * maze_cols)

walls = wall_list(maze_rows,maze_cols)

draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 
start = time.time()

count = 0

if m == ((maze_rows*maze_cols)-1):
    print('There is a unique path from source to destination (when m = n-1)')
    # Builds maze with standard union
    while not one_Forest(forest): #!= 1:
        d = random.randint(0, len(walls)-1)
        if union(forest, walls[d][0],walls[d][1]):
            walls.pop(d)

    end = time.time()
    draw_maze(walls,maze_rows,maze_cols) 

#-----------------------------------------------------------------------------

elif m >= ((maze_rows*maze_cols)-1):
    print('There is at least one path from source to destination (when m > n-1)')
    # Builds maze with standard union
    while m != count: #!= 1:
        while not one_Forest(forest):
            d = random.randint(0, len(walls)-1)
            if union(forest, walls[d][0],walls[d][1]):
                print('removing wall ',walls[d])
                walls.pop(d)
                count+=1
        d = random.randint(0, len(walls)-1)
        walls.pop(d)
        count+=1
    end = time.time()
    draw_maze(walls,maze_rows,maze_cols) 
            
#-----------------------------------------------------------------------------
            
elif m < (maze_rows*maze_cols):
    print('A path from source to destination is not guaranteed to exist (when m < n-1)')
    # Builds maze with standard union
    while m != count: #!= 1:
        d = random.randint(0, len(walls)-1)
        if union(forest, walls[d][0],walls[d][1]):
            walls.pop(d)
            count +=1
    end = time.time()
    draw_maze(walls,maze_rows,maze_cols) 
    

maze_end = (maze_rows*maze_cols)-1
AL = AL_rep(walls,maze_rows,maze_cols)
print('Adjacency List Representation:')
print(AL)
print()
print('BFD path:')
print(Breadth_First_Search(AL,maze_end))
print()
print('DFS path:')
print(Depth_First_Search(AL,maze_end))
print()
print('DFS-R path:')
x = []
print(Depth_First_SearchR(x,AL,0,maze_end,visited=[]))
print()

print('time:', round((end-start),5))


