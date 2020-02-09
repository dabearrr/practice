"""
EPI
Chapter 16, Dynamic Programming

1 2 3 5 6 7 12
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
samples
"""
def sample1(n):
	cache = {}
	def fib(n):
		if n <= 1:
			return n
		elif n not in cache:
			cache[n] = fib(n - 1) + fib(n - 2)
		return cache[n]
	
	return fib(n)

def sample2(n):
	if n <= 1:
		return n
		
	f_minus_2, f_minus_1 = 0, 1
	
	for _ in range(1, n):
		f = f_minus_2 + f_minus_1
		f_minus_2, f_minus_1 = f_minus_1, f
	
	return f_minus_1

"""

find the max sum over all subarrays of A

create every subarray

max = max(A)
candidates = [[x] for x in A]

while len(candidates) > 1:
	newCandidates = []
	
	for i in range(1, len(candidates)):
		candidate = []
		
		for item in candidates[i-1]:
			candidate.append(item)


-- dont need subarrays, just ranges

	RangeSum = collections.namedtuple('RangeSum', ['left', 'right', 'sum'])

	candidates = [RangeSum(i, i, A[i]) for i in range(0, len(A))]
	max = max(candidates)

	while len(candidates) > 1:
		for i in range(0, len(candidates) - 1):
			candidates[i].sum += A[candidates[i].right + 1]
			candidates[i].right += 1
			
			max = max(max, candidates[i].sum)
	
	return max
	
	
	n^2 runtime
	n mem
"""
def sample3(A):
	RangeSum = collections.namedtuple('RangeSum', ['left', 'right', 'sum'])

	candidates = [RangeSum(i, i, A[i]) for i in range(0, len(A))]
	maxCandidate = max(candidates, key= lambda x : x.sum)

	length = len(candidates)
	while length > 1:
		for i in range(0, length - 1):
			newCandidate = RangeSum(candidates[i].left, candidates[i].right + 1, candidates[i].sum + A[candidates[i].right + 1])
			candidates[i] = newCandidate
			
			maxCandidate = max(maxCandidate, candidates[i], key= lambda x : x.sum)
		length -= 1
	
	return (maxCandidate.left, maxCandidate.right)
	
def sample3Test():
	A = [10, -1, 5, -6]
	B = [904, 40, 523, 12,-335, -385, -124, 481, -31]
	
	clear()
	print("expecting 0, 2: ", sample3(A))
	print("expecting 0, 3: ", sample3(B))
	
sample3Test()

"""
16.1 Count the number of score combinations

2 3 7 values

input: final score int
output: combinations of (2, 3, 7) that add up to the final score

2
3
22
23
33 222
7 232
2222 332
333 72
73 22222, 3322
722 3332

3333 222222 732 222333

27 333 

0   1  2  3  4  5  6  7  8  9  10 11 12
[x, x, 1, 1, 1, 1, 2, 1, 2, 2, 3, 2, 4]

a[i] = a[i-2] + a[i-3] + a[i - 7]

this doesnt work becuase of overlap:

"""	

"""
does not work
"""
def countScoreCombos(finalScore):
	SCORES = [2, 3, 7]
	cache = [None for _ in range(finalScore + 1)]
	
	# assuming scores cannot have more than combination here
	for score in SCORES:
		cache[score] = 1
	
	# look back if possible to i - score for each score, then sum them up
	for i in range(SCORES[0] + 1, len(cache)):
		if cache[i] is None:
			sumCombinations = 0
			for score in SCORES:
				if i - score > 0 and cache[i - score]:
					sumCombinations += cache[i - score]
			
			cache[i] = sumCombinations
	
	return cache[finalScore]

def countScoreCombos2(finalScore):
	SCORES = [2, 3, 7]

	def prettyPrint(cache):
		for i in range(len(cache)):
			print(i, cache[i])
	
	def doesNotMatchAnyEntry(counter, list):
		for entry in list:
			if counter == entry:
				return False
		
		return True
	
	cache = [None for _ in range(finalScore + 1)]
	
	
	# assuming scores cannot have more than combination here
	for score in SCORES:
		cache[score] = [collections.Counter({score : 1})]
	
	# look back if possible to i - score for each score, then sum them up
	for i in range(SCORES[0] + 1, len(cache)):
		if cache[i] is None:
			combinations = []
			
			# look back at previous entries in cache, add one of score goals to the counter.
			for score in SCORES:
				if i - score > 0 and cache[i - score]:
					for counter in cache[i - score]:
						cur = copy.deepcopy(counter)
						cur[score] += 1
						if doesNotMatchAnyEntry(cur, combinations):
							combinations.append(cur)
			
			cache[i] = combinations
	
	return len(cache[finalScore])

def countScoreCombos3(finalScore):
	SCORES = [2, 3, 7]
	cache = [[1 if x == 0 else 0 for x in range(finalScore + 1)] for score in SCORES]

	for i in range(len(cache)):
		for j in range(len(cache[i])):
			curVal = 0
			if j - SCORES[i] >= 0:
				
def countScoreCombosTest():
	fs = 12
	
	clear()
	print('expecting 4, ', countScoreCombos(fs))
	print('expecting 4, ', countScoreCombos2(fs))
	
countScoreCombosTest()

"""
16.2
"""	



"""
16.3
"""	



"""
16.5
"""	



"""
16.6
"""	



"""
16.7
"""	



"""
16.12
"""