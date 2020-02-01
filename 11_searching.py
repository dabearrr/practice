"""
EPI
Chapter 11, Searching

1 3 4 5 6 7 8 9 10
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
11.1 
Find first occurance of k in an array

brute
search from left to right for k
o(n) runtime

better:
binary search for k, if found, check to left until the item to the left is not k, return here
o(log(n)) avg
o(n) worst

best:
use bisect library
o(log(n)) avg
o(n) worst

"""

def searchForFirstOccurrence(A, k):
	l, u = 0, len(A) - 1
	
	index = -1
	while l <= u:
		m = int(l + (u - l) / 2)
		
		if A[m] == k:
			index = m
			break
		elif A[m] > k:
			u = m - 1
		else:
			l = m + 1
	
	while index > 0 and A[index - 1] == k:
		index -= 1
		
	return index
	
def searchForFirstOccurrence2(A, k):
	l, u = 0, len(A) - 1
	
	index = -1
	while l <= u:
		m = int(l + (u - l) / 2)
		
		if A[m] == k:
			# start looking left
			index = m
			u = m - 1
		elif A[m] < k:
			l = m + 1
		else:
			u = m - 1
	
	return index
	
def searchForFirstOccurrenceBisect(A, k):
	pos = bisect.bisect_left(A, k)
	
	if pos < len(A) and A[pos] == k:
		return pos
	
	return -1

def searchForFirstOccurrenceTest():
	L = [2, 3, 4, 7, 8, 11, 14, 69]
	L2 = [8, 8, 8, 8, 8, 8, 8, 8, 8]
	L3 = [7, 7, 9, 10]
	
	clear()
	print("Expecting 6, ", searchForFirstOccurrenceBisect(L, 14))
	print("Expecting 1, ", searchForFirstOccurrenceBisect(L, 3))
	print("Expecting 0, ", searchForFirstOccurrenceBisect(L2, 8))
	print("Expecting -1, ", searchForFirstOccurrenceBisect(L3, 8))
	
	
	clear()
	print("Expecting 6, ", searchForFirstOccurrence(L, 14))
	print("Expecting 1, ", searchForFirstOccurrence(L, 3))
	print("Expecting 0, ", searchForFirstOccurrence(L2, 8))
	print("Expecting -1, ", searchForFirstOccurrence(L3, 8))
	
	
	clear()
	print("Expecting 6, ", searchForFirstOccurrence2(L, 14))
	print("Expecting 1, ", searchForFirstOccurrence2(L, 3))
	print("Expecting 0, ", searchForFirstOccurrence2(L2, 8))
	print("Expecting -1, ", searchForFirstOccurrence2(L3, 8))
	
searchForFirstOccurrenceTest()

"""
11.2 Search a sorted array for entry equal to its index

input: array of sorted integers A
output: an index i such that A[i] = i

brute force:
traverse array, check i A[i] = i
O(n)

better:
can we use binary search?
if A[m] = m:
return m
elif A[m] < m:
# since we know the array is sorted we can know that all left values are wrong
l = m + 1
else:
#vice versa
u = m - 1

o(log(n)) runtime

[-1 0 1 3 7 9]
"""

def arrayAtIndexEqualsIndex(A):
	l, u = 0, len(A) - 1
	
	while l <= u:
		m = int(l + (u - l) / 2)
		if A[m] == m:
			return m
		elif A[m] < m:
			# since we know the array is sorted, all of the left values are wrong
			l = m + 1
		else:
			# vice versa
			u = m - 1
	
	return -1

def arrayAtIndexEqualsIndexTest():
	A = [-1, 0, 1, 3, 7, 9]
	A2 = [-2, 0, 2, 3, 6, 7, 9]
	
	clear()
	print("Expecting 3, ", arrayAtIndexEqualsIndex(A))
	print("Expecting 2 or 3, ", arrayAtIndexEqualsIndex(A2))

arrayAtIndexEqualsIndexTest()

