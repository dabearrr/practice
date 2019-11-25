"""
EPI
Chapter 10, Heaps

1 3 4 5 6
"""

import collections
import math
import random
import heapq

class TreeNode:
	def __init__(self, val=None, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

def clear():
	print("-----------------------")

	
"""
10.1 sort a set of sorted lists

brute force:
combine all lists, then sort
O(N*M) memory
O(N*M + N*M log(N*M)) runtime

how can we use the sorted list property to our advantage?

we can take the smallest first element of all the lists, then repeatedly pick that until we have selected all elements
"""

def mergeSortedFiles(listOfSequences):
	heap = []
	for list in listOfSequences:
		for item in list:
			heapq.heappush(heap, item)
	
	return [heapq.heappop(heap) for i in range(len(heap))]

def mergeSortedFiles2(listOfSequences):
	class HeapItem:
		def __init__(self, item, list, index):
			self.item = item
			self.list = list
			self.index = index
		def __lt__(self, other):
			return self.item < other.item
	ans = []
	heap = []
	
	for list in listOfSequences:
		if len(list) > 0:
			heapq.heappush(heap, HeapItem(list[0], list, 0))
	
	while heap:
		min = heapq.heappop(heap)
		ans.append(min.item)
		
		# add the next item from that list to the heap if possible
		if min.index + 1 < len(min.list):
			heapq.heappush(heap, HeapItem(min.list[min.index + 1], min.list, min.index + 1))
	
	return ans

def mergeSortedFilesTest():
	listOfSequences = [[1, 2, 3], [4, 5], [0, 0, 1, 7]]
	
	clear()
	print("Expecting 0, 0, 1, 1, 2, 3, 4, 5, 7 ", print(mergeSortedFiles(listOfSequences)))
	print("Expecting 0, 0, 1, 1, 2, 3, 4, 5, 7 ", print(mergeSortedFiles2(listOfSequences)))

mergeSortedFilesTest()

"""
8.2
sort increasing-decreasing array

sort a k increasing-decreasing array

k-d-i have k sections of increasing then decreasing arrays

we can frame this in the view of the last problem

it is just k sorted arrays where some are in reverse.

We can simply iterate in reverse on the increasing arrays

we will insert the smallest of each in a heap, then heappop the min, adding the next from that popped array

until the heap is empty

"""

def kIncreasingDecreasing(k, A):
	ListInDe = collections.namedtuple('ListInDe', 'list isIncreasing')
	lists = [ListInDe([], True)]
	listIndex = 0
	isIncreasing = True
	prev = None
	for i in range(len(A)):
		if prev:
			if (isIncreasing and A[i] - prev < 0) or (not isIncreasing and A[i] - prev > 0):
				listIndex += 1
				isIncreasing = not isIncreasing
				lists.append(ListInDe([], isIncreasing))
		prev = A[i]
		lists[listIndex].list.append(A[i])
	
	
	for listInDe in lists:
		if listInDe.list:
			if not listInDe.isIncreasing:
				listInDe.list.reverse()
		
	print(lists)
	heap = []
	sorted_array_iters = [iter(x.list) for x in lists]
	
	for i, it in enumerate(sorted_array_iters):
		first_element = next(it, None)
		if first_element is not None:
			heapq.heappush(heap, (first_element, i))
	
	result = []
	while heap:
		print(heap)
		smallest_entry, smallest_array_i = heapq.heappop(heap)
		smallest_array_iter = sorted_array_iters[smallest_array_i]
		
		result.append(smallest_entry)
		next_element = next(smallest_array_iter, None)
		if next_element is not None:
			heapq.heappush(heap, (next_element, smallest_array_i))
	
	return result

def kIncreasingDecreasingTest():
	A = [57, 131, 393, 294, 221, 339, 418, 452, 442, 190] 
	
	clear()
	print("Expecting 52, 131, 190, 221, 294, 339, 393, 418. 442. 452", kIncreasingDecreasing(4, A))

kIncreasingDecreasingTest()