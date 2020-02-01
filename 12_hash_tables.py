"""
EPI
Chapter 12, Hash Table

1 2 3 4 5 6 9
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
12.1 Validate palindromic string

input: 1 string
output: true / false (can the word be arranged to be palindromic?)

samples:
racecar
dood

all letters appear twice except for one (odd)
all letters appear twice (even)

if more than one letter appears only once: false

O(n) runtime
O(n) mem
"""

def validatePalindromicPermutation(s):
	ht = {}
	
	for c in s:
		if c not in ht:
			ht[c] = 1
		else:
			ht[c] += 1

	seenOdd = False
	for c in s:
		if ht[c] & 1:
			if seenOdd:
				return False
			seenOdd = True
	
	return True

def validatePalindromicPermutationTest():
	a = "racecar"
	b = "dood"
	c = "blaee"
	d = "chad"
	e = "aaaaaaaaaaa"
	f = "taccoat"
	
	clear()
	print("expecting True: ", validatePalindromicPermutation(a))
	print("expecting True: ", validatePalindromicPermutation(b))
	print("expecting False: ", validatePalindromicPermutation(c))
	print("expecting False: ", validatePalindromicPermutation(d))
	print("expecting True: ", validatePalindromicPermutation(e))
	print("expecting True: ", validatePalindromicPermutation(f))
	
validatePalindromicPermutationTest()

"""
12.2 Construct Letter from Magazine clippings

input: 2 strings (letter to write, magazine to use)
output: boolean (can the magazine be used to write the letter)

every character in the letter must appear in the magazine the same or more times


solution:
use a hash table

key: character, value: count

traverse the letter, adding to the hash table

traverse the magazine, subtracting from the hash table (if it is in the hash table)

traverse the hash table, checking that the entry in the hash table <= 0

should we consider spaces? (for now lets say yes)
"""

def letterFromMagazine(l, m):
	ht = {}
	
	for c in l:
		if c not in ht:
			ht[c] = 1
		else:
			ht[c] += 1
	
	for c in m:
		if c in ht:
			ht[c] -= 1
	
	for key in ht:
		if ht[key] > 0:
			return False
	
	return True
	
def letterFromMagazineTest():
	letter = "write the letter"
	magazine = "  wrritttteeehl"
	
	letter2 = "write the letterz"
	magazine2 = "  wrritttteeehl"
	
	letter3 = "write the letter"
	magazine3 = "  wrrittteeehl"
	
	clear()
	print("expecting True, ", letterFromMagazine(letter, magazine))
	print("expecting False, ", letterFromMagazine(letter2, magazine2))
	print("expecting False, ", letterFromMagazine(letter3, magazine3))

letterFromMagazineTest()

"""
12.3 ISBN cache

LRU cache
lookup / insert -> move to top
remove

class constructor -> pass cache size

ll / ht interactions
ht indexes to node

on insert, tail is popped if max size is surpassed	

"""

class IsbnNode:
	def __init__(self, isbn=0, price=0, next=None, prev=None):
		self.isbn = isbn
		self.price = price
		self.next = next
		self.prev = prev
		
class IsbnCache:
	def __init__(self, capacity):
		self.capacity = capacity
		self.ht = {}
		
		# setting up linked list structure
		# set up dummy head / tail
		self.head = IsbnNode()
		self.tail = IsbnNode()
		self.head.next = self.tail
		self.tail.prev = self.head
		
		self.length = 0
	
	def _insert(self, isbn, price):
		# inserts into the linked list, at head
		# ptrs to change: head.next, head.next.next.prev 
		# assign the new node's head & tail total: 4 ptrs
		newNode = IsbnNode(isbn, price)
		newNode.next = self.head.next
		newNode.prev = self.head
		newNode.next.prev = newNode
		self.head.next = newNode
		
		self.ht[isbn] = newNode
		self.length += 1
	
	def _pop(self):
		# pops the tail, since we have a dummy, we pop the left of tail (if it is not the dummy head)
		# to pop it, we need to reassign 2 ptrs: tail.prev.prev.next = tail , tail.prev = tail.prev.prev
		if self.tail.prev == self.head:
			raise Error("popping empty list!!")
		
		self.ht.pop(self.tail.prev.isbn)
		self.length -= 1
		
		self.tail.prev.prev.next = self.tail
		self.tail.prev = self.tail.prev.prev
		
	
	def _delete(self, isbn):
		"""
		one crux of the cache: we need to have O(1) deletes, but how??
		the hash table maps to the linked list node containing our node to delete
		ht lookup: O(1)
		ll delete: O(1)
		
		perfect
		
		the trade off is O(2n) space complexity
		"""
		if isbn not in self.ht:
			raise Error("deleting value that is not in the cache!!")
		
		nodeToDelete = self.ht[isbn]
		
		# need to change 2 ptrs: node.prev.next = node.next, node.next.prev = node.prev
		nodeToDelete.prev.next = nodeToDelete.next
		nodeToDelete.next.prev = nodeToDelete.prev
		
		self.ht.pop(isbn)
		self.length -= 1
		
		return nodeToDelete
	
	def insert(self, isbn, price):
		# check if isbn exists
		# if isbn exists, move to front of queue
		# insert if not
		# requires _insert, _pop (if too long), _delete (to delete then move to front)
		if isbn in self.ht:
			deleted = self._delete(isbn)
			self._insert(isbn, deleted.price)
		else:
			self._insert(isbn, price)
			if self.length > self.capacity:
				self._pop()
	
	def remove(self, isbn):
		# check if isbn exists in ht, then remove or throw error
		return self._delete(isbn)
	
	def lookup(self, isbn):
		# check if isbn in ht, if so, move to front of queue
		# needs _delete, _insert
		if isbn in self.ht:
			self.insert(isbn, None)
			return self.ht[isbn].price
		
		# not found 
		return -1

