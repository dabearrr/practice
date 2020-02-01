#!/usr/bin/env python

# [smaller][equal][unclassified][larger]

import math
import random

def clear():
	print("-------------------------------------------")

def dnf(A, pivotIndex):
	smaller, equal, larger = 0, 0, len(A) - 1
	
	while equal < larger:
		if A[equal] < A[smaller]:
			A[smaller], A[equal] = A[equal], A[smaller]
			smaller += 1
			equal += 1
		elif A[equal] > A[larger]:
			A[larger], A[equal] = A[equal], A[larger]
			larger -= 1
		else:
			equal += 1
			

ex1 = [6, 1, 5, 3, 3, 2, 1, 4]
ex1 = [6, 1, 5, 3, 3, 2, 1, 4]
dnf(ex1, 3)
print(ex1)

def add(A):
	rev = A
	rev.reverse()
	print(rev)
	carry, i = 1, 0
	while(carry):
		print(rev)
		if i >= len(A):
			rev.append(1)
			carry = 0
		elif rev[i] == 9:
			rev[i] = 0
			i += 1
		else:
			rev[i] += 1
			carry = 0
	rev.reverse()
	
def add2(A):
	for i in reversed( range(0, len(A)) ):
		A[i] += 1
		if A[i] != 10:
			break;
		
		if i == 0:
			A[i] = 1
			A.append(0)
		else:
			A[i] = 0

A = [1, 0, 9]
A2 = [1, 0, 0]
A3 = [9, 9, 9, 9, 9]
add2(A)
add2(A2)
add2(A3)
print(A)
print(A2)
print(A3)

def stockSalesBrute(A):
	maxDiff = -float("inf")
	for i in range(len(A)):
		for j in range(i + 1, len(A)):
			for k in range(j + 1, len(A)):
				for l in range(k + 1, len(A)):
					maxDiff = max(maxDiff, (A[j] - A[i]) + (A[l] - A[k]))
	
	return maxDiff
	
def stockSales(A):
	buy = {} # holds max value of buying at index and selling later
	sell = {} # holds max value of selling at index
	
	for i in range(len(A)):
		minSeen = A[i]
		for j in range(i + 1, len(A)):
			if i in buy:
				buy[i] = max(buy[i], A[j] - minSeen)
			else:
				buy[i] = A[j] - minSeen
			if j in sell:
				sell[j] = max(sell[j], A[j] - minSeen)
			else:
				sell[j] = A[j] - minSeen
			minSeen = min(minSeen, A[j])
			
	ans = -float("inf")
	for i in range(1, len(A)):
		for j in range(i + 1, len(A) - 1):
			ans = max(ans, sell[i] + buy[j])
			print(i, j)
	
	return ans

def stockSalesFast(A):
	sell = {}
	
	minPriceSeen = A[0]
	maxSaleToday = A[1] - A[0]
	for i in range(1, len(A)):
		maxSaleToday = max(maxSaleToday, A[i] - minPriceSeen)
		sell[i] = maxSaleToday;
		minPriceSeen = min(minPriceSeen, A[i])
	
	maxPriceSeen = A[len(A) - 1]
	ans = A[-1] - A[-2] + sell[len(A)-3]
	for i in reversed(range(2, len(A) - 1)):
		ans = max(ans, sell[i-1] + maxPriceSeen - A[i])
		maxPriceSeen = max(maxPriceSeen, A[i])
		
	return ans

stockVals = [310,315,275,295,260,270,290,230,255,250]

print(stockSalesBrute(stockVals))
print(stockSales(stockVals))
print(stockSalesFast(stockVals))

def generatePrimes(n):
	primes = []
	isPrime = ([False] * 2) + ([True] * (n - 2))
	
	for i in range(2, n):
		if(isPrime[i]):
			primes.append(i)
			# mark multiples as not primes
			for j in range(i * 2, n, i):
				isPrime[j] = False
	
	return primes

print(generatePrimes(18))

"""
permutations
[2, 0, 1, 3]
[a, b, c, d]
->
[c, a, b, d]

brute force:
new array copying elements in permutation order
o(n) runtime
o(n) space

can it be done in-place?
we lose positions after swaps
i=0 swaps with 2
[c, b, a, d]
prev = (0, 2)
but we have our P array [2, 0, 1, 3], which tells us where 0 is
i=1 swaps with P[0]=2
[c, a, b, d]
prev=(1, 0)
i=2 is ok
i=3 is ok

"""

def permute(A, P):
	checked = [False] * len(A)
	
	for i in range(len(A)):
		if not checked[P[i]]:
			if P[i] != i:
				cur = P[i]
				temp = A[cur]
				
				while cur != i:
					print(A, cur, i)
					A[cur] = A[P[cur]]
					checked[cur] = True
					cur = P[cur]
				A[cur] = temp
				checked[cur] = True
			print(checked)

pArr = ['a', 'b', 'c', 'd']
pPerm = [2, 0, 1, 3]

print(pArr)
permute(pArr, pPerm)
print(pArr)

# 5.12 Sample offline data
"""
get a random subset of size k from input array of distinct elements
ex: [2, 0, 1, 4]
k = 1
[2], [1], [0], [4]
k = 2
[2, 0], [2, 1], [2, 4], [1, 0], [1, 4], [0, 4]
k = 3
[2, 0, 1], [2, 0, 4], [2, 1, 4], [1, 0, 4]
k = n
(k-1) + (1) not in (k-1)
"""

def offline(A, k):
	if k < 1:
		return []
	if k > len(A):
		# do something to cover this with expected behavior maybe throw error
		return A
	
	# track selected elements moved to end
	window = len(A) - 1
	
	#start selecting
	while(k > 0):
		# which should we select
		selectedIndex = random.randint(0, window)
		
		#move selected item to the end
		A[selectedIndex], A[window] = A[window], A[selectedIndex]
		
		# slide our window of selected items
		window -= 1
		
		#decrement exit condition
		k -= 1
	
	return A
