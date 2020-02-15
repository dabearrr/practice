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
		for j in range(1, len(cache[i])):
			curVal = 0
			
			if j - SCORES[i] >= 0:
				curVal += cache[i][j - SCORES[i]]
			if i > 0:
				curVal += cache[i - 1][j]
			cache[i][j] = curVal
	
	return cache[len(SCORES) - 1][finalScore]
	
def countScoreCombosTest():
	fs = 12
	
	clear()
	print('expecting 4, ', countScoreCombos(fs))
	print('expecting 4, ', countScoreCombos2(fs))
	print('expecting 4, ', countScoreCombos3(fs))
	
countScoreCombosTest()

"""
16.1 variant: climbing steps

input: nth step to get to, k steps max per move
output: amount of ways to reach nth step

brute force:
enumerate all combinations of 1->k that add up to n

dp:
let's do some examples

1 1
2 11 2
3 111 12 3
4 1111 22 211 31 4
5 11111 2111 221 32 311 41 5

0				0	1	2	3	4	5
0 steps only	0	0	0	0	0	0
1 steps only	1	1	1	1	1	1
12 steps only	1	1	2	2	3	3
123 steps		1	1	2	3	4	5
1234 steps		1	1	2	3	5	6
12345 steps		1	1	2	3	5	7

A[i][j] = up 1 + left i

optimizations: below the diagonal with the answer (A[i][j]), all the values are repeated, this is potential wasted work

"""

def climbingSteps(n, k):
	cache = [[1 if col < 2 and row > 0 else 0 for col in range(n + 1)] for row in range(k + 1)]
	
	for row in range(1, len(cache)):
		for col in range(2, len(cache[row])):
			sum = 0
			if row > 0:
				sum += cache[row - 1][col]
			if col - row >= 0:
				sum += cache[row][col - row]
			cache[row][col] = sum
	
	return cache[k][n]

def climbingStepsTest():
	clear()
	print('expecting 7, n=5, k=5: ', climbingSteps(5, 5))
	
climbingStepsTest()

"""
16.2 Levinshtein distance

input: two strings
output: minimum levenshtien distance from a to b

distance steps: replace char, remove char, insert char

Saturday
Sundays
 
 ---replacement is upleft (+1)---
 why? 
 consider sund and satu
 if we replace d -> u, we get sunu satu, meaning the lev distance is 1 + ld(sun, sat)
 ---deletion is up (+1)---
 why? 
 consider sund and satu
 if we delete d, we get sun and satu (^ one)
 ---insertion is ? --- left (+1) i think
 
 Sunday Saturday + 1 choice
 Sundays Saturday

sunu satu

			""	"S"		"Sa"	"Sat"	"Satu"	"Satur"		"Saturd"	"Saturda"	"Saturday"
""			0	1		2		3		4		5			6			7			8
"S"			1	0		1		2		3		4			5			6			7
"Su"		2	1		1		2		2		3			4			5			6
"Sun"		3	2		2		2		3		3			4			5			6
"Sund"		4	3		3		3		3		4			3			4			5
"Sunda"		5	4		4		4		4		4			4			3			4
"Sunday"	6	5		5		5		5		5			5			4			3
"Sundays"	7	6		6		6		6		6			6			5			4


recurrence relation:

let a be len(A), let b be len(B), A and B are strings
E(A[a-1], B[b-1]) is the levenshtien distance between A and B

 E(A[a-1], B[b-1]) = min (
 1 + E(A[a-2], B[b-1]), deletion
 1 + E(A[a-1], B[b-2]), insertion
 1 + E(A[a-2], B[b-2]) replacement
 ) if A[a-1] != B[b-1] 
 else E(A[a-2], B[b-2])
"""	

def levenshtienDistance(a, b):
	cache = [[col if row == 0 else row if col == 0 else 0 for col in range(len(a) + 1)] for row in range(len(b) + 1)]
	
	for row in range(1, len(cache)):
		for col in range(1, len(cache[row])):
			# take min of 3 options: delete, insert, replace
			cache[row][col] = min(cache[row - 1][col], cache[row][col - 1], cache[row - 1][col - 1])
			if a[col - 1] != b[row - 1]:
				cache[row][col] += 1
	
	return cache[len(b)][len(a)]

def levenshtienDistanceTest():
	clear()
	print(levenshtienDistance("Saturday", "Sundays"))
	
levenshtienDistanceTest()

"""
16.3 count the number of ways to traverse a 2d array
input: 2d array
output: number of ways to traverse from top left to bottom right

moves: go right or go down

does this have optimal substructure?

consider some cases:

cols	0	1	2	3
rows
0		0	0	0	0
1		0	1	1	1
2		0	1	2	3	
3		0	1	3	6

when you go down, reduce rows by 1
when you go right, reduce cols by 1

C(NxM) = C(N-1xM) + C(NxM-1)

why?
we showed it numerically, now we need to prove it

to get to pos (2, 2) in our 3x3 array, we need to either reach (1, 2) or (2, 1).
since we can have either previous position we have to add the counts to reach those positions.
to get to pos (1, 2) in our 3x3 array, we need to either reach (0, 2) or (1, 1).
since we can have either previous position we have to add the counts to reach those positions.
repeat for all array cells

# cant have zero rows or columns in 2d array => 0
# if we have only one row or one column, we can only go right or down => 1
if col < 2 or row < 2:
	A[i][j] = min(row, col)
A[i][j] = sum(A[i-1][j], A[i][j-1])
"""	