"""
11.3

Search a cycliccally sorted array

array is cyclically sorted if it is possible to shift its entries all over x indices such that it becomes sorted

to find the index, we check if the left is GREATER than it.

brute force:
iterate through whole array array for min

can we use binary search?
sort of. we can split the array in two, looking to see if the min is in either slice

[7 8 9 1 2 3 4 5 6]

m = 2
if A[m] > A[right]:
	# if m > right, means that the solution lies to the right
	l = m + 1
else:
	# if m < right, means that this and to the left hold the solution
	u = m

if elements are repeated, it cannot be solved in less than o(n)
"""

def findPivot(A):
	l, u = 0, len(A) - 1
	
	while l < u:
		m = int(l + (u - l) / 2)
		if A[m] > A[u]:
			# if m > right, means that the solution lies to the right
			l = m + 1
		else:
			# if m < right, means that this and to the left hold the solution
			u = m
	
	return l

def findPivotTest():
	A = [7,8,9,10,1,2,3,4,5,6]
	A2 = [7,8,9,10,11,12,13,14,15,1,2,3,4,5,6]
	
	clear()
	print("Expecting 4, ", findPivot(A))
	print("Expecting 9, ", findPivot(A2))
	
findPivotTest()

"""
11.4 compute the integer square root

input: nonnegative integer
output: largest integer whose square is less than or equal to the given integer

can we use binary search?

what's our mid?

assume 2^32 is int max
u starts at 2^16
l = 0

runtime should always be log(ints)

we can do better

l = 0
u = the number, since the root is always smaller or equal
log(k)
"""

def computeRoot(k):
	l, u = 0, k
	
	result = 0
	while l <= u:
		m = int((l + u) / 2)
		if m * m <= k and m * m > result:
			result = m
			l = m + 1
		else:
			u = m - 1
	
	return result

def computeRootTest():
	k = 81
	k2 = 69
	k3 = 0x80000000
	
	clear()
	
	print("Expecting 9 ", computeRoot(k))
	print("Expecting 8 ", computeRoot(k2))
	print("Expecting 2^16 (65536) ", computeRoot(k3))
	
computeRootTest()	



"""
11.5 Compute the real square root

This time, the input will be floating point.

Can we use the same technique?
We know the same principles should apply in:
the input is larger or equal to the root
the root is larger or equal to 0
[0, input]

we can perform binary search here, similarly this time with floating point numbers

Runtime?
depends on the complexity of the decimal
0.5 is easier to calculate than 0.1245341

Edge cases:
Consider realNum < 1.0

root of 1/4 is 1/2

so roots CAN be larger in this case

Important tools:
use math.isclose to find close floating point numbers
"""

def computeRealSquareRoot(realNum):
	l, h = 0, 0
	if realNum > 1.0:
		l, h = 0.0, realNum
	else:
		l, h = 0, 1.0
	
	while not math.isclose(l, h):
		m = (l + h) / 2
		
		print(m)
		
		if m * m < realNum:
			l = m
		else:
			h = m
	
	return l

def computeRealSquareRootTest():
	real = 2.25
	real2 = 3.5
	real3 = 0.0625
	
	print("Expecting 1.5, got ", computeRealSquareRoot(real))
	print("Expecting 1.87082869339, got ", computeRealSquareRoot(real2))
	print("Expecting 0.25, got ", computeRealSquareRoot(real3))

computeRealSquareRootTest()


"""
11.6 Search in a 2D sorted array

Call a 2D array sorted if its rows and columns are non decreasing (both right and down are always larger)

input: 2d array, number
output: boolean, does that number appear in the 2d array?

brute force:
search the whole 2d array
o(n * m) runtime

better?
search, comparing cur with the target. if cur is smaller go left, if cur is larger, go right/ down?
no
search
if cur is target, return true
if cur is too small, check right and down
if cur is too large, check left and up

better:
heuristic search?
using cartesian distance to find the right path
if all of our traversal options have been visited, stop

we can start in the middle to save time

"""