"""
O(k) runtime
O(1) memory # assuming we know the last k elements in A are the solution
"""
	
offlineInp = [2, 0, 1, 4]

print(offline(offlineInp, 1))
print(offline(offlineInp, 2))
print(offline(offlineInp, 3))
print(offline(offlineInp, 4))

"""
5.18 spiral ordering
1 2
3 4

returns [1, 2, | 3, | 4]
order is 00, 01, 11, 10

1 2 3
4 5 6
7 8 9
returns 1 2 3 6 9 8 7 4 5
order is 00 01 02 | 12 22 | 21 20 | 10 | 11

1 2 3 4
5 6 7 8
9 a b c
d e f g
returns 1 2 3 4 | 8 c g | f e d | 9 5 | 6 7 | b a

"""

# assume nxn 2d array
def spiral(A):
	if len(A) < 1:
		return []
	if len(A) == 1:
		return A[0]
	
	ans = []
	
	i, j = 0, 0
	layerComplete = False
	top, bottom, right, left = 0, len(A), len(A), -1
	while(len(ans) < (len(A) * len(A))):
		if not layerComplete:
			print(j, right)
			while(j < right):
				ans.append(A[i][j])
				j+=1
			j-=1
			i+=1
			while(i < bottom):
				ans.append(A[i][j])
				i+=1
			i-=1
			j-=1
			while(j > left):
				ans.append(A[i][j])
				j-=1
			j+=1
			i-=1
			while(i > top):
				ans.append(A[i][j])
				i-=1
			i+=1
			layerComplete = True
		else:
			j+=1
			top+=1
			bottom-=1
			right-=1
			left+=1
			layerComplete = False
	return ans
	
def spiralTest():
	testArr = [[1, 2], [3, 4]]
	print(spiral(testArr), "should be", [1, 2, 4, 3])

def spiralTest2():
	testArr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	print(spiral(testArr), "should be", [1, 2, 3, 6, 9, 8, 7, 4, 5])
	

def spiralTest3():
	testArr = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 'a', 'b', 'c'], ['d', 'e', 'f', 'g']]
	print(spiral(testArr), "should be", [1, 2, 3, 4, 8, 'c', 'g', 'f', 'e', 'd', 9, 5, 6, 7, 'b', 'a'])
spiralTest()
spiralTest2()
spiralTest3()


"""
5.17

Sudoku verification 

check columns, check rows, check 3x3 grids
"""

def sudoku(A):
	for i in range(len(A)):
		seenRow = set()
		seenColumn = set()
		for j in range(len(A)):
			# row
			if A[i][j] in seenRow:
				return False
			if A[i][j] != 0:
				seenRow.add(A[i][j])
			
			# column
			if A[j][i] in seenColumn:
				return False
			if A[j][i] != 0:
				seenColumn.add(A[j][i])
	
	# 3x3 grids 
	for rowOffset in range(3):
		for columnOffset in range(3):
			seenGrid = set()
			for i in range(3):
				row = i + (3 * rowOffset)
				for j in range(3):
					col = j + (3 * columnOffset)
					if A[row][col] in seenGrid:
						return False
					if A[row][col] != 0:
						seenGrid.add(A[i][j])
	
	return True
	


"""
5.15

brute force:
generate all subsets, return one randomly
nCk runtime and space

Compute a random subset of size k
A:
1 2 3 4

random subsets of size 1
1 2 3 4

size 2

12 13 14 23 24 34

size 3
123 124 134 234

size 4
1234

better solution:
just add one from unselected part of array randomly

compute random subset of size 1, pick one randomly
(4) | 2 3 1

compute random subset of size 2, pick one randomly
(4) (3) | 2 1

O(k) runtime and O(1) space
"""

# first k items in A will contain the solution
def randomSubset(A, k):
	if k > len(A):
		# k is too large
		return None
	elif k < 1:
		# k is too small
		return []

	for i in range(k):
		selectedIndex = random.randint(i, len(A) - 1)
		A[i], A[selectedIndex] = A[selectedIndex], A[i]
		
	
	# can return A[:k] too if we need to, but this solution would use O(k) space instead of O(1)
	return A
		

# simple
def randomSubsetTest():
	A = [1, 2, 3, 4, 5]
	
	clear()
	print(randomSubset(A, 1)[:1])
	print(randomSubset(A, 2)[:2])
	print(randomSubset(A, 3)[:3])
	print(randomSubset(A, 4)[:4])
	print(randomSubset(A, 5)[:5])

# k too small	
def randomSubsetTest2():
	A = [1, 2, 3, 4, 5]
	
	clear()
	print(randomSubset(A, 0))

# k too large
def randomSubsetTest3():
	A = [1, 2, 3, 4, 5]
	
	clear()
	print(randomSubset(A, 6))


randomSubsetTest()
randomSubsetTest2()
randomSubsetTest3()

"""
5.14 compute permutations

1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1

pick one randomly, move to selected group on left
do this until all are selected
O(N) runtime
O(1) space
"""

def permute(A):
	for i in range(len(A)):
		selectedIndex = random.randint(i, len(A) - 1)
		A[i], A[selectedIndex] = A[selectedIndex], A[i]
	
	return A

# simple
def permuteTest():
	A = [1, 2, 3, 4, 5]
	
	print(permute(A))

# empty
def permuteTest2():
	A = []
	
	print(permute(A))

# size = 1
def permuteTest3():
	A = [1]
	
	print(permute(A))
	
permuteTest()
permuteTest2()
permuteTest3()