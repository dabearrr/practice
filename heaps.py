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


"""
10.3 Sort an almost sorted array

An array is almost sorted, any element is at most k away from its correctly sorted position

brute force:
we can sort the whole array naively
nlogn runtime
1 memory

better:
we can track a 2k sized heap, performing heap pop to get the correct next item 
n + klogk runtime
k memory

"""

def sortAlmostSortedArray(k, A):
    # effecively it is unsorted
    if k + 1 >= len(A):
        A.sort()
        return A
        
    heap = []
    
    for i in range(k + 1):
        heapq.heappush(heap, A[i])
    
    cur = k + 1
    ans = []
    while heap:
        ans.append(heapq.heappop(heap))
        
        if cur < len(A):
            heapq.heappush(heap, A[cur])
            cur += 1
    return ans
    
def sortAlmostSortedArrayTest():
    temp = [3, 2, 1, 6, 5, 4, 9, 8, 7, 12, 11, 10]
    
    clear()
    print("Expected 1 2 3 4 5 6 7 8 9 10 11 12 ", sortAlmostSortedArray(2, temp))
    print("Expected 1 2 3 4 5 6 7 8 9 10 11 12 ", sortAlmostSortedArray(12, temp))
    
sortAlmostSortedArrayTest()

"""
10.4 compute the k closest stars

consider the earth's position at 0, 0, 0
star's distance from earth is sqrt of a^2 + b^2 + c^2, but we can scale it without the sqrt

we can create a maxheap, inserting the first k items

from k position on, if k > max of the heap, dont insert it

return k smallest from the heap

runtime o nlogn
mem o n
"""

def kClosestStars(k, A):
    class Star:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
        def distance(self):
            return self.x ** 2 + self.y ** 2 + self.z ** 2
        def __lt__(self, other):
            # want maxheap not minheap, so we reverse the ordering
            return not (self.distance() < other.distance())
    
    if k > len(A):
        return A
    
    heap = []
    for i in range(k):
        cur = A[i]
        heapq.heappush(heap, Star(cur[0], cur[1], cur[2]))
    
    for i in range(k, len(A)):
        cur = A[i]
        next = Star(cur[0], cur[1], cur[2])
        
        if next.distance() < heap[0].distance():
            heapq.heappush(heap, next)
            heapq.heappop(heap)
    
    return [(x.x, x.y, x.z) for x in heap]

def kClosestStarsTest():
    l = [(5, 5, 5), (4, 4, 4), (2, 2, 2), (3, 3, 3), (6, 6, 6), (0, 1, 0), (0, 0, 1)]
    
    clear()
    
    print("Expecting 001 010 222, ", kClosestStars(3, l))
    print("Expecting 555 444 222 333 666 010 001 (in any order), ", kClosestStars(11, l))

kClosestStarsTest()

"""
10.5 Compute the median of online data

We want to compute the running median of a sequence of numbers

brute force:
sort the current list, get the median 
runtime nlogn
mem n

better:
I think we can use two heaps

top half of list will reside in minheap
bottom half in maxheap

when one has two more units, pop the heap top and append it to the other heap

if the heaps are the same size, median is heap1 top + heap2 top / 2

if the heaps are different sizes, the median is the larger of the heaps' top
"""

class RunningMedian:
	def __init__(self):
		self.minHeap = []
		self.maxHeap = []
	
	def _balanceHeaps(self):
		if len(self.minHeap) - len(self.maxHeap) > 1:
			# signs are inverted
			heapq.heappush(self.maxHeap, -heapq.heappop(self.minHeap))
		elif len(self.maxHeap) - len(self.minHeap) > 1:
			# signs are inverted
			heapq.heappush(self.minHeap, -heapq.heappop(self.maxHeap))
			
	def append(self, value):
		if not self.minHeap or value >= self.minHeap[0]:
			heapq.heappush(self.minHeap, value)
		else:
			# there is no max heap in python, to get around this, we simply insert negative values
			heapq.heappush(self.maxHeap, -value)
		
		self._balanceHeaps()
	def median(self):
		if not self.minHeap and not self.maxHeap:
			raise Exception("Median called with no entries in the runningMedian")
		# keep negative heap in mind
		if len(self.minHeap) == len(self.maxHeap):
			return (self.minHeap[0] - self.maxHeap[0]) / 2
		elif len(self.minHeap) > len(self.maxHeap):
			return self.minHeap[0]
		else:
			return -self.maxHeap[0]

def runningMedianTest():
	rm = RunningMedian()
	
	clear()
	rm.append(1)
	print("Expecting 1, got ", rm.median())
	rm.append(0)
	print("Expecting 0.5, got ", rm.median())
	rm.append(3)
	print("Expecting 1, got ", rm.median())
	rm.append(5)
	print("Expecting 2, got ", rm.median())
	rm.append(2)
	print("Expecting 2, got ", rm.median())
	rm.append(0)
	print("Expecting 1.5, got ", rm.median())
	rm.append(1)
	print("Expecting 1, got ", rm.median())

runningMedianTest()