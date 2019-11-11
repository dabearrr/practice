from collections import deque, namedtuple
import math
import random

def clear():
	print("-----------------------")

"""
CTCI 3.2

Stack Min:

design a stack with push, pop, and min

push and pop in O(1) is easy

linked list with head pointer and tail pointer can handle O(1) push / pop

min:
as items are inserted, we can track the min seen, then return it on min calls

what if the min is popped?
doesnt work

we can track all the mins as we push into a linked list called mins

if the min is popped, pop from the mins as well

"""

class MinStack:
	class Node:
		def __init__(self, val, prev, next):
			self.val = val
			self.prev = prev
			self.next = next
	
	def __init__(self):
		self.head = None
		self.tail = None
		self.minHead = None
		self.minTail = None
	
	def push(self, item):
		if not self.head:
			self.head = Node(item, None, None)
			self.tail = self.head
		else:
			self.tail.next = Node(item, self.tail, None)
			self.tail = self.tail.next
		
		# handle min tracking
		if not self.minHead:
			self.minHead = Node(item, None, None)
			self.minTail = self.minHead
		elif item < self.minTail.val:
			self.minTail.next = Node(item, self.minTail, None)
			self.minTail = self.minTail.next
	
	def pop(self):
		if not self.head:
			return # can throw error here too
		if self.head is self.tail:
			self.head = None
			self.tail = None
			self.minHead = None
			self.minTail = None
		else:
			if self.tail is self.minTail:
				self.minTail = self.minTail.prev
				self.minTail.next = None
			self.tail = self.tail.prev
			self.tail.next = None

"""
18.3 Set of Stacks

In real life, when a plate stack gets too big, we use another stack.

Implement a set of stacks with max capacities, which creates a new stack when one gets too large.

FOLLOW UP:
it should have popAt(stackIndex), which pops from a specific stack.

we will need a list of stacks
"""

class SetOfStacks:
	def __init__(self, maxCapacity):
		self.stacks = [[]]
		self.maxCapacity = maxCapacity
		self.cur = 0
	def push(self, item):
		curStack = self.stacks[self.cur]
		if len(curStack) < self.maxCapacity:
			curStack.append(item)
		else:
			self.cur += 1
			if len(self.stacks) <= self.cur:
				self.stacks.append([item])
			else:
				self.stacks[self.cur].append(item)
	def pop(self):
		ans = None
		
		if len(self.stacks[self.cur]) > 0:
			ans = self.stacks[self.cur].pop()
		else:
			if self.cur > 0:
				self.cur -= 1
			else:
				return None
			ans = self.stacks[self.cur].pop()
			
		if len(self.stacks[self.cur]) == 0:
			self.cur -= 1
		
		return ans

class SetOfStacksFollowUp:
	def __init__(self, maxCapacity):
		self.stacks = [[]]
		self.maxCapacity = maxCapacity
		self.cur = [0]
	def push(self, item):
		curStack = self.stacks[self.cur[-1]]
		if len(curStack) < self.maxCapacity:
			curStack.append(item)
		else:
			self.cur[-1] += 1
			if len(self.stacks) <= self.cur[-1]:
				self.stacks.append([item])
			else:
				self.stacks[self.cur[-1]].append(item)
	def pop(self):
		ans = None
		
		if len(self.stacks[self.cur[-1]]) > 0:
			ans = self.stacks[self.cur[-1]].pop()
		else:
			if self.cur[-1] > 0:
				self.cur[-1] -= 1
			else:
				return None
			ans = self.stacks[self.cur].pop()
			
		if len(self.stacks[self.cur]) == 0:
			self.cur -= 1
		
		return ans
		