def twoDimSearch(A, target):
	seen = set()
	def search(cur):
		val = A[cur[0]][cur[1]]
		if val == target:
			return True
		elif cur in seen:
			return False
		elif val > target:
			seen.add(cur)
			l = (cur[0], cur[1] - 1)
			u = (cur[0] - 1, cur[1])
			sol = False
			if l[1] >= 0:
				sol = sol or search(l)
			if u[0] >= 0:
				sol = sol or search(u)
			return sol
		else:
			seen.add(cur)
			r = (cur[0], cur[1] + 1)
			d = (cur[0] + 1, cur[1])
			sol = False
			if d[0] < len(A):
				sol = sol or search(d)
			if r[1] < len(A[cur[0]]):
				sol = sol or search(r)
			
			return sol
	
	return search((0, 0))

"""
can we binary search?
binary search each row
since we know the row is sorted, we know the if row[0] > target, we can skip that row

"""
def twoDimSearch2(A, target):

	"""
	Going to practice both methods here, library usage and self implementation
	"""
	def binSearch(A, target):
		l, h = 0, len(A) - 1
		
		while l <= h:
			m = (l + h) / 2
			
			if A[m] == target:
				return True
			elif A[m] < target:
				l = m + 1
			else:
				h = m - 1
		
		return False
	def binSearch2(A, target):
		index = bisect.bisect_left(A, target)
		
		if index != len(A) and A[index] == target:
			return True
			
		return False
	
	for row in A:
		if row[0] < target:
			if binSearch2(row, target):
				return True
	
	return False
	
"""
Let's consider more information. If target < A[0][-1], target is less than all elements in column n - 1
If target > A[0][-1], target is larger than all elements in row 0

we can traverse using this information, starting from the top right

runtime: O(m + n)
"""
def twoDimSearch3(A, target):
	row, col = 0, len(A[0]) - 1
	
	while row < len(A) and col > 0:
		if target < A[row][col]:
			col -= 1
		elif target > A[row][col]:
			row += 1
		else:
			return True
	
	return False
	
def twoDimSearchTest():
	array = [[-1, 2, 4, 4, 6],[1, 5, 5, 9, 21],[3, 6, 6, 9, 22],[3, 6, 8, 10, 24],[6, 8, 9, 12, 25], [8, 10, 12, 13, 40]]
	
	clear()
	print("Expecting True, ", twoDimSearch(array, 6))
	print("Expecting True, ", twoDimSearch(array, 13))
	print("Expecting False, ", twoDimSearch(array, 7))
	
	
	print("Expecting True, ", twoDimSearch2(array, 6))
	print("Expecting True, ", twoDimSearch2(array, 13))
	print("Expecting False, ", twoDimSearch2(array, 7))
	
	print("Expecting True, ", twoDimSearch3(array, 6))
	print("Expecting True, ", twoDimSearch3(array, 13))
	print("Expecting False, ", twoDimSearch3(array, 7))

twoDimSearchTest()

"""
11.7 find the min and max simultaneously

find the min and max with less than 2(n-1) comparisons (naive)

naive is
mx = A[0]
mn = A[0]

for item in A:
	mx = max(mx, item)
	mn = min(mn, item)

find a way to reduce comparisons.
let's use only max comparisons

for item in A:
	if item > mx:
		# we know item is now also greater than min, skip min compare
		mx = item
	else:
		#item can be greater than or less than mn
		mn = min(mn, item)

can we do better?
number line:
mn      mx
1 2 4 5 6

if 7 comes in 

mn      mx
1 2 4 5 6 || 7
we know its greater than mx and mn just by comparing to mx

if 0 comes in 

     mn      mx
0 || 1 2 4 5 6
we know its less than mn and thus less than mx

if 3 comes in    
mn         mx
1 || 2 4 5 6
we know its greater than mn, but we cant know if its greater than mx without ANOTHER compare. vice versa

what about combo compares?
if target > mn and target < mx:
	# ignore
else:
	# one of mn or mx is assigned target?

	3 2 5 1 2 5

1 + 2 + 1 + 2 + 2 = 8 compares
"""