def countWaysToTraverseToBottomRight(n, m):
	cache = [[min(row, col) if col < 2 or row < 2 else 0 for col in range(m + 1)] for row in range(n + 1)]
	
	for row in range(2, n + 1):
		for col in range(2, m + 1):
			cache[row][col] = cache[row - 1][col] + cache[row][col - 1]
	
	return cache[n][m]
	
def countWaysToTraverseToBottomRightTest():
	clear()
	
	print('Expecting 6: ', countWaysToTraverseToBottomRight(3, 3))
	print('Expecting 70: ', countWaysToTraverseToBottomRight(5, 5))

countWaysToTraverseToBottomRightTest()
"""
16.5 Search for a sequence in a 2d array
input: 2d array and 1d array
output: boolean (found 1d array through traversal)

we have to find the 1d array as a traversal
we can move up down left and right
1d array must be adjacent
can go over same cell twice


looking for 1 3 4 6

1 2 3
3 4 5
5 6 7


to find 1 3 4 6: need to have found 1 3 4

pattern = K
len(K) = k

2d array = A (n x m)

solution = S(A, K[0, k-1]) = S(A, K[0, k-2]) + move up down left or right to K[k-1]


dont think we need a table here

consider guided search

at cell, we search for a suffix of K

if found, adjust suffix and search from adjacent cells
"""	

def sequenceSearch(A, K):
	def dfs(row, col, suffix):
		# found answer
		if suffix >= len(K):
			ans[0] = True
			return
		if ans[0] or row < 0 or row >= len(A) or col < 0 or col >= len(A[row]) or A[row][col] != K[suffix]:
			return
		
		dfs(row - 1, col, suffix + 1)
		dfs(row, col - 1, suffix + 1)
		dfs(row + 1, col, suffix + 1)
		dfs(row, col + 1, suffix + 1)

	ans = [False]
	for i in range(len(A)):
		for k in range(len(A)):
			if A[i][k] == K[0]:
				dfs(i, k, 0)
	
	return ans[0]
	
def sequenceSearch2(A, K):
	def dfs(row, col, suffix):
		# found answer
		if suffix >= len(K):
			ans[0] = True
			return True
			
		if ans[0] \
		or (row, col, suffix) in previousFailedAttempts \
		or row < 0 \
		or row >= len(A) \
		or col < 0 \
		or col >= len(A[row]) \
		or A[row][col] != K[suffix]:
			return False
		
		if dfs(row - 1, col, suffix + 1) \
		or dfs(row, col - 1, suffix + 1) \
		or dfs(row + 1, col, suffix + 1) \
		or dfs(row, col + 1, suffix + 1):
			return True
		
		previousFailedAttempts.add((row, col, suffix))
		return False

	previousFailedAttempts = set()
	ans = [False]
	for i in range(len(A)):
		for k in range(len(A)):
			if A[i][k] == K[0]:
				dfs(i, k, 0)
	
	return ans[0]

def is_pattern_contained_in_grid(grid, S):
	def is_pattern_suffix_contained_starting_at_xy(x, y, offset):
		if len(S) == offset:
			return True
		
		if (0 <= x < len(grid) \
		and 0 <= y < len(grid[x]) \
		and grid[x][y] == S[offset] \
		and (x, y, offset) not in previous_attempts \
		and any(is_pattern_suffix_contained_starting_at_xy(x + a, y + b, offset + 1) for a, b in ((-1, 0), (1, 0), (0, -1), (0, 1)))):
			return True
		previous_attempts.add((x, y, offset))
		return False
	
	previous_attempts = set()
	return any(is_pattern_suffix_contained_starting_at_xy(x, y, 0) for x in range(len(grid)) for y in range(len(grid[x])))

def sequenceSearchTest():
	A = [[1, 2, 3],[3, 4, 5],[5, 6, 7]]
	K = [1, 3, 4, 6]
	K2 = [1, 2, 3, 4]
	
	clear()
	print('expecting true: ', sequenceSearch(A, K))
	print('expecting false: ', sequenceSearch(A, K2))
	clear()
	print('expecting true: ', is_pattern_contained_in_grid(A, K))
	print('expecting false: ', is_pattern_contained_in_grid(A, K2))
	clear()
	print('expecting true: ', sequenceSearch2(A, K))
	print('expecting false: ', sequenceSearch2(A, K2))

sequenceSearchTest()