def isbnCacheTest():
	cache = IsbnCache(3)
	
	clear()
	
	cache.insert("book1", "5")
	print("Expecting 5: ", cache.lookup("book1"))
	cache.insert("book2", "6")
	print("Expecting 6: ", cache.lookup("book2"))
	cache.insert("book3", "7")
	print("Expecting 7: ", cache.lookup("book3"))
	cache.insert("book4", "8")
	print("Expecting 8: ", cache.lookup("book4"))
	
	try:
		cache.remove("book1")
		print("remove failed to throw error when removing non existant entry")
	except:
		print("remove successfully throws error when removing non existant entry")
	
	print("Expecting -1 since capacity was passed and this entry book1 should be LRU removed: ", cache.lookup("book1"))
	
	cache.remove("book4")
	print("Expecting -1 since delete entry called on book4: ", cache.lookup("book4"))
	
	
	cache.insert("book5", "9")
	print("Expecting 9: ", cache.lookup("book5"))
	
	
	cache.insert("book6", "10")
	print("Expecting 10: ", cache.lookup("book6"))
	
	
	print("Expecting -1 since capacity was passed again after some deletes and inserts and this entry book2 should be LRU removed: ", cache.lookup("book2"))
	
	print("Expecting 9: ", cache.lookup("book5"))
	print("Expecting 7: ", cache.lookup("book3"))
	print("Expecting 10: ", cache.lookup("book6"))
	
	
	cache.insert("book7", "11")
	print("Expecting 11: ", cache.lookup("book7"))
	
	print("Expecting -1 since capacity was passed again after some deletes and inserts and this entry book2 should be LRU removed: ", cache.lookup("book5"))

isbnCacheTest()
	
"""
12.4 Compute LCA, close ancestor optimized

Normally:
we use a algorithm similar to the linked list intersection algo
Determine distance to root from both nodes
adjust to equal distances, check parents from there
O(h) (h- node height max (a, b)) minimum runtime
O(1) mem

Adjusted for close:
Brute:
O(h) (distance to parent max (a, b)) runtime
O(h) mem

"""

class TreeNode:
	def __init__(self, val=0, left=None, right=None, parent=None):
		self.val = val
		self.left = left
		self.right = right
		self.parent = parent


def lcaClose(a, b):
	nodeSet = set()
	
	while a is not None or b is not None:
		if a:
			if a in nodeSet:
				return a
			nodeSet.add(a)
			a = a.parent
		if b:
			if b in nodeSet:
				return b
			nodeSet.add(b)
			b = b.parent
	
	return None

def lcaCloseTest():
	c = TreeNode(512)
	a = TreeNode(5)
	a.parent = c
	b = TreeNode(15)
	b.parent = c
	
	print("Expecting 512: ", lcaClose(a, b).val)
	
	d = TreeNode(3)
	c = TreeNode(22, d, b)
	a.parent = d
	b.parent = c
	d.parent = c
	
	print("Expecting 22: ", lcaClose(a, b).val)

lcaCloseTest()


"""
12.5 Nearest repeated entries in an array

input: array of word strings
output: closest pair of same words

alg:
hash table
key: word
value: index of appearance

if cur word in ht:
curIndex - ht[curWord] = distance
minDistance = min(distance, minDistance)
"""