def findMinMax(A):
	mn = mx = A[0]
	for i in range(1, len(A)):
		if A[i] < mn:
			mn = A[i]
		else:
			mx = max(mx, A[i])
	
	return mn, mx

""" 
5 compares + 4 compares = 9 compares
"""	

def findMinMax2(A):
	mn = mx = 0
	for i in range(len(A)):
		if A[i] < A[mn]:
			mn = i
	# removes ith element
	tmpA = A[:i] + A[i + 1:]
	
	for i in range(len(tmpA)):
		if tmpA[i] > tmpA[mx]:
			mx = i
	
	return A[mn], A[mx]

"""
Lets try divide and conquer.
We can compare pairs of numbers in the array.
Less goes to a smaller set
More goes to a larger set

smaller must contain min
larger must contain max

until smaller and larger set are size 1, stop

how can we track the sets?
think dutch flag
swap smalls to left side window
swap bigs to right side window

smalls |3 2 5 1 2 4| bigs
smalls 2 | 4 5 1 2 | 3 bigs
smalls 2 4 | 1 2 | 5 3 bigs
smalls 2 4 1 || 2 5 3 bigs

3 + 2 + 2 = 7 compares

findmin of smalls and findmax of bigs
"""	
def findMinMax3(A):
	l, h = 0, len(A) - 1
	
	i = 0
	while l < h:
		if A[l] > A[h]:
			A[l], A[h] = A[h], A[l]
		l += 1
		h -= 1
	h += 1
	l -= 1
	mx = A[h]
	mn = A[l]
	
	while l >= 0:
		mn = min(mn, A[l])
		l -= 1
	
	while h < len(A):
		mx = max(mx, A[h])
		h += 1
	
	return mn, mx

"""
streaming min and max
3 2

1 compare
g = 2, 3
l = 1, 5
newg = 1, 5

4 compares
g = 1, 5
l = 2, 4
newg = 1, 5

7 compares

same amount, but a bit cleaner.
"""
	
def find_min_max(A):
	MinMax = collections.namedtuple("MinMax", ["smaller", "larger"])
	
	def min_max(a, b):
		if a < b:
			return MinMax(a, b)
		return MinMax(b, a)
	
	global_min_max = MinMax(A[0], A[1])
	
	for i in range(2, len(A) - 1, 2):
		local_min_max = MinMax(A[i], A[i+1])
		global_min_max = MinMax(
			min(global_min_max.smaller, local_min_max.smaller), 
			max(global_min_max.larger, local_min_max.larger)
		)
	
	return global_min_max
	

def find_min_max_test():
	A = [3, 2, 5, 1, 2, 4]
	
	print("Expecting 1, 5", findMinMax(A))
	print("Expecting 1, 5", findMinMax2(A))
	print("Expecting 1, 5", findMinMax3(A))
	print("Expecting 1, 5", find_min_max(A))

find_min_max_test()

"""
11.8
Find the kth largest element

brute force:
sort the array, return A[k - 1]

nlogn runtime
o(1) mem

another thought:
heap is my first thought.
create a max heap and heapop k times

better create a minheap of first k elements
then compare next elements to heap top
if smaller, ignore
if larger, heapop and then heap push new element

this may do unnecessary work though. we are tracking the top k unnecessarily

we can narrow the problem set with multiple o(n) operations though

select a random pivot
pick 4
[2 4 5 3 1]

sort like a flag problem o(n) op
greater pivot less
[5 | 4 | 1 2 3]

if the pivot is in location k - 1, it is the kth largest item

if not, we have narrowed the problem set.
pivotIndex < k - 1:
solution lies in pivotIndex + 1 -> right 
else solution lies in left -> pivotIndex
"""

