# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:40:45 2019
CS 2302 - Data Structures
Instructor:Olac Fuentes
Lab 8, Algorithm Design Techniques
Makes use of the Backtracking and Randomized Algorithm techniques to find equal expressions and
to find if a set S can be partitioned in to two different sets that add up to the same number.
TA:Anindita Nath
@author: Hugo Chavez
"""
#from math import *
from mpmath import *
import math
import random
import numpy  as np

#------------------------------------------------------------------
def discover(exp):
    tolerance = 0.0001
    equalities = []
    for i in range(len(exp)):
        for j in range(len(exp)):
            equal = True
            for e in range(10):
                t  = random.uniform(-1*math.pi,1*math.pi) 
                y1 = eval(exp[i])
                y2 = eval(exp[j])
                if np.abs(y1-y2)>tolerance:
                    equal = False
            if equal:
                temp = []
                temp.append(exp[i])
                temp.append(exp[j])
                equalities.append(temp)
                
    return equalities
#----------------------------------------

def subsetsum(S,last,goal):
    if goal ==0:
        return True, []
    if goal<0 or last<0:
        return False, []
    res, subset = subsetsum(S,last-1,goal-S[last]) # Take S[last]
    if res:
        subset.append(S[last])
        return True, subset
    else:
        return subsetsum(S,last-1,goal) # Don't take S[last]


def subsets(S,pos,count,S1,S2):
    if sum(S)%2 ==1:
        return False, S1,S2
    
    else:
        a,S1 = subsetsum(S,len(S)-1,sum(S)/2)
        if a:
            Se= []
            for i in range(len(S)):
                
                Se.append(S[i])
            for j in range(len(S1)):
                Se.remove(S1[j])
            b,S2 = subsetsum(Se,len(Se)-1,sum(S1))
            
            if b and(len(S1) + len(S2) == len(S)):
                return True, S1, S2
    S1 = []
    S2 = []
    return False,S1,S2
#-----------------------------------------------------------------------------
    
print('\n------------- Trigonometric Identities -------------')

expressions = ['sin(t)','cos(t)','tan(t)','sec(t)','-sin(t)','-cos(t)','-tan(t)','sin(-t)','cos(-t)','tan(-t)','(sin(t))/(cos(t))','2*sin(t/2)*cos(t/2)','sin(t)*sin(t)','(1-cos(t))*cos(t)','(1-cos(2*t))/(2)','1/(cos(t))']
                
print('\n')
equals = discover(expressions)
print('Equal expressions:')
for i in range(len(equals)):
    print('Equation ', i+1 ,':',equals[i])

print()
print('\n---------------- Partition Problem ----------------')
S = [2,4,5,9,12]

S1=[]
S2 = []
a,Sn,St = subsets(S,0,len(S)-1,S1,S2)

if a:
    print('\nS', S)
    print('\nS1 =', Sn)
    print('\nS2 =', St)
    
else:
    print('\nS has no partition')