def nearestRepeatedEntries(A):
	ht = {}
	minDist = float("inf")
	for i in range(len(A)):
		s = A[i]
		if s in ht:
			minDist = min(minDist, i - ht[s])
		ht[s] = i
	
	if minDist == float("inf"):
		return None
		
	return minDist

def nearestRepeatedEntriesTest():
	clear()
	
	A = ["All", "work", "and", "no", "play", "makes", "for", "no", "work", "no", "fun", "and", "no", "results"]
	
	print("Expecting 2: ", nearestRepeatedEntries(A))

nearestRepeatedEntriesTest()


"""
12.6 smallest subarray

input: array of strings (page), set of strings (keywords)

output: shortest subarray of the page with the set

idea:
track location of keywords as we go across
whenever we see the keywords, save their location
whenever we save their location, if we have seen all keywords, check the length between the farthest and the current keyword 
	--this is a candidate subarray
	
can use ordered dict to track the first one 
"""

def smallestSubarray(A, S):
	SmallestSubarray = collections.namedtuple('SmallestSubarray', ['start', 'end'])
	def first(C):
		return next(iter(C))
	
	def isSmaller(A, B):
		return (A.end - A.start) < (B.end - B.start)
	
	locs = collections.OrderedDict()
	
	sol = SmallestSubarray(0, len(A) - 1)
	for i in range(len(A)):
		item = A[i].lower()
		if item in S:
			if item in locs:
				locs.pop(item)
			locs[item] = i
		
		if len(locs) == len(S):
			cur = SmallestSubarray(locs[first(locs)], i)
			print(cur, sol)
			if isSmaller(cur, sol):
				sol = cur
	
	return sol
	

def smallestSubarrayTest():
	A = "If there be those who would not save the Union unless they could at the same time destroy slavery, I do not agree with them. My paramount object in this struggle is to save the Union, and is not either to save or to destroy slavery.".split(" ")
	S = "union save".split(" ")
	
	clear()
	print("Expecting 7, 9", smallestSubarray(A, S))
	
	A = "apple banana apple apple dog cat apple dog banana apple cat dog".split(" ")
	S = "banana cat".split(" ")
	
	clear()
	print("Expecting 8, 10", smallestSubarray(A, S))
	
smallestSubarrayTest()


"""
12.9 longest interval length

input: set of integers
output: size of largest SUBSET of contiguous integers

sample : 3 -2 7 9 8 1 2 0 -1 5 8
output: (-2 -1 0 1 2 3).size = 6

solution:
brute force: sort the array, traverse counting contiguous numbers
nlogn
o1

better:
hash table store the entries

pass through the array, creating longest contained interval from those pts
"""

def longestSubintervalLength(A):
	ht = {}
	maxLength = [0]
	
	for item in A:
		ht[item] = None
	
	def helper(num):
		if num in ht and ht[num] is not None:
			return ht[num]
		elif num in ht:
			# creating or using subsolutions, dynamic!
			subarray = None
			if num + 1 in ht and ht[num + 1] is not None:
				subarray = ht[num + 1]
			else:
				subarray = helper(num + 1)
			ht[num] = subarray + [num]
			
			# solution tracker
			maxLength[0] = max(maxLength[0], len(ht[num]))
			
			return ht[num]
			
		return []
	
	#can traverse keys in ht here, is duplicates exist it is faster
	for item in A:
		helper(item)
	
	return maxLength
	
"""
keeping in mind, each item is only part of one subinterval, we can remove the item from our candidates after passing it
"""
def longestSubintervalLength2(A):
	# build set
	unprocessed_entries = set()
	for item in A:
		unprocessed_entries.add(item)
	
	
	maxLength = 0
	while unprocessed_entries:
		cur = lower_bound = higher_bound = next(iter(unprocessed_entries))
		unprocessed_entries.remove(cur)
		
		while lower_bound - 1 in unprocessed_entries:
			lower_bound = lower_bound - 1
			unprocessed_entries.remove(lower_bound)
		
		while higher_bound + 1 in unprocessed_entries:
			higher_bound = higher_bound + 1
			unprocessed_entries.remove(higher_bound)
		
		
		maxLength = max(maxLength, (higher_bound - lower_bound + 1))
	
	return maxLength
	
def longestSubintervalLengthTest():
	A = [3, -2, 7, 9, 8, 1, 2, 0, -1, 5, 8]
	
	clear()
	print("Expecting 6, ", longestSubintervalLength(A))
	
longestSubintervalLengthTest()

def longestSubintervalLength2Test():
	A = [3, -2, 7, 9, 8, 1, 2, 0, -1, 5, 8]
	
	clear()
	print("Expecting 6, ", longestSubintervalLength2(A))
	
longestSubintervalLength2Test()