def kthLargest(A, k):
	def kthOperation(comp):
		def parition_around_pivot(left, right, pivot_index):
			pivot_value = A[pivot_index]
			# will need to swap this into the correct spot later
			A[right], A[pivot_index] = A[pivot_index], A[right]
			new_pivot_index = left
			
			for i in range(left, right):
				if comp(A[i], pivot_value):
					A[i], A[new_pivot_index] = A[new_pivot_index], A[i]
					new_pivot_index += 1
			
			# need to swap this back into correct place
			A[right], A[new_pivot_index] = A[new_pivot_index], A[right]
			return new_pivot_index
	
		left = 0
		right = len(A) - 1
		
		while left <= right:
			pivot_index = random.randrange(left, right + 1)
			new_pivot_index = parition_around_pivot(left, right, pivot_index)
			
			if new_pivot_index == k - 1:
				return A[new_pivot_index]
			elif new_pivot_index > k - 1:
				right = new_pivot_index - 1
			else:
				left = new_pivot_index + 1
		
	return kthOperation(operator.gt)

def kthLargestTest():
	A = [2, 4, 5, 3, 1]
	
	clear()
	print("Expecting 3, ", kthLargest(A, 3))
	
	print("Expecting 5, ", kthLargest(A, 1))
	print("Expecting 1, ", kthLargest(A, 5))
	A = [3, 3, 5, 3, 1]
	
	print("Expecting 3, ", kthLargest(A, 2))
	print("Expecting 3, ", kthLargest(A, 4))
	A = [0, 0, 0, 0, 0, 0]
	
	print("Expecting 0, ", kthLargest(A, 1))
	print("Expecting 0, ", kthLargest(A, 6))

kthLargestTest()


"""
11.9  Find the missing IP Address

brute force 1:
load the table into a set

index into it to find the missing ip address

O(n) mem
o(n) runtime (1 time to build table)


"""

"""
11.10 Find the duplicate and the missing number

input: array of n integers, from 0 - n-1, where one is missing and one is duplicated:
ex [0 2 33 4 5] 1 missing, 3 duplicated
not sorted 

brute force:
sorting makes this trivial
nlogn runtime


"""

def duplicate_and_missing(A):
	def expected_sum(A):
		n = len(A)
		
		return n * (n - 1) / 2
		
	sum, item_set, duplicate, missing = 0, set(), None, None
	
	# one pass to get true sum and find duplicate
	for item in A:
		sum += item
		if item in item_set:
			duplicate = item
		item_set.add(item)
	
	return duplicate, duplicate - (sum - expected_sum)
	
def duplicate_and_missing_book(A):
	# return object
	DuplicateAndMissing = collections.namedtuple('DuplicateAndMissing', 'duplicate', 'missing')

	# compute xor of all numbers from 0 to |A| - 1 and all entries in A
	miss_XOR_dup = functools.reduce(lambda v, i: v ^ i[0] ^ i[1], enumerate(A), 0)
	
	"""
	We need to find a bit that's set to 1 in miss_XOR_dup. Such a bit must
	exist if there is a single missing number and a single duplicated number in A
	
	The bit-fiddling assignment below sets all of bits in differ_bit # to 0 except
	for the least significant bit in miss_XOR_dup that's 1. 
	differ_bit, miss_or_dup = miss_XOR_dup & (~(miss_XOR_dup - 1)), 0
	"""
	
	for i, a in enumerate(A):
		# Focus on entries and numbers in which the differ_bit-th bit is 1
		if i & differ_bit:
			miss_or_dup ^= i
		if a & differ_bit:
			miss_or_dup ^= a
		
	# miss_or_dup is either the missing value or the duplicated entry
	if miss_or_dup in A:
		# miss_or_dup is the duplicate
		return DuplicateAndMissing(miss_or_dup, miss_or_dup ^ miss_XOR_dup)
	
	return DuplicateAndMissing(miss_or_dup ^ miss_XOR_dup, miss_or_dup)
		
	
def duplicate_and_missing_test():
	A = [0, 2, 3, 3, 4, 5]
	
	clear()
	print("Expecting (3, 1), got: ", duplicate_and_missing(A))

duplicate_and_missing_test()