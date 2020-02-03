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

find the maximum height of a calendar event
event has start, end

input: events, event, L (max height of events stack)
output: maximum number of concurrent events

if events overlap, they stack on top of each other.
events take up L space in total
events that are stacked split the L space equally


brute force:
check all times between the earliest start time and latest end time, check the whole events array to see which apply at that time
track max
O(deltaT^n) runtime
O(1) mem

better:
considering events:
input: list of events
Event:
start
end

we can watch the endpoints:
Endpoint:
time
active (start = 1, end = -1)

we can add endpoints to a heap, sorted by time

we pop from the heap, tracking the sum of active as a counter for concurrent events
"""
class Event:
	def __init__(self, start, end):
		self.start = start
		self.end = end

def maxConcurrentEvents(A):
	class Endpoint:
		def __init__(self, time, concurrentShift):
			self.time = time
			self.concurrentShift = concurrentShift
		def __lt__(self, other):
			if self.time == other.time:
				return self.concurrentShift > other.concurrentShift
			return self.time < other.time
	
	# can potentially use heap instead here, unsure if faster
	endpoints = []
	for event in A:
		endpoints.append(Endpoint(event.start, 1))
		endpoints.append(Endpoint(event.end, -1))
	endpoints.sort()
	
	maxConcurrent = 0
	curConcurrent = 0
	for item in endpoints:
		curConcurrent += item.concurrentShift
		maxConcurrent = max(maxConcurrent, curConcurrent)
	
	return maxConcurrent

# using lambda sort on namedtuple
def maxConcurrentEvents2(A):
	Endpoint = collections.namedtuple('Endpoint', ['time', 'concurrentShift'])
	
	# can potentially use heap instead here, unsure if faster
	endpoints = []
	for event in A:
		endpoints.append(Endpoint(event.start, 1))
		endpoints.append(Endpoint(event.end, -1))
	endpoints.sort(key=lambda e: (e.time, -e.concurrentShift))
	
	maxConcurrent = 0
	curConcurrent = 0
	for item in endpoints:
		curConcurrent += item.concurrentShift
		maxConcurrent = max(maxConcurrent, curConcurrent)
	
	return maxConcurrent
	
def maxConcurrentEventsTest():
	A = []
	A.append(Event(1, 5))
	A.append(Event(2, 7))
	A.append(Event(4, 5))
	A.append(Event(6, 10))
	A.append(Event(8, 9))
	A.append(Event(9, 17))
	A.append(Event(11, 13))
	A.append(Event(12, 15))
	A.append(Event(14, 15))
	
	clear()
	print("Expecting 3, ", maxConcurrentEvents(A))
	print("Expecting 3, ", maxConcurrentEvents2(A))

maxConcurrentEventsTest()
"""
13.7 union intervals
input: list of intervals 
output: list of intervals (no overlap)


"""
def computeUnionOfIntervals(A):
	Interval = collections.namedtuple('Interval', ['start', 'end'])
	Endpoint = collections.namedtuple('Endpoint', ['time', 'isOpen'])

	A.sort(key=lambda i: (i.start.time, i.end.time))

	def isOverlapping(a, b):
		if a.start.time > b.start.time:
			return isOverlapping(b, a)
		if a.end.time <= b.start.time:
			return True
	
	def union(a, b):
		newInterval = Interval(None, None)
		if a.start < b.start or (a.start == b.start and not a.start.isOpen):
			newInterval.start = a.start
		else:
			newInterval.start = b .start
		
		if a.end > b.end or (a.end == b.end and not a.start.isOpen):
			newInterval.end = a.end
		else:
			newInterval.end = b.end
		
		return newInterval
	
	result = []
	curInterval = A[0]

	for i in range(1, len(A)):
		if isOverlapping(curInterval, A[i])
			curInterval = union(curInterval, A[i])
		else:
			result.append(curInterval)
			curInterval = A[i]
	
	return result

def computeUnionOfIntervalsTest():
	Interval = collections.namedtuple('Interval', ['start', 'end'])
	Endpoint = collections.namedtuple('Endpoint', ['time', 'isOpen'])

	A = [Interval(Endpoint(0, True), Endpoint(3, True)), Interval(Endpoint(9, True), Endpoint(11, False)), Interval(Endpoint(1, False), Endpoint(1, False)), Interval(Endpoint(2, False), Endpoint(4, False)), Interval(Endpoint(8, False), Endpoint(11, True)), Interval(Endpoint(3, False), Endpoint(4, True)), Interval(Endpoint(5, False), Endpoint(7, True)), Interval(Endpoint(7, False), Endpoint(8, True))]

	clear()
	print("Expecting 0 open to 4 closed, 5 closed to 11 closed", computeUnionOfIntervals(A))

computeUnionOfIntervalsTest()


"""
13.8
"""
"""
13.10
"""