def setOfStacksTest():
	stacks = SetOfStacks(2)
	
	stacks.push(1)
	stacks.push(2)
	stacks.push(3)
	stacks.push(4)
	stacks.push(5)
	stacks.push(6)
	stacks.push(7)
	stacks.push(8)
	stacks.push(9)
	
	clear()
	print("Expecting 9 8 7 6 5 4 3 2 1 None")
	print(stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop())
	
	
	stacks.push(9)
	stacks.push(8)
	stacks.push(7)
	stacks.push(6)
	stacks.push(5)
	stacks.push(4)
	stacks.push(3)
	stacks.push(2)
	stacks.push(1)
	
	
	print("Expecting 1 2 3 4 5 6 7 8 9 None")
	print(stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop(), stacks.pop())

setOfStacksTest()

"""
3.4 implement a queue with two stacks

we can have a push stack and pop stack

if push is called while pop stack is in use, move to push stack
vice versa

O(n) push and pop
O(n) space

we can track a stack newest and a stack oldest
when peek or pop is called, we check if oldest is empty. if empty, move newest to oldest

on push we just push to stack newest
"""

class TwoStackQueue:
	def __init__(self):
		self.stackNewest = []
		self.stackOldest = []
		
	def size(self):
		return len(self.stackNewest) + len(self.stackOldest)
	
	def push(self, item):
		self.stackNewest.append(item)
	
	def shiftStacksIfNeeded(self):
		if len(self.stackOldest) < 1:
			while self.stackNewest:
				self.stackOldest.append(self.stackNewest.pop())
	
	def peek(self):
		self.shiftStacksIfNeeded()
		return self.stackOldest[-1]
	
	def pop(self):
		self.shiftStacksIfNeeded()
		return self.stackOldest.pop()
		
def twoStackQueueTest():
	queue = TwoStackQueue()
	
	clear()
	queue.push(1)
	queue.push(2)
	queue.push(3)
	print(queue.pop())
	print(queue.pop())
	queue.push(4)
	print(queue.pop())
	print(queue.pop())

twoStackQueueTest()

"""
3.5 sort stack

sort a stack st smallest items are on the top

"""

def sortStack(stack):
	unsorted = stack
	
	#sorted will have reverse order sort -- then we can move back to unsorted
	sorted = []
	
	sorted.append(unsorted.pop())
	
	while unsorted:
		count = 0
		temp = unsorted.pop()
		
		while len(sorted) > 0 and sorted[-1] > temp:
			unsorted.append(sorted.pop())
			count += 1
		
		sorted.append(temp)
		
		for i in range(count):
			sorted.append(unsorted.pop())
			
	while sorted:
		unsorted.append(sorted.pop())
	
def sortStackTest():
	unsorted = [5, 1, 2, 7, 0, 8]
	
	sortStack(unsorted)
	
	while unsorted:
		print(unsorted.pop(), " ")
		
sortStackTest()

"""
3.6 Animal Stacks
enqueue
dequeue (Any, Dog, Cat)

dequeue should always return the oldest in that set

brute force:
maintain 3 stacks, one for each set
on dog push or pop, perform op on both dog and all
on cat push or pop, perform op on both cat and all

better?
we can use a custom Node with two next pointers
next -> next oldest
nextType -> next same Type node

bsest:
use 2 stacks, with timestamp stored as well in the nodes
"""

class AnimalStacks:
	class Animal:
		def __init__(self, type, time):
			self.type = type
			self.time = time
	
	def __init__(self):
		self.dogQueue = deque()
		self.catQueue = deque()
		
		# tracks insertion time relative to others
		self.cur = 0
	
	def enqueue(self, item):
		new = Animal(item, self.cur)
		self.cur += 1
		
		if item == "dog":
			dogQueue.append(new)
		else:
			catQueue.append(new)
		
	def dequeueAny(self):
		if self.dogQueue and self.catQueue:
			topDog = self.dogQueue.peekFirst()
			topCat = self.catQueue.peekFirst()
			
			if topDog.time < topCat.time:
				return self.dogQueue.popleft()
			else:
				return self.catQueue.popleft()
		elif self.dogQueue:
			return self.dogQueue.popleft()
		elif self.catQueue:
			return self.catQueue.popleft()
		else:
			return None
			
	def dequeueDog(self):
		return self.dogQueue.popleft()
		
	
	def dequeueCat(self):
		return self.catQueue.popleft()

"""
EPI Stacks (chapter 8)
1 2 3 4 6 7 8
"""

"""
8.1 stack with max

Implement a stack with a max function

Brute force:
track max as we create the stack into a variable
when max is popped?
search the stack for next max

O(1) push
O(n) pop
O(n) space

better:
store each element as a pair (value, max at current element)
O(1) push
O(1) pop
O(n) space

best:
track max into a max stack
when max is popped?
pop from max stack as well

O(1) push
O(1) pop
O(n) space

"""

class StackWithMax():
	def __init__(self):
		self.stack = []
		self.maxStack = []
	
	def push(self, item):
		self.stack.append(item)
		
		# need less than or equal to here to account for duplicate maxes
		if not self.maxStack or self.maxStack[-1] <= item:
			self.maxStack.append(item)
	
	def pop(self):
		if not self:
			raise IndexError("pop() empty stack")
		ans = self.stack.pop()
		if ans == self.maxStack[-1]:
			self.maxStack.pop()
		
		return ans
		
	def max(self):
		if not self:
			raise IndexError("max() empty stack")
		return self.maxStack[-1]

"""
possible edge case:

5 maxStack = 4, 5
1
4
4 

-> pop
1 maxStack = 4
4
4

-> pop
4 maxStack = 4
4


-> pop
4 maxStack = [] -- issue!

we can solve this by push to maxStack on equal value as well
"""

def stackWithMaxTest():
	target = StackWithMax()
	
	target.push(2)
	target.push(1)
	target.push(4)
	"""
	4
	1
	2
	"""
	
	clear()
	
	print("expecting 4, ", target.max())
	print("expecting 4, ", target.pop())
	print("expecting 2, ", target.max())
	print("expecting 1, ", target.pop())
	print("expecting 2, ", target.max())
	print("expecting 2, ", target.pop())
	
def stackWithMaxTest2():
	target = StackWithMax()
	
	target.push(1)
	target.push(5)
	target.push(5)
	target.push(6)
	target.push(1)
	"""
	1
	6
	5
	5
	1
	"""
	
	clear()
	
	print("expecting 6, ", target.max())
	print("expecting 1, ", target.pop())
	print("expecting 6, ", target.max())
	print("expecting 6, ", target.pop())
	print("expecting 5, ", target.max())
	print("expecting 5, ", target.pop())
	print("expecting 5, ", target.max())
	print("expecting 5, ", target.pop())
	print("expecting 1, ", target.max())
	print("expecting 1, ", target.pop())
	
stackWithMaxTest()
stackWithMaxTest2()

"""
8.2 Evaluate RPN expressions

Reverse Polish Expressions
Numbers: "4" "-52" "300"

Expressions: A B o
"1, 2, x" = 2
"3, 4, +, 2, x, 1, +" = 15

"""

def expression(rpnString):
	EXP = {"+", "-", "x", "*", "/"}
	def isExpression(str):
		return str in EXP
	
	def operate(l, op, r):
		if op == "+":
			return int(l) + int(r)
		elif op == "-":
			return int(l) - int(r)
		elif op == "x" or op == "*":
			return int(l) * int(r)
		elif op == "/":
			return int(l) / int(r)
		else:
			raise InputError("bad operator")
	
	def expr(S):
		if not isExpression(S[-1]):
			return S.pop()
		
		op = S.pop()
		r = expr(S)
		l = expr(S)
		
		return operate(l, op, r)
	
	# remove whitespaces and split on comma
	stack = rpnString.replace(" ", "").split(",")
	
	return expr(stack)

def expressionTest():
	test1 = "1, 2, x"
	test2 = "3, 4, +, 2, x, 1, +"
	
	clear()
	print("Expecting 2, got: ", expression(test1))
	print("Expecting 15, got: ", expression(test2))

expressionTest()