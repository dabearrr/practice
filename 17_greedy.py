"""
EPI
Chapter 17, Greedy Algorithms
4 5 6 7 8
"""

import collections
import math
import random
import heapq
import bisect 
import operator
import functools
import copy
import timeit

def clear():
	print("-----------------------")

	
"""
17.1

Optimal Task Assignment

input: Array of task lengths
output: pairs of tasks to assign to each worker

sol:
sort the tasks by task length
traverse from both sides, assigning pairs (n - 1, 0),(n - 2, 1) 
"""

"""
assuming even number of tasks
"""
def taskAssignment(A):
	A.sort()
	
	ans = []
	for i in range(0, int((len(A)) / 2)):
		ans.append((A[i], A[len(A) - 1 - i]))
	
	return ans

def taskAssignmentTest():
	A = [45, 91, 10, 1, 25, 40]
	
	clear()
	print('expecting 91-1, 45-10, 25-40: ', taskAssignment(A))

taskAssignmentTest()

"""
17.4
3sum

input: array, value
output: set of triplets that add up to value

brute:
triple for loop
n^3 runtime
n memory

better:
create hash_table of entries
perform double for loop 
n^2 runtime
n mem 

better ?:
sort the array
for each item
perform sliding window to find a sum to value
n^2 runtime 
1 mem
"""

def threeSum(A, target):
	A.sort()
	ans = set()
	for i in range(len(A)):
		low = 0
		high = len(A) - 1
		
		while(low <= high):
			sum = A[i] + A[low] + A[high]
			if sum == target:
				ans.add(tuple(sorted((A[i], A[low], A[high]))))
				break
			elif sum > target:
				high -= 1
			else:
				low += 1
	
	return ans

def threeSumTest():
	A = [7, 11, 5, 2, 3]
	clear()
	print('Expecting 3-7-11, 5-5-11: ', threeSum(A, 21))

threeSumTest()

"""
17.5 Find the majority element

input: array of elements where one element appears > n/2 times
output: most common element

must be performed in one pass

brute:
hash table
o(n) mem
o(n) runtime (one pass)

knowledge:
> n/2 appearances
means it must appear at least once before the midpoint
means it must appear consecutively at least once

aaa b a b aa aaaaaa bb cc


"""

def majority(A):
	candidate = A[0]
	count = 1
	
	for i in range(1, len(A)):
		if count == 0:
			candidate = A[i]
			count += 1
		elif A[i] == candidate:
			count += 1
		else:
			count -= 1
		
	
	return candidate

def majorityTest():
	A = [2, 1, 3, 1, 1, 2, 1, 1, 3, 1]
	
	print('expecting 1, ', majority(A))
	
majorityTest()

"""
17.6 the gasup problem
	
	G	GD		TD		+-		T		AdjT
A	50	1000	900		100		100		100
B 	20	400		600		-200	-100	0
C 	5	100		200		-100	-200	0
D 	30	600		400		200		0		200
E 	25	500		600		-100	-100	100
F 	10	200		200		0		-100	100
G	10	200		100		100		0		100

D has the best +- of the cities.
If a city has the best +-, it must be ample? not true
	G	GD		TD		+-		T		AdjT
A	50	1000	800		200		200		200
B 	20	700		600		-300	-100	0
C 	10	200		100		100		0		100

if a city has negative +-, it cannot be ample.

	G	GD		TD		+-		T
A	50	1000	800		200		200
B 	20	400		600		-200	0
C 	5	100		200		-100	-100
D 	30	600		400		200		100
E 	25	500		600		-100	0
F 	10	200		200		0		0
G	10	200		100		100		100

alg: 2 pass
	G	GD		TD		+-		T		AdjT	last+
A	50	1000	900		100		100		100		A
B 	20	400		600		-200	-100	0		A
C 	5	100		200		-100	-200	0		None (passed 0)
D 	30	600		400		200		0		200		D
E 	25	500		600		-100	-100	100		D
F 	10	200		200		0		-100	100		D
G	10	200		100		100		0		200		D
A	50	1000	900		100		100		300		D
B 	20	400		600		-200	-100	100		D
C 	5	100		200		-100	-200	0		D
D 	30	600		400		200		0		200		D <- if cur == last+ return cur

	G	GD		TD		+-		T		AdjT	last+
A	50	1000	800		200		200		200		A
B 	20	700		600		-300	-100	0		None (passed 0)
C 	10	200		100		100		0		100		C
A	50	1000	800		200		200		300		C
B 	20	700		600		-300	-100	0		C
C 	10	200		100		100		0		100		C <- if cur == last+ return cur

brute:
for each city, perform a pass to see if the total gas remains > 0
n^2

better:
2 pass
track a adjustedTotal. adjustedTotal = adjustedTotal + cur +-
If adjustedTotal goes negative, adjustedTotal = 0 and last+ = None
If adjustedTotal goes positive (from 0 and last+ is None), adjustedTotal = cur+- and last+ = cur

if last+ == cur, return cur as ample city

"""

#assume array of +-
def gas_up(A):
	lastPlus = None
	adjTotal = 0
	for i in range(0, len(A) * 2):
		index = i % len(A)
		if lastPlus == index:
			return index
		
		if A[index] > 0 and lastPlus is None:
			lastPlus = index
			adjTotal = A[index]
		else:
			adjTotal += A[index]
		
		if adjTotal < 0:
			lastPlus = None
			adjTotal = 0
	
	raise Exception("No ample city exists")

def gas_up_test():
	A = [200, -300, 100]
	B = [200, -200, -100, 200, -100, 0, 100]
	
	clear()
	print('expecting 2: ', gas_up(A))
	print('expecting 3: ', gas_up(B))
	
gas_up_test()

"""
17.7 Compute the maximum water trapped by a pair of vertical lines

input: array of heights
output: max water trapped by a pair of vertical lines

brute:
check all pairs
n^2

better:
sliding window
we start at the edges of the array, checking the area of water trapped ((i2 - i1) * min(A[i1], A[i2])) and tracking a max
if A[i1] <= A[i2], we can increment the left side, since the optimal pair for i1 has been seen, vice versa
n

"""

def maximumWater(A):
	WaterPair = collections.namedtuple('WaterPair', ['water', 'left', 'right'])
	def calcWater(A, i, j):
		return abs(j - i) * min(A[i], A[j])
	
	i, j = 0, len(A) - 1
	maxWater = WaterPair(calcWater(A, i, j), i, j)
	
	while i < j:
		maxWater = max(WaterPair(calcWater(A, i, j), i, j), maxWater, key=lambda x: x.water)
		if A[i] <= A[j]:
			i += 1
		else:
			j -= 1
	
	return maxWater
	
def maximumWaterTest():
	A = [1, 2, 1, 3, 4, 4, 5, 6, 2, 1, 3, 1, 3, 2, 1, 2, 4, 1]
	
	clear()
	print('expecting 16, 4: ', maximumWater(A))
	
maximumWaterTest()

"""
17.8 largest rectangle under the skyline

input: array of rectangle heights
output: area of the largest rectangle contained by the rectangles


brute:
for each building, check all combinations of other buildings to get the max height including this building
n^n

better:

"""

def largestContainedRectangle(A):
	pillar_indices, maxRectangle = [], 0
	
	for i, h in enumerate(A + [0]):
		while pillar_indices and A[pillar_indices[-1]] > h:
			height = A[pillar_indices.pop()]
			width = i if not pillar_indices else  i - pillar_indices[-1] - 1
			maxRectangle = max(maxRectangle, height * width)
			
		pillar_indices.append(i)
		
	return maxRectangle
	
def largestContainedRectangleTest():
	A = [1, 4, 2, 5, 6, 3, 2, 6, 6, 5, 2, 1, 3]
	
	clear()
	print('expecting 20: ', largestContainedRectangle(A))
	
largestContainedRectangleTest()

