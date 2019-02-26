# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 10:53:44 2019

@author: Hugo Chavez

"""
import random

#Node Functions
class Node(object):
    # Constructor
    def __init__(self, item, next=None):  
        self.item = item
        self.next = next 
        
def PrintNodes(N):
    if N != None:
        print(N.item, end=' ')
        PrintNodes(N.next)
        
def PrintNodesReverse(N):
    if N != None:
        PrintNodesReverse(N.next)
        print(N.item, end=' ')
        
#List Functions
class List(object):   
    # Constructor
    def __init__(self): 
        self.head = None
        self.tail = None
        
def IsEmpty(L):  
    return L.head == None     
        
def Append(L,x): 
    # Inserts x at end of list L
    if IsEmpty(L):
        L.head = Node(x)
        L.tail = L.head
    else:
        L.tail.next = Node(x) 
        L.tail = L.tail.next
        
def Print(L):
    # Prints list L's items in order using a loop
    temp = L.head
    while temp is not None:
        print(temp.item, end=' ')
        temp = temp.next
    print()  # New line 

def PrintRec(L):
    # Prints list L's items in order using recursion
    PrintNodes(L.head)
    print() 
    
def Remove(L,x):
    # Removes x from list L
    # It does nothing if x is not in L
    if L.head==None:
        return
    if L.head.item == x:
        if L.head == L.tail: # x is the only element in list
            L.head = None
            L.tail = None
        else:
            L.head = L.head.next
    else:
         # Find x
         temp = L.head
         while temp.next != None and temp.next.item !=x:
             temp = temp.next
         if temp.next != None: # x was found
             if temp.next == L.tail: # x is the last node
                 L.tail = temp
                 L.tail.next = None
             else:
                 temp.next = temp.next.next
         
def PrintReverse(L):
    # Prints list L's items in reverse order
    PrintNodesReverse(L.head)
    print()     
    
       
def GetLength(L):
    temp = L.head
    count = 0
    while temp is not None:
        count += 1
        temp = temp.next
    return count

def RandomGenerator(n):
    L = List()
    for i in range(n):
        x = random.randrange(101)
        Append(L,x)
    return L

def BubbleSort(L):
    cond =False 
    while not cond:
        cond = True
        temp = L.head
        while temp.next is not None:
            if temp.item > temp.next.item:
                t = temp.item
                temp.item = temp.next.item
                temp.next.item = t
                cond = False
            temp = temp.next
     
def MergeSort(L):
    size = GetLength(L)
    temp = L.head
    L1 = List()
    L2 = List()
    if size > 1:
        
        mid = size//2

        for i in range(size):
            if i < mid:
                Append(L1, temp.item)
                temp = temp.next
            else:
                Append(L2,temp.item)
                temp = temp.next
        MergeSort(L1)
        MergeSort(L2)
    L3 = List()
    L3.head = Merge(L1.head,L2.head)
    
    return L3

def Merge(temp1,temp2):
    L = None
    if temp1 == None:
        return temp1
    
    if temp2 == None:
        return temp2

    if temp1.item >= temp2.item:
        L = temp2
        L.next = Merge(temp1,temp2.next)
    else:
        L = temp1
        L.next = Merge(temp1.next, temp2)

    return L
    
def QuickSort(L):
    size = GetLength(L)
    temp = L.head
    
    if size > 1:
        pivot = temp.item
        temp = temp.next
        L1 = List()
        L2 = List()
        while temp is not None:
            if temp.item < pivot:
                Append(L1,temp.item)
            else:
                Append(L2,temp.item)
            temp = temp.next
        L1 = QuickSort(L1)
        L2 = QuickSort(L2)
        Append(L1,pivot)
        L = List()
        temp2 = L1.head

        while temp2 != None:
            Append(L, temp2.item)
            temp2 = temp2.next
            
        temp3 = L2.head
        while temp3 != None:
            Append(L, temp3.item)
            temp3 = temp3.next
    return L
  
def ModQuickSort(L):
    size = GetLength(L)
    temp = L.head
    if size > 1:
        pivot = temp.item
        temp = temp.next
        L1 = List()
        L2 = List()
        while temp is not None:
            if temp.item < pivot:
                Append(L1,temp.item)
            else:
                Append(L2,temp.item)
            temp = temp.next
        Append(L1,pivot)
        L = List()
        temp2 = L1.head

        while temp2 != None:
            Append(L, temp2.item)
            temp2 = temp2.next
            
        temp3 = L2.head
        while temp3 != None:
            Append(L, temp3.item)
            temp3 = temp3.next
        
        L = QuickSort(L)
        
    return L
        
    
    

L = RandomGenerator(6)
Print(L)
#L = MergeSort(L)
#Print(L)
#BubbleSort(L)
#Print(L)
L = ModQuickSort(L)
Print(L)