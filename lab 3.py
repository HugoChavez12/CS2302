# Code to implement a binary search tree 
# Programmed by Hugo Chavez
# Last modified March 11, 2019
import matplotlib.pyplot as plt
import numpy as np
import math 

def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

class BST(object):
    # Constructor
    def __init__(self, item, left=None, right=None):  
        self.item = item
        self.left = left 
        self.right = right      
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T

def Delete(T,del_item):
    if T is not None:
        if del_item < T.item:
            T.left = Delete(T.left,del_item)
        elif del_item > T.item:
            T.right = Delete(T.right,del_item)
        else:  # del_item == T.item
            if T.left is None and T.right is None: # T is a leaf, just remove it
                T = None
            elif T.left is None: # T has one child, replace it by existing child
                T = T.right
            elif T.right is None:
                T = T.left    
            else: # T has two chldren. Replace T by its successor, delete successor
                m = Smallest(T.right)
                T.item = m.item
                T.right = Delete(T.right,m.item)
    return T
         
def InOrder(T):
    # Prints items in BST in ascending order
    if T is not None:
        InOrder(T.left)
        print(T.item,end = ' ')
        InOrder(T.right)
  
def InOrderD(T,space):
    # Prints items and structure of BST
    if T is not None:
        InOrderD(T.right,space+'   ')
        print(space,T.item)
        InOrderD(T.left,space+'   ')
  
def SmallestL(T):
    # Returns smallest item in BST. Returns None if T is None
    if T is None:
        return None
    while T.left is not None:
        T = T.left
    return T   
 
def Smallest(T):
    # Returns smallest item in BST. Error if T is None
    if T.left is None:
        return T
    else:
        return Smallest(T.left)

def Largest(T):
    if T.right is None:
        return T
    else:
        return Largest(T.right)   

def Find(T,k):
    # Returns the address of k in BST, or None if k is not in the tree
    if T is None or T.item == k:
        return T
    if T.item<k:
        return Find(T.right,k)
    return Find(T.left,k)
    
def FindAndPrint(T,k):
    f = Find(T,k)
    if f is not None:
        print(f.item,'found')
    else:
        print(k,'not found')
#------------------------------------------------------------------------------
        
def height(T):
    if T is None:
        return 0
    else:
        ldepth= 1 + height(T.left)
        rdepth = 1 + height(T.right)
        if ldepth < rdepth:
            return rdepth
        else:
            return ldepth
    
def DrawBST(ax,T,x,y,dx):
    if T is not None:
        dx = dx/2
        circle1 = plt.Circle((x,y), 3, color='k', fill = False)
        ax.add_artist(circle1)
        plt.text(x-1, y-1, T.item, fontsize = 10)
        if T.left is not None:
            DrawBST(ax, T.left ,x-dx,y-10,dx)
            p = np.array([[x,y-3],[x-dx,y-7]])
            ax.plot(p[:,0],p[:,1],color='k')
            
        if T.right is not None:
            DrawBST(ax, T.right ,x+dx,y-10,dx)
            q = np.array([[x,y-3],[x+dx,y-7]])
            ax.plot(q[:,0],q[:,1],color='k')
            
            

def ISearch(T,k):
    if k <= T.item:
        while T is not None:
            if k == T.item:
                return T
            if k < T.item:
                T = T.left
            if k > T.item:
                T = T. right
            if T == None:
                return None
    elif k >= T.item:
        while T is not None:
            if k == T.item:
                return T
            if k < T.item:
                T = T.left
            if k > T.item:
                T = T. right
            if T == None:
                return None
            
            
def BuildT(A, start, end):
    if start > end:
        return None
    L = None
    mid = (start + end)//2 
    L = BST(A[mid])
    L.left = BuildT(A, start, mid-1)
    L.right = BuildT(A, mid+1, end)
    
    return L
    
    
def Extract(T, A):
    if T is None:
        return 
    Extract(T.left, A)
    A.append(T.item)
    
    Extract(T.right, A)
    return A
    
def PrintAtDepth(T, depth):
    if T is None:
        return
    if depth ==0:
            print(T.item, end = ' ')
    else:
        PrintAtDepth(T.left, depth -1)
        PrintAtDepth(T.right, depth -1)

# Code to test the functions above
T = None
A = [10,4,15,2,8,12,18,1,3,5,9,7]
Y = [10,4,15,2,8,12,18,1,3,5,9,7]

for a in A:
    T = Insert(T,a)

A.sort()
#-----------------------------------------------------------------------------
plt.close("all") 
fig, ax = plt.subplots() 
DrawBST(ax,T, 50,97,50)
ax.set_xlim((0, 100))
ax.set_ylim((0, 100))
plt.show()
fig.savefig('bst.png')

print('-----Iterative Search-----')
X = ISearch(T, 7)
if X is not None:
    print(X.item)
elif X == None:
    print('None')
print('----Build List-----')
print(A)
L = BuildT(A, 0, len(A)-1)

#DrawBST(ax,L, 50,97,50)
print('----Extract tree-----')

print('Original list')
print(Y)
B = []
B = Extract(T, B)
print('Extracted List')
print(B)
print('----Keys at Depth----')
depth = height(T)
for i in range(depth):
    print('Keys at Depth', i, ':', end = ' ')
    PrintAtDepth(T, i)
    print()