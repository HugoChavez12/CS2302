# Code to implement a B-tree 
# Programmed by Hugo Chavez
# Last modified February 12, 2019
import math 

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
        
def height(T):
    if T.isLeaf:
        return 1
    return 1 + height(T.child[0])
        
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
        
#------------------------------------------------------------------------------
def Extract(T, A):
    if T.isLeaf:
        for i in range(len(T.item)):
            A.append(T.item[i])
    for i in range(len(T.child)):
        Extract(T.child[i],A)
                    

def MinItemAtDepth(T,depth):
    if depth == 0:
        return T.item[0]
    if T.isLeaf:
        return math.inf
    else:
        return MinItemAtDepth(T.child[0],(depth-1))
    
    
def MaxItemAtDepth(T,depth):
    if depth == 0:
        return T.item[-1]
    if T.isLeaf:
        return math.inf
    else:
        return MaxItemAtDepth(T.child[-1],depth-1)
        
def NumNodesAtDepth(T, depth):
    if depth == 0:
        return 1
    else:
        temp = 0
        for i in range(len(T.child)):
            temp += NumNodesAtDepth(T.child[i],depth -1)
            #print(temp)
    return temp
            
def PrintAtDepth(T, depth):
    if depth == 0:
        for i in range(len(T.item)):
            print(T.item[i], end =' ')
    else:
        for i in range(len(T.child)):
            PrintAtDepth(T.child[i],depth-1 )
            
def FullNodes(T):
    if IsFull(T):
        return 1
    x = 0
    for i in range(len(T.child)):
        x += FullNodes(T.child[i])
    return x

def FullLeaf(T):
    if T.isLeaf:
        if IsFull(T):
            return 1
        else:
            return 0
    fullLeaf = 0
    for i in range(len(T.child)):
        fullLeaf += FullLeaf(T.child[i])
    return fullLeaf


def KeyAtDepth(T, k):
    if k in T.item:
        return 0
    if T.isLeaf:
        return -1
    if k > T.item[-1]:
        d = KeyAtDepth(T.child[-1], k)
    else:
        for i in range(len(T.item)):
            if k < T.item[i]:
                d = KeyAtDepth(T.child[i],k)
        if d == -1:
            return -1
    return d+1
    
            
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
T = BTree()
depth = 1
    
for i in L:
    #print('Inserting',i)
    Insert(T,i)
    #PrintD(T,'') 
    #print('\n####################################')
PrintD(T, '')
print('\n---------------Depth/Height-----------------')
H = height(T)
print('\nHeight of Tree', height(T))

print('\n-------------Extract------------------------')
B = []
A = Extract(T,B)
print('\n', A)

print('\n---------------Min Item at Depth-------------------')

x = MinItemAtDepth(T,depth)
print('\nMin Item at depth', depth,':', x)

print('\n---------------Max Item at Depth-------------------')
ma = MaxItemAtDepth(T,depth)
print('\nMax Item at depth',depth, ':', ma)

print('\n---------------Number of Nodes at Depth------------')
y = NumNodesAtDepth(T,1)
print('\n',y)

print('\n----------------Print At Depth-----------------------')
print()
PrintAtDepth(T,depth)
print()
print('\n----------------Full Nodes--------------------------')
x = FullNodes(T)
print('\n',x)

print('\n----------------Full Leaves--------------------------')
x = FullLeaf(T)
print('\n',x)

print('\n----------------Key At Depth-------------------------')
dep = KeyAtDepth(T, 5)
print('\nKey at depth:',dep)