"""
EPI
Chapter 13, Sorting

1 2 5 7 8 10
"""

import collections
import math
import random
import heapq
import bisect 
import operator
import functools

def clear():
	print("-----------------------")
	
"""
if all items are known to be k distance from their correct location
min heap runs in o(nlog(k))

if all items are from a small set of possible values
we can use a counting sort, which ccounts the appearance of each item, then create the array from the counts in order
can keep keys in array or BST

if there are few items, insertion sort is faster than other sorts
"""
"""
13.1 Compute the intersection of two sorted arrays

simple:
turn the smaller array into a set

then traverse larger array, if A[i] in smaller array set, add to solution set
"""

def intersection(A, B):
	if len(A) < len(B):
		return intersection(B, A)
	
	setB = set()
	for item in B:
		setB.add(item)
	
	ans = set()
	for item in A:
		if item in setB:
			ans.add(item)
	
	return ans

def intersection2(A, B):
	i = j = 0
	ans = set()
	while i < len(A) and j < len(B):
		if A[i] < B[j]:
			i += 1
		elif A[i] > B[j]:
			j += 1
		else:
			shared = A[i]
			ans.add(shared)
			while i < len(A) and A[i] == shared:
				i += 1
			while j < len(B) and B[j] == shared:
				j += 1
	
	return ans
	
def intersectionTest():
	A = [4, 5, 6]
	B = [1, 2, 4, 4, 4, 6, 7, 7, 8]
	
	clear()
	print("expecting 4, 6: ", intersection(A, B))
	
def intersection2Test():
	A = [4, 5, 6]
	B = [1, 2, 4, 4, 4, 6, 7, 7, 8]
	
	clear()
	print("expecting 4, 6: ", intersection2(A, B))

intersectionTest()
intersection2Test()

"""
WRONG PROBLEM
13.2 Merge two sorted arrays

input: array a, array b (both sorted)
output: one array consisting of both arrays combined and sorted

brute force:
combine both arrays then sort
O((N+M)log(N+M)) runtime
O(N+M) mem

better:
consider the mergesort alg, and the alg we just used.

we can perform a two ptr traversal, crossing both arrays and progressively adding to a result array the smaller one.

runtime: O(n+m)
mem: O(n + m)

"""

def mergeTwoSortedArraysWrongProblem(A, B):
	i = j = 0
	result = []
	while i < len(A) or j < len(B):
		if i >= len(A) or (j < len(B) and A[i] > B[j]):
			result.append(B[j])
			j += 1
		else:
			result.append(A[i])
			i += 1
	
	return result
				
			
def mergeTwoSortedArraysWrongProblemTest():
	A = [4, 4, 5, 7, 8, 9, 11, 15, 21]
	B = [1, 6, 99, 100]
	
	clear()
	print("Expecting 1, 4, 4, 5, 6, 7, 8, 9, 11, 15, 21, 99, 100: ", mergeTwoSortedArraysWrongProblem(A, B))
	print("(Validating reverse order input) Expecting 1, 4, 4, 5, 6, 7, 8, 9, 11, 15, 21, 99, 100: ", mergeTwoSortedArraysWrongProblem(B, A))

mergeTwoSortedArraysWrongProblemTest()

"""
13.2 Merge two sorted arrays

input: array a (has extra space at the end for both arrays), array b (both sorted)
output: one array consisting of both arrays combined and sorted

brute force:
combine both arrays then sort
O((N+M)log(N+M)) runtime
O(1) mem

better:
traverse both in reverse, adding the largest value to the farthest right open location in a

sample:
1, 4, 7, 20, _, _ , _
0, 3, 25


1, 4, 7, 20, _, _ , 25
1, 4, 7, 20, _, 20 , 25
1, 4, 7, 20, 7, 20 , 25
1, 4, 7, 4, 7, 20 , 25
1, 4, 3, 4, 7, 20 , 25
1, 1, 3, 4, 7, 20 , 25
0, 1, 3, 4, 7, 20 , 25

runtime: O(N + M)
mem: O(1)
"""

def mergeTwoSortedArrays(A, B):
	if len(B) > len(A):
		return mergeTwoSortedArrays(B, A)
	
	i, j, k = len(A) - len(B) - 1, len(B) - 1, len(A) - 1
	
	while(k >= 0):
		if j < 0 or (i >= 0 and A[i] > B[j]):
			A[k] = A[i]
			i -= 1
		else:
			A[k] = B[j]
			j -= 1
			
		k -= 1
	
	return A

def mergeTwoSortedArraysTest():
	A = [4, 4, 5, 7, 200, None, None, None, None]
	B = [1, 6, 99, 100]
	
	clear()
	print("Expecting 1, 4, 4, 5, 6, 7, 99, 100, 200: ", mergeTwoSortedArrays(A, B))
	
	
	A = [4, 4, 5, 7, 200, None, None, None, None]
	B = [1, 6, 99, 100]
	print("(Validating reverse order input) Expecting 1, 4, 4, 5, 6, 7, 99, 100, 200: ", mergeTwoSortedArrays(B, A))

mergeTwoSortedArraysTest()

"""
13.5 Render a calendar
"""
"""
13.7
"""
"""
13.8
"""
"""
13.10
"""