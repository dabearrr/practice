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

"""
8.3

Matching parenthesis

validate if a string has correctly formatted parenthesis:

( ) [ ] { }

we can use a stack
compare stack.top to insert value

if new value is open, just add it
if new value is closed, it must match top or else return false

return true at end of string

o(n) runtime
o(n) space
"""

def isMatching(S):
	closed = {")" : "(", "[" : "]", "{" : "}"}
	stack = []
	
	for item in S:
		# means it's an open paren
		if item in closed.values():
			stack.append(item)
		elif item in closed:
			if not stack:
				return False
			elif closed[item] == stack[-1]:
				stack.pop()
			else:
				return False
		else:
			raise InputError(item, " is not a valid character")
	
	if stack:
		return False
	
	return True

def isMatchingTest():
	test = "[{}]()()[[(())]]"
	test2 = "[{}]()()[[(())]"
	test3 = "[{}]()()[[(())]}"
	
	clear()
	print("Expecting True ", test)
	print("Expecting False ", test2)
	print("Expecting False ", test3)
	
isMatchingTest()


"""
8.4 normalize paths

/././cool/../cool = /cool
cur/../cur = cur

take a path and turn it into its shortest form

start:
check if absolute or relative (does it start with slash)
. = dont do anything to stack
.. = stack pop
else = stack add




"""

def normalizePaths(path):
	def isAbsolute(path):
		return path[0] == "/"
	def stackToPath(stack):
		stack.reverse()
		return "/".join(stack)
	boolAbsolute = isAbsolute(path)
	splitPath = path.split("/")
	if boolAbsolute:
		splitPath = splitPath[1:]
	
	stack = []
	for section in splitPath:
		if section == "..":
			# if user goes too far back, error out
			if not stack:
				raise InputError("path is invalid, too many ..s")
			stack.pop()
		elif section == ".":
			continue
		else:
			stack.append(section)
			
	if boolAbsolute:
		return "/" + stackToPath(stack)
		
	return stackToPath(stack)
	
def normalizePathsTest():
	path1 = "/././cool/../cool"
	path2 = "cur/../cur"
	path3 = "cur/../cur/../.."
	
	clear()
	
	print("expecting /cool ", normalizePaths(path1))
	print("expecting cur ", normalizePaths(path2))
	
	try:
		print("expecting error")
		print(normalizePaths(path3))
	except:
		print("correctly errored out")
	finally:
		print("should say \" correctly errored out \" ^")

normalizePathsTest()

"""
8.6
Compute buildings with a sunset view


processing:
We reading in buildings from east to west
array = [2 1 4 6 5]

buildings will be
5 < 6 < 4 < 1 < 2

in this case, only 6 and 5 can see the west sunset,
the rest are blocked by 6 and 4

we can use a stack to process the array

whenever we see a new building, while stack.top() < new building, pop them from the stack

the resulting stack is the solution

runtime is O(n) (at worst we pop all the previous elements, processing 2n - 1 elements)
memory is o(n) (all buildings have sunset view and are added to the stack)
"""

def sunsetViews(A):
	stack = []
	
	for item in A:
		if stack:
			while stack and stack[-1] < item:
				stack.pop()
		stack.append(item)
	
	return stack

def sunsetViewsTest():
	B = [2, 1, 4, 6, 5, 7, 3]
	C = [100, 80, 101, 20, 21, 19, 30, 11, 6, 5, 12, 3, 4, 8, 7, 1]
	
	clear()
	print("Expecting 3 and 7: ", sunsetViews(B))
	print("Expecting 101 30 12 8 7 1: ", sunsetViews(C))

sunsetViewsTest()

"""
8.6 binary tree by depths

put nodes in lists for each depth
sorted from left to right

BFS:
Do a breadth first traversal, tracking the height as we go along the tree
we add to that height's list as we go across

DFS:
Do depth first traversal, passing the height recursively as we go along the tree
we add to that height's list as we go across
"""
class TreeNode:
	def __init__(self, val=None, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right
		
def bfsDepths(root):
	q = deque()
	
	# add root
	q.append(root)
	h = 0
	ans = []
	
	while q:
		temp = deque()
		while q:
			cur = q.popleft()
			if len(ans) < h + 1:
				ans.append([])
			ans[h].append(cur.val)
			if cur.left:
				temp.append(cur.left)
			if cur.right:
				temp.append(cur.right)
		h += 1
		q = temp
	
	return ans

def dfsDepths(root):
	ans = []
	
	def traverse(cur, height):
		if cur is None:
			return
		traverse(cur.left, height + 1)
		
		while len(ans) < height + 1:
			ans.append([])
		ans[height].append(cur.val)
		
		traverse(cur.right, height + 1)
	
	traverse(root, 0)
	
	return ans

def depthTest():
	testTree = TreeNode(314, TreeNode(6, TreeNode(271, TreeNode(28), TreeNode(0)), TreeNode(561, None, TreeNode(3, TreeNode(17)))), TreeNode(6, TreeNode(2, None, TreeNode(1, TreeNode(401, None, TreeNode(641)), TreeNode(257))), TreeNode(271, None, TreeNode(28))))
	
	clear()
	print(bfsDepths(testTree))
	print(dfsDepths(testTree))
	
depthTest()

"""
8.7 Implement a circular queue

array as a queue
resize dynamically

can start head and tail at dummy -1

insert at t + 1
"""

class CircleQueue:
	def __init__(self, capacity):
		self.capacity = capacity
		self.length = 0
		self.array = [None] * capacity
		self.head = None
		self.tail = None
	
	def getLength(self):
		return self.length
		
	def dequeue(self):
		if self.head is None and self.tail is None:
			raise Exception("popped from empty queue")
			
		ans = self.array[self.head]
		if self.head == self.tail:
			self.head = self.tail = None
		else:
			self.head = (self.head + 1) % self.capacity
		self.length -= 1
		
		return ans
	def resizeIsNeeded(self):
		return self.length == self.capacity
		
	def resize(self):
		self.array = self.array + [None] * self.capacity
		self.capacity *= 2
	
	def enqueue(self, value):
		if self.head is None and self.tail is None:
			self.head = 0
			self.tail = -1
		else:
			if self.resizeIsNeeded():
				self.resize()
		self.length += 1
		self.tail = (self.tail + 1) % self.capacity
		self.array[self.tail] = value

def circleQueueTest():
	q = CircleQueue(3)
	
	q.enqueue(1)
	q.enqueue(2)
	q.enqueue(3)
	
	print("expecting 1", q.dequeue())
	print("expecting 2", q.dequeue())
	q.enqueue(4)
	q.enqueue(5)
	print("expecting 3", q.dequeue())
	print("expecting 4", q.dequeue())
	print("expecting 5", q.dequeue())
	
	try:
		q.dequeue()
		print("did not throw error when dequeue was called on empty queue")
	except:
		print("correctly threw error when dequeue was called on empty queue")

def circleQueueTest2():
	q = CircleQueue(3)
	
	q.enqueue(1)
	q.enqueue(2)
	q.enqueue(3)
	q.enqueue(4) # triggers a resize
	q.enqueue(5)
	
	print("expecting 5", q.getLength())
	
	print("expecting 1", q.dequeue())
	print("expecting 4", q.getLength())
	print("expecting 2", q.dequeue())
	print("expecting 3", q.getLength())
	print("expecting 3", q.dequeue())
	print("expecting 2", q.getLength())
	print("expecting 4", q.dequeue())
	print("expecting 1", q.getLength())
	print("expecting 5", q.dequeue())
	print("expecting 0", q.getLength())
	
	try:
		q.dequeue()
		print("did not throw error when dequeue was called on empty queue")
	except:
		print("correctly threw error when dequeue was called on empty queue")

		
circleQueueTest()
circleQueueTest2()

"""
8.8 queue using stacks

ok lets try one stack

push 1 2 3

[1 2 3]
pop gets 3 x wrong

we can move it to a second stack

[3 2 1]
pop gets 1! good

if pop stack is empty move push stack to pop stack
then pop

else just pop from pop stack
"""

class QueueFromStacks:
	def __init__(self):
		self.pushStack = []
		self.popStack = []
	
	def push(self, value):
		self.pushStack.append(value)
	
	def pop(self):
		if not self.popStack:
			if not self.pushStack:
				raise Exception("pop called on empty queue")
			while self.pushStack:
				self.popStack.append(self.pushStack.pop())
		
		return self.popStack.pop()

def queueFromStacksTest():
	q = QueueFromStacks()
	
	q.push(1)
	q.push(2)
	q.push(3)
	
	clear()
	
	print("Expecting 1", q.pop())
	print("Expecting 2", q.pop())
	q.push(4)
	q.push(5)
	print("Expecting 3", q.pop())
	print("Expecting 4", q.pop())
	print("Expecting 5", q.pop())
	
	try:
		q.pop()
		print("Failed to error out on empty queue pop")
	except:
		print("Succeeded to error out on empty queue pop")

queueFromStacksTest()

"""
8.9 Queue with Max

We need a queue struct that also tracks the max of the queue

brute force:
search the whole array on max called
o(n) max runtime
o(1) mem

better:
track the max in a max stack, whenever an insert occurs, while top is less, pop it, then push
max is the bottom of the stack at all times
assuming a doubly linked list implementation
o(1) max runtime
o(n) mem (decreasing list)

however, insert becomes o(n) (worst case, decreasing list then a number greater than all the previous values)

"""

class QueueWithMax:
	def __init__(self):
		# this is a doubly linked list that we must interact with at both ends
		self.maxList = deque()
		self.queue = deque()
	
	def push(self, value):
		self.queue.append(value)
		
		if self.maxList:
			while self.maxList and self.maxList[-1] < value:
				self.maxList.pop()
		# always append to the end of the maxList
		self.maxList.append(value)
	
	def pop(self):
		if not self.queue:
			raise Exception("called pop on empty queue")
		
		# normal queue interaction
		ans = self.queue.popleft()
		
		if ans == self.maxList[0]:
			# if we popped the max, pop it from the maxlist on the left
			self.maxList.popleft()
		
		return ans
		
	def max(self):
		if not self.maxList:
			raise Exception("called max on empty list")
		
		# return the max at the left of the doubly linked list
		return self.maxList[0]

def queueWithMaxTest():
	q = QueueWithMax()
	
	q.push(5)
	q.push(3)
	q.push(8)
	q.push(6)
	
	clear()
	
	print("Expecting 8", q.max())
	print("Expecting 5", q.pop())
	print("Expecting 8", q.max())
	print("Expecting 3", q.pop())
	print("Expecting 8", q.max())
	print("Expecting 8", q.pop())
	print("Expecting 6", q.max())
	print("Expecting 6", q.pop())
	
	try:
		q.max()
		print("Failed to except on max called on empty queue")
	except:
		print("Succeeded to except on max called on empty queue")
	
	try:
		q.pop()
		print("Failed to except on pop called on empty queue")
	except:
		print("Succeeded to except on pop called on empty queue")

queueWithMaxTest()