"""
16.6 The Knapsack problem

input: list of items with weight and values, backpack weight constraint
output: subset of items with maximal value while under the weight constraint

items
name	weight		value
1		4			7
2		2			2
3		3			5
4		1			3

max weight = 4
	weight constraint	0	1	2	3	4
items to consider
0						0	0	0	0	0
1						0	0	0	0	7
1-2						0	0	2	2	7
1-3						0	0	2	5	7
1-4						0	3	3	5	8

T(n) = max(dont pick this item, pick this item, pick this item + previous optimal with space for this item)
A[i][j] = max(A[i-1][j], S[i].value + A[i-1][j-S[i].weight] if j > S[i].weight)

"""

def knapsack(S, maxWeight):
	cache = [[0 for col in range(maxWeight + 1)] for row in range(len(S) + 1)]
	
	for row in range(1, len(cache)):
		for col in range(len(cache[row])):
			pickItemSum = 0
			dontPickItemSum = cache[row - 1][col]
			if col >= S[row - 1].weight:
				pickItemSum += cache[row - 1][col - S[row - 1].weight] + S[row - 1].value
			cache[row][col] = max(pickItemSum, dontPickItemSum)
	
	return cache[len(S)][maxWeight]

def knapsackTest():
	SackItem = collections.namedtuple('SackItem', ['weight', 'value'])
	S = [SackItem(4, 7), SackItem(2, 2), SackItem(3, 5), SackItem(1, 3)]
	
	clear()
	print('expect 8: ', knapsack(S, 4))
	

knapsackTest()

"""
divide the spoils
input: set of items to split as evenly as possible by value
output: value to robber A, value to robber B

brute force:
consider all subsets s and their inverse s' (all the other items)
2^n runtime

At each item, we are making a choice.

Do we take this item for thief A, or leave it to thief B

T(n) = T(n - 1)???

lets draw it out
items
name	value
1		7
2		2
3		5
4		3

				items to consider A	0	1		1-2		1-3		1-4
items to consider B	
					0				0	
					1
					1-2
					1-3
					1-4
----

we should instead consider the midpoint
sum(items) / 2 would be the optimal split

we should pick sets of items to get as close to this as possible

we traverse the item array, at each step adding or not adding to a sum
if we pass the midpoint, we should stop this branch

"""

def divideSpoils(S):
	def dfs(curSum, index):
		if curSum > mid[0]:
			minDiff[0] = min(minDiff[0], curSum - mid[0])
			return
		if (curSum, index) in seenSumIndex or index >= len(S):
			return
		seenSumIndex.add((curSum, index))
		
		# pick or not pick
		dfs(curSum + S[index], index + 1)
		dfs(curSum, index + 1)
	
	seenSumIndex = set()
	mid = [sum(S) / 2]
	minDiff = [float('inf')]
	dfs(0, 0)
	return minDiff[0] * 2

def divideSpoilsTest():
	A = [7, 2, 5, 3]
	
	clear()
	print('expect 1: ', divideSpoils(A))
	A = [7, 2, 5, 3,5,5,5,5,99]
	print('expect 62: ', divideSpoils(A))

divideSpoilsTest()
"""
16.7 bed bath beyond problem
input: string (url), set of strings (dictionary)
output: array of strings that concatenate to make the url (have to all add up to the word exactly, can reuse word)

brute:
we can traverse the string in two for loops
we make every word possible from a start index
then we traverse the string with only the words we made

n^2 time and mem

optimal substructure:
bedbathandbeyond
bed + bathandbeyond

T(S) = S[0:i] + T(S[i:]) where S[0:i] in dictionary

better:
construct words from 0 onwards
construct words from 0words end index onwards
 
 cache words by start index
"""

def bbb(S, D):
	def wordsFromIndex(start, end, curWord):
		if ans[0]:
			return
		if curWord in D:
			words.append(curWord)
			wordsFromIndex(end, end, "")
			words.pop()
		if end == len(S):
			if sum(map(lambda x: len(x), words)) == len(S):
				ans[0] = copy.deepcopy(words)
			return
		
		wordsFromIndex(start, end + 1, curWord + S[end])
	ans = [None]
	words = []
	wordsFromIndex(0, 0, "")
	
	return ans[0]
	
def decompose_to_dictionary(domain, dictionary):
	last_length = [-1] * len(domain)
	
	for i in range(len(domain)):
		if domain[:i + 1] in dictionary:
			last_length[i] = i + 1
		
		if last_length[i] == -1:
			for j in range(i):
				if last_length[j] != -1 and domain[j + 1: i + 1] in dictionary:
					last_length[i] = i - j
					break
	
	decompositions = []
	
	if last_length[-1] != -1:
		# we have a solution
		idx = len(domain) - 1
		while idx >= 0:
			decompositions.append(domain[idx + 1 - last_length[idx]:idx + 1])
			idx -= last_length[idx]
		decompositions= decompositions[::-1]
	
	return decompositions
				

				
def bbbTest():
	A = set(["bat", "bed", "bath"])
	S = "bedbath"
	
	clear()
	print('expecting bed bath: ', bbb(S, A))

bbbTest()

"""
16.12
"""