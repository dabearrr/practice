from collections import deque, namedtuple
import math
import random

def clear():
	print("-----------------------")

def printLl(A):
	if A is None:
		print("NONE")
	temp = A
	while temp:
		print(temp.val, end = " ")
		temp = temp.next
	print("")

def printTreePre(A):
	if A is None:
		print("NONE")
	def helper(cur):
		if cur is not None:
			print(cur.val)
			helper(cur.left)
			helper(cur.right)
	helper(A)

def printTreePost(A):
	if A is None:
		print("NONE")
	def helper(cur):
		if cur is not None:
			helper(cur.left)
			helper(cur.right)
			print(cur.val)
	helper(A)

def printTree(A):
	if A is None:
		print("NONE")
	def helper(cur):
		if cur is not None:
			helper(cur.left)
			print(cur.val)
			helper(cur.right)
	helper(A)
"""
CTCI

4.1

check if a route exists between two nodes

brute force:
enumerate all routes from s, if any contain t, then True

O(n) runtime, O(n) space to store routes

better 
BFS or DFS from s, if node visited is t, return True

d = depth
o(k = amount of children from node ^ d) runtime, O(k^d) space

best:
bidirection search with s and t

o(k^(d/2)) runtime and space
"""

class Node:
	def __init__(self, val, children):
		self.val = val
		self.children = children
		self.visited = False
class Graph:
	def __init__(self, nodes):
		self.nodes = nodes

def hasRoute(s, t):
	class Node:
		def __init__(self, val, children):
			self.val = val
			self.children = children
			self.visited = False
	class Graph:
		def __init__(self, nodes):
			self.nodes = nodes
			
	def updateQueue(queue, node):
		for item in node.children:
			if not item.visited:
				queue.append(item)

	queueS = deque()
	queueT = deque()
	
	# initialize queues
	updateQueue(queueS, s)
	updateQueue(queueT, t)
	
	while queueS or queueT:
		if queueS:
			temp = queueS.popleft()
			if temp is t or temp.visited:
				return True
			temp.visited = True
			updateQueue(queueS, temp)
		if queueT:
			temp = queueT.popleft()
			if temp is s or temp.visited:
				return True
			temp.visited = True
			updateQueue(queueT, temp)
				
	return False
	
def hasRouteTest():
	b = Node(2, [])
	a = Node(1, [b])
	b.children.append(a)
	
	clear()
	print(hasRoute(a, b))
	
def hasRouteTest2():
	c = Node(3, [])
	d = Node(4, [])
	b = Node(2, [d])
	a = Node(1, [c])
	
	clear()
	print(hasRoute(a, b))
	
def hasRouteTest3():
	c = Node(3, [])
	d = Node(4, [])
	b = Node(2, [d])
	a = Node(1, [c])
	d.children.append(c)
	c.children.append(d)
	
	clear()
	print(hasRoute(a, b))

hasRouteTest()
hasRouteTest2()
hasRouteTest3()
	
"""
4.2

Given a sorted array with unique integer elements, write an algorithm to create a bst with minimal height

find middle value, set as root
pick middle of left side of middle and middle of right side of middle as childs
repeat for left and right
"""
def printTree(A):
	if A is None:
		return
	printTree(A.left)
	print(A.val)
	printTree(A.right)

class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right

def minTree(A):
	def findMiddleIndex(A):
		if len(A) <= 1:
			return 0
		else:
			return int((len(A) + 1) / 2)
		
	def minTreeHelper(A):
		if not A:
			return None
		
		mid = findMiddleIndex(A)
		cur = TreeNode(A[mid])
		cur.left = minTreeHelper(A[:mid])
		cur.right = minTreeHelper(A[mid+1:])
		
		return cur
		
	return minTreeHelper(A)

def minTreeTest():
	A = [1, 2, 3, 4, 5, 6, 7]
	
	clear()
	printTree(minTree(A))

def minTreeTest2():
	A = []
	
	clear()
	printTree(minTree(A))

minTreeTest()
minTreeTest2()

"""
4.3
List of Depths

Binary Tree
create a LL at each depth for all the nodes at that depth

Makes most sense with Breadth First Search, since it goes in order of depths

need to track depth somehow

can keep track of a temp queue for next Layer
"""

class llNode:
	def __init__(self, val=0, next=None):
		self.val = val
		self.next = next


		
def listOfDepths(root):
	if root is None:
		return []
	
	def updateQueue(queue, cur):
		if cur.left is not None:
			queue.append(cur.left)
		if cur.right is not None:
			queue.append(cur.right)
	
	listsList = []
	
	queue = deque()
	queue.append(root)
	
	tempQueue = deque()
	
	curHead = llNode()
	cur = curHead
	
	while queue:
		temp = queue.popleft()
		
		cur.next = llNode(temp.val)
		cur = cur.next
		
		updateQueue(tempQueue, temp)
		
		if not queue:
			listsList.append(curHead.next)
			curHead = llNode()
			cur = curHead
			queue = tempQueue
			tempQueue = deque()
	
	return listsList

def listOfDepthsTest():
	left = TreeNode(2, TreeNode(4), TreeNode(5))
	right = TreeNode(3, TreeNode(6), TreeNode(7))
	root = left = TreeNode(1, left, right)
	
	clear()
	ans = listOfDepths(root)
	print(len(ans))
	for item in ans:
		printLl(item)
		
listOfDepthsTest()

"""
4.4 Check Balanced

check if b tree is balanced

define balanced

the heights of the two subtrees of any node never differ by more than one
"""

def checkBalance(root):
	if root is None:
		return True
	
	def height(cur):
		if cur is None:
			return 0
		if cur.left is None and cur.right is None:
			return 1
		return max(height(cur.left), height(cur.right))

	return abs(height(root.left) - height(root.right)) < 2 and checkBalance(root.left) and checkBalance(root.right)

def checkBalance(root):
	if root is None:
		return True
	
	def getHeight(root):
		if root is None:
			return -1
		return max(getHeight(root.right), getHeight(root.left)) + 1
	
	heightDiff = abs(getHeight(root.left) - getHeight(root.right))
	
	if heightDiff > 1:
		return False
	
	return checkBalance(root.left) and checkBalance(root.right)
	
def checkBalanceTest():
	left = TreeNode(2, TreeNode(4), TreeNode(5))
	right = TreeNode(3, TreeNode(6), TreeNode(7))
	root = TreeNode(1, left, right)
	
	clear()
	print(checkBalance(root))
	
def checkBalanceTest2():
	left = TreeNode(2, TreeNode(4), TreeNode(5))
	right = TreeNode(3, TreeNode(6), None)
	root = left = TreeNode(1, left, right)
	
	clear()
	print(checkBalance(root))
	
def checkBalanceTest3():
	left = TreeNode(2, TreeNode(4), TreeNode(5))
	right = None
	root = left = TreeNode(1, left, right)
	
	clear()
	print(checkBalance(root))

checkBalanceTest()
checkBalanceTest2()
checkBalanceTest3()

"""
4.5 validate BST

we can perform an inorder traversal, comparing to the previous value checking that it is always increasing

we also need to consider the possibility of duplicates and how we will handle duplicates

assuming dupes go left
"""

def validateBst(root):
	def validateBstHelper(cur, minVal, maxVal):
		if cur is None:
			return True
		if cur.val < minVal or cur.val > maxVal:
			return False
		
		return validateBstHelper(cur.left, minVal, min(cur.val, maxVal)) and validateBstHelper(cur.right, max(minVal, cur.val), maxVal)
	
	return validateBstHelper(root, float('-inf'), float('inf'))
	
def validateBstTest():
	left = TreeNode(2, TreeNode(1), TreeNode(3))
	right = TreeNode(6, TreeNode(5), TreeNode(7))
	root = TreeNode(4, left, right)
	
	clear()
	print(validateBst(root))
	
	
def validateBstTest2():
	left = TreeNode(2, TreeNode(4), TreeNode(5))
	right = TreeNode(3, TreeNode(6), TreeNode(7))
	root = TreeNode(1, left, right)
	
	clear()
	print(validateBst(root))
	
def validateBstTest3():
	left = TreeNode(2, TreeNode(1), None)
	right = TreeNode(6, None, TreeNode(7))
	root = TreeNode(4, left, right)
	
	clear()
	print(validateBst(root))

def validateBstTest4():
	left = TreeNode(2, TreeNode(1), TreeNode(3))
	right = TreeNode(6, TreeNode(0), TreeNode(7))
	root = TreeNode(4, left, right)
	
	clear()
	print(validateBst(root))
	
def validateBstTest5():
	left = TreeNode(2, TreeNode(1), TreeNode(25))
	right = TreeNode(6, TreeNode(5), TreeNode(7))
	root = TreeNode(4, left, right)
	
	clear()
	print(validateBst(root))
	
validateBstTest()
validateBstTest2()
validateBstTest3()
validateBstTest4()
validateBstTest5()

"""
4.6 successor
nodes have parent link
Write an algroithm to find the inorder successor of the input node

brute force:
We can do an inorder traversal, if we find the node, set a flag to return the next node processed

steps to find next inorder node:
check cur.right ? return cur.right : check parent
check parent > cur ? parent : cur = parent, loop again checking parent > cur

"""
class TreeNode:
	def __init__(self, val=0, left=None, right=None, parent=None):
		self.val = val
		self.left = left
		self.right = right
		self.parent = parent


def leftmostChild(node):
	if node.left is None:
		return node
	return leftmostChild(node.left)

def findSuccessor(node):
	if node is None:
		return None
	if node.right is not None:
		return leftmostChild(node.right)
	
	# need to check parents
	def findGreaterParent(cur, val):
		if cur is None:
			return None
		if cur.val > val:
			return cur
		return findGreaterParent(cur.parent, val)
	
	return findGreaterParent(node.parent, node.val)

	
"""
4.7
Build order
if d requires a
graph points a -> d
select nodes with no incoming edges and remove them from the graph, removing their outgoing edges
repeat until graph is empty


"""

def buildOrder(A, D):
	def removeEdges(nodes, nodeToRemove):
		for key, value in nodes.items():
			if nodeToRemove in value:
				value.remove(nodeToRemove)
	
	
	nodes = {}
	for package in A:
		nodes[package] = set()
	
	# b depends on a
	for a, b in D:
		nodes[b].add(a)
	
	buildOrder = []
	
	edgesExist = True
	while edgesExist:
		foundEdge = False
		nodesToRemove = []
		for package in list(nodes):
			# no outgoing edges, pick this edge
			print(nodes[package])
			if len(nodes[package]) == 0:
				buildOrder.append(package)
				nodesToRemove.append(package)
				foundEdge = True
		if not foundEdge:
			# cycle exists
			return None
		if len(buildOrder) >= len(A):
			edgesExist = False
		for item in nodesToRemove:
			removeEdges(nodes, item)
			nodes.pop(item)
	return buildOrder

def buildOrderTest():
	values = ['a', 'b', 'c', 'd', 'e', 'f']
	dependencies = [('a', 'd'), ('f', 'b'), ('b', 'd'), ('f', 'a'), ('d', 'c')]
	
	clear()
	print(buildOrder(values, dependencies))

buildOrderTest()

"""
4.8
First common ancestor
do dfs, passing up a node if you find one of the two nodes.

if left and right pass up a node, return cur, else return left or right


"""

def firstCommonAncestor(root, nodeA, nodeB):
	def helper(cur, nodeA, nodeB):
		if cur is None:
			return None, False
		left = helper(cur.left, nodeA, nodeB)
		right = helper(cur.right, nodeA, nodeB)

		# found ancestor already
		if left[1] or right[1]:
			if left[1]:
				return left
			else:
				return right

		# cur is ancestor
		if (left[0] is nodeA and right[0] is nodeB) or \
		(left[0] is nodeB and right[0] is nodeA) or \
		(cur is nodeA and (left[0] is nodeB or right[0] is nodeB)) or \
		(cur is nodeB and (left[0] is nodeA or right[0] is nodeA)):
			return cur, True

		# cur is nodeA or nodeB and not an ancestor
		if cur is nodeA or cur is nodeB:
			return cur, False

		# one node found in left subtree
		if left[0] is nodeA or left[0] is nodeB:
			return left, False

		# one node found in right subtree
		if right[0] is nodeA or right[0] is nodeB:
			return right, False

		return None, False

	ans = helper(root, nodeA, nodeB)
	if ans[1]:
		return ans[0]
	else:
		return None

# simple case
def firstCommonAncestorTest():
	nodeA = TreeNode(4)
	nodeB = TreeNode(5)
	root = TreeNode(1, TreeNode(2, nodeA, nodeB), TreeNode(3))

	clear()
	print(firstCommonAncestor(root, nodeA, nodeB).val)

# one is an ancestor of the other
def firstCommonAncestorTest2():
	nodeB = TreeNode(5)
	nodeA = TreeNode(4, nodeB, None)
	root = TreeNode(1, TreeNode(2), TreeNode(3, nodeA, nodeB))

	clear()
	print(firstCommonAncestor(root, nodeA, nodeB).val)

# no common ancestor
def firstCommonAncestorTest3():
	nodeB = TreeNode(5)
	nodeA = TreeNode(4)
	root = TreeNode(1, TreeNode(2, nodeA, None), TreeNode(3))

	clear()
	print(firstCommonAncestor(root, nodeA, nodeB))

# none
def firstCommonAncestorTest4():
	nodeB = None
	nodeA = None
	root = None

	clear()
	print(firstCommonAncestor(root, nodeA, nodeB))

firstCommonAncestorTest()
firstCommonAncestorTest2()
firstCommonAncestorTest3()
firstCommonAncestorTest4()

"""
4.9
BST Sequences

build sequences from bottom up

Use a weave function to weave sequences as we go up

return fully weaved sequences
"""

def bstSeq(root):
	def weave(left, right, prefix, sequences):
		# print(left, right, prefix, sequences)
		if not left and not right:
			sequences.append(prefix)
			print(prefix)
		if left:
			newPrefix = prefix[:]
			newPrefix.append(left[0])
			weave(left[1:], right, newPrefix, sequences)
		if right:
			newPrefix = prefix[:]
			newPrefix.append(right[0])
			weave(left, right[1:], newPrefix, sequences)


	if root is None:
		return []
	l = bstSeq(root.left)
	r = bstSeq(root.right)
	sequences = []

	if not l and not r:
		sequences.append([root.val])
	for lSeq in l:
		for rSeq in r:
			weave(lSeq, rSeq, [root.val], sequences)

	return sequences
	
# simple example
def bstSeqTest():
	root = TreeNode(2, TreeNode(1), TreeNode(3))

	clear()
	print(bstSeq(root))

# complex example
def bstSeqTest2():
	root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, TreeNode(5), TreeNode(7)))

	clear()
	print(bstSeq(root))

bstSeqTest()
bstSeqTest2()
"""
4.10 
Check subtree

check if T2 is a subtree of T1

Method 1:
Turn T1 and T2 into a String using a preorder traversal, traverse T1 string looking for T2 string

runtime o(n + m)
mem: o(n)

0
12
1
34
2
56

node index = n
left child index = 2n + 1
right child index = 2n + 2

Method 2:
Perform a traversal of T1, if cur.val == T2 root.val, perform a tree compare. If compare is return true. Else continue traversal
runtime o(n + n*m)
mem: o(1)

"""

def checkSubtree(A, B):
	def treeString(root):
		if root is None:
			return "x"
		return str(root.val) + treeString(root.left) + treeString(root.right)
	Astring = treeString(A)
	Bstring = treeString(B)

	return Bstring in Astring

def checkSubtreeTest():
	subTree = TreeNode(2, TreeNode(4, None), None)
	root = TreeNode(1, subTree, TreeNode(3))
	clear()

	print(checkSubtree(root, subTree))

def checkSubtreeTest2():
	subTree = TreeNode(5)
	root = TreeNode(1, TreeNode(2, TreeNode(4, None), None), TreeNode(3))
	clear()

	print(checkSubtree(root, subTree))

checkSubtreeTest()
checkSubtreeTest2()

"""
4.11  Get random node

brute force approach:
tree.size

random.randint to pick 0 to tree size

traverse the tree in any fashion, until we rand amount of nodes, then return that node
O(n) runtime, O(1) memory

using properties of bst
assuming bst is balanced

we can traverse starting from the root, randomly pick left or right log(n) times, return once we hit rand amount of traversals, where rand = 0 to log(n), or we hit a leaf
This would only be truly random if the bst is balanced
O(log(n)) time, O(1) mem

actually we can ensure balancing of the tree, since we are implementing the Tree ourselves

"""

# assume our tree class auto balances BST
def getRandomNode(root, size):
	# here the depths are equally likely, which is not an equal distrubution of nodes.
	# randomDepth = random.randint(0, math.log(size - 1, 2))


	# now each depth is not equally likely, weighed by size
	randomDepth = math.log(random.randint(1, size), 2)

	curDepth = 0
	cur = root

	while curDepth < randomDepth:
		# randomly select direction, all nodes should be equally likely, does not work if the tree is not complete
		# randDir = random.randint(0, 1)

		# need to weigh the directions by the sizes of the subtrees
		print("fill this later")

	return cur


def getRandomNode(root, size):
	randIndex = random.randint(0, size - 1)

	queue = collections.deque()
	queue.append(root)
	index = 0
	while queue:
		cur = queue.popleft()
		if index == randIndex:
			return cur
		index += 1
		queue.append(cur.left)
		queue.append(cur.right)

	#should never be reached
	return None


"""
EPI
Chapter 9 B Trees

9.1, 9.4, 9.2, 9.12, 9.11, 9.13, 9.16
"""

"""
9.1

check height subtrees

if they differ by more than 1, return false
"""

def validateHeights(root):
	def getHeight(cur):
		if cur is None:
			return 0

		left = getHeight(cur.left)
		right = getHeight(cur.right)

		if left == float('-inf') or right == float('-inf'):
			return float('-inf')

		if abs(left - right) > 1:
			return float('-inf')

		return max(left, right) + 1

	if root is None:
		return True

	left = getHeight(root.left)
	right = getHeight(root.right)

	if left == float('-inf') or right == float('-inf'):
		return False

	return abs(left - right) < 2


def validateHeightTest():
	root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, TreeNode(6), TreeNode(7)))

	clear()
	print("should be True ", validateHeights(root))

def validateHeightTest2():
	root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)))

	clear()
	print("should be False ", validateHeights(root))

def validateHeightTest3():
	root = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5, TreeNode(6))), TreeNode(3))

	clear()
	print("should be False ", validateHeights(root))


validateHeightTest()
validateHeightTest2()
validateHeightTest3()

"""
9.2

Symmetric Tree

The right subtree is a reflection of the left subtree

runtime is O(n) since we potentially read the entire tree if it is symmetric

memory is O(1), we only store some pointers to traverse
"""

def symmetricTree(root):
	if root is None:
		return True
	def helper(left, right):
		if left is None and right is None:
			return True
		if left is None or right is None:
			return False
		return left.val == right.val and helper(left.left, right.right) and helper(left.right, right.left)
	return helper(root.left, root.right)

"""
9.3

Lowest Common Ancestor

We can do a preorder traversal, looking for either of the two nodes in the left or right subtrees
if one node is in the left subtree and the other node is in the right subtree, return cur

Assuming that least common ancestor cannot be nodeA or nodeB
"""

def lca(root, nodeA, nodeB):
	def helper(cur, nodeA, nodeB):
		# base case
		if cur is None:
			return None, False
		
		# found nodeA or nodeB
		if cur is nodeA or cur is nodeB:
			return cur, False
		
		left = helper(cur.left, nodeA, nodeB)
		right = helper(cur.right, nodeA, nodeB)
		
		# found ancestor already in subtree
		if left[1]:
			return left
		elif right[1]:
			return right
		
		# cur is ancestor
		if (left[0] is nodeA and right[0] is nodeB) or \
		(left[0] is nodeB and right[0] is nodeA):
			return cur, True
		
		# cur is not ancestor, nodeA, or NodeB AND subtrees do not contain ancestor, nodeA, or nodeB
		return None, False
	
	ans = helper(root, nodeA, nodeB)
	
	if ans[1]:
		return ans[0]
	return None

def lcaTest():
	nodeA = TreeNode(5)
	nodeB = TreeNode(7)
	
	root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, nodeA, nodeB))
	
	clear()
	print("Should return 6 (a node) ", lca(root, nodeA, nodeB).val)
	
def lcaTest2():
	nodeB = TreeNode(7)
	nodeA = TreeNode(5, nodeB, None)
	
	root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, nodeA, None))
	
	clear()
	print("Should return None ", lca(root, nodeA, nodeB))
	
def lcaTest3():
	nodeA = TreeNode(2, TreeNode(1), TreeNode(3))
	nodeB = TreeNode(6, TreeNode(5), TreeNode(7))
	
	root = TreeNode(4, nodeA, nodeB)
	
	clear()
	print("Should return 4 (a node) ", lca(root, nodeA, nodeB).val)
	
lcaTest()
lcaTest2()
lcaTest3()

"""
9.4

Lowest Common Ancestor with parent ptr

last sol:
We can do a preorder traversal, looking for either of the two nodes in the left or right subtrees
if one node is in the left subtree and the other node is in the right subtree, return cur

Assuming that least common ancestor cannot be nodeA or nodeB

Now what can we add with the parent ptr?

we dont have to traverse with the root, we have the nodes, we have parent pointers, just go up

brute force:
create a set of one traversal going up to the root.

perform the other traversal up, check if cur is in the set
if cur in set return True
if non in the second traversal in set return False

if the tree is balanced:
runtime o(log(n))
memory o(log(n))

tree is basically a ll:
runtime o(n)
memory o(n)

better!:
find the depth of each node

put a ptr at each node
increment the deeper one until the ptrs are at the same depth
climb up until curA is curB or either is None

if the tree is balanced:
runtime o(log(n))
memory o(1)

tree is basically a ll:
runtime o(n)
memory o(1)
"""

class TreeNodeParent:
	def __init__(self, val=0, left=None, right=None, parent=None):
		self.val = val
		self.left = left
		self.right = right
		self.parent = parent

def lcaParent(nodeA, nodeB):
	def depth(node):
		if node is None:
			return 0
		return depth(node.parent) + 1
	
	aDepth = depth(nodeA)
	bDepth = depth(nodeB)
	
	curA = nodeA
	curB = nodeB
	
	if bDepth > aDepth:
		aDepth, bDepth = bDepth, aDepth
		curA, curB = curB, curA
	
	while aDepth > bDepth:
		curA = curA.parent
	
	while curA is not None and curB is not None:
		if curA is curB:
			return curA
		curA = curA.parent
		curB = curB.parent
	
	return None

def lcaParentTest():
	root = TreeNodeParent(0)
	nodeA = TreeNodeParent(2, TreeNode(1), TreeNode(3), root)
	nodeB = TreeNodeParent(6, TreeNode(5), TreeNode(7), root)
	
	clear()
	print("Should return 0 (a node) ", lcaParent(nodeA, nodeB).val)

def lcaParentTest2():
	root = TreeNodeParent(0)
	root2 = TreeNodeParent(1)
	nodeA = TreeNodeParent(5, None, None, root)
	nodeB = TreeNodeParent(7, None, None, root2)
	
	clear()
	print("Should return None ", lcaParent(nodeA, nodeB))
	
lcaParentTest()
lcaParentTest2()

"""
9.11

Inorder Traversal O(1) space, no recursion
we have parent ptrs
we have to find the next node without using recursion or a queue

start = leftmost node of root
next = if right exists:
leftmostChildOfRight
else
next = parent if cur is parent.left else continue up until parent is None, then stop traversal
"""

def inorderNoSpace(root):
	def leftmostChild(node):
		while node.left is not None:
			node = node.left
		return node
	def lastNode(node):
		while node.right is not None:
			node = node.right
		return node
		
	cur = root
	last = lastNode(root)
	
	while cur.left is not None:
		cur = cur.left
	
	while cur is not last:
		# do work
		print(cur.val)
		
		if cur.right is not None:
			cur = leftmostChild(cur.right)
		else:
			next = cur
			while next.parent.left is not next:
				next = next.parent
			cur = next.parent

def inorderNoSpaceTest():
	root = TreeNodeParent(50)
	root.left = TreeNodeParent(25, None, None, root)
	root.left.left = TreeNodeParent(12, None, None, root.left)
	root.left.right = TreeNodeParent(37, None, None, root.left)
	root.left.right.left = TreeNodeParent(31, None, None, root.left.right)
	root.left.right.left.left = TreeNodeParent(29, None, None, root.left.right.left)
	root.left.right.left.left.left = TreeNodeParent(28, None, None, root.left.right.left.left)
	root.left.right.right = TreeNodeParent(43, None, None, root.left.right)
	root.right = TreeNodeParent(75, None, None, root)
	root.right.right = TreeNodeParent(100, None, None, root.right)
	root.right.right.left = TreeNodeParent(87, None, None, root.right.right)
	root.right.right.right = TreeNodeParent(125, None, None, root.right.right)
	
	clear()
	inorderNoSpace(root)

inorderNoSpaceTest()

"""
9.12

build tree from inorder and preorder traversal strings

preorder gives you root
inorder gives you inorder of left and right
preorder gives you preorder of left (next (n-1) / 2 chars) and right (after that)
"""

# slower

	# def helper(preorder, inorder):
		# if len(preorder) < 1 or len(inorder) < 1:
			# return None
		# cur = TreeNode(preorder[0])
		# curIndex = inorder.find(preorder[0])
		# leftInorder = inorder[:curIndex]
		# cur.left = helper(preorder[1:1 + len(leftInorder)], leftInorder)
		# cur.right = helper(preorder[1 + len(leftInorder):], inorder[curIndex + 1:])
		
		# return cur
	
	# return helper(preorder, inorder)

def treeBuilder(preorder, inorder):
	map = {data : i for i, data in enumerate(inorder)}
	def faster(pStart, pEnd, iStart, iEnd):
		if pStart >= pEnd or iStart >= iEnd:
			return None
		
		cur = TreeNode(preorder[pStart])
		length = map[preorder[pStart]] - iStart
		cur.left = faster(pStart + 1, pStart + 1 + length, iStart, map[preorder[pStart]])
		cur.right = faster(pStart + 1 + length, pEnd, map[preorder[pStart]] + 1, iEnd)
		
		return cur
	
	return faster(0, len(preorder) - 1, 0, len(inorder) + 1)
	
def treeBuilderTest():
	preorder = "HBFEACDGI"
	inorder = "FBAEHCDIG"
	
	clear()
	printTree(treeBuilder(preorder, inorder))
	
treeBuilderTest()


"""
9.13

We must traverse the string in the same manner as the tree was to create the string

we can use an iterator, we just need to make sure the right subtree is call after left since that is the preorder ordering

"""

def construct_preorder_graph(preorder):
	# this function reads the preorder string as it was created
	# due to the ordering of the recursion, recursion trees will terminate at correct locations
	def helper(preorder_iter):
		
		key = next(preorder_iter)
		
		if key is None:
			return None
		
		left_subtree = helper(preorder_iter)
		right_subtree = helper(preorder_iter)
		
		return TreeNode(key, left_subtree, right_subtree)
		
	return helper(iter(preorder))

def construct_preorder_graph_test():
	preorder = ['H', 'B', 'F', None, None, None, 'C', None, 'D', None, 'G', 'I', None, None, None]
	
	clear()
	printTree(construct_preorder_graph(preorder))

construct_preorder_graph_test()

"""
9.16
compute the right sibling tree

we need a next ptr on each node, pointing to the next node on this level

assume complete b tree

The natural approach is using breadth first search to do this

We can track what level we are on during the search by getting the length at the start

then we track cur and prev. prev starts as None

if prev is not None
prev.next = cur

on the depth transition
length = queue length
prev = None

so we dont cross levels
"""
class TreeNodeNext:
	def __init__(self, val=0, left=None, right=None, next=None):
		self.val = val
		self.left = left
		self.right = right
		self.next = next
		
def connectNextSibling(root):
	queue = deque()
	queue.append(root)
	
	length = 1
	prev = None
	while queue:
		if length <= 0:
			# new depth
			length = len(queue)
			prev = None
		cur = queue.popleft()
		
		if prev is not None:
			prev.next = cur
		
		if cur.left is not None:
			queue.append(cur.left)
		if cur.right is not None:
			queue.append(cur.right)
			
		prev = cur
		length -= 1
	
	return root
	
def connectNextSiblingTest():
	a = TreeNodeNext(4)
	root = TreeNodeNext(1, TreeNodeNext(2, a, TreeNodeNext(5)), TreeNodeNext(3, TreeNodeNext(6), TreeNodeNext(7)))
	
	connectNextSibling(root)
	clear()
	cur = a
	while cur is not None:
		print(cur.val)
		cur = cur.next
	
connectNextSiblingTest()


"""
EPI Chapter 14 BST

1 2 3 4 5 7 8
"""

"""
14.1

validateBst

we need to check if the tree is a valid bst
that means for each node, node > node.left and node < node.right

we need to track max seen and min seen

check if cur > min or cur < max at any time

assume no dupes
"""

def validateBst(root):
	def helper(cur, maxSeen, minSeen):
		if cur is None:
			return True
		if cur.val > maxSeen or cur.val < minSeen:
			return False
		return helper(cur.left, min(cur.val, maxSeen), minSeen) and helper(cur.right, maxSeen, max(minSeen, cur.val))
	
	return helper(root, float('inf'), float('-inf'))

def validateBstTest():
	root = TreeNode(4, None, TreeNode(6, TreeNode(7), None))
	
	clear()
	print("Expecting False: ", validateBst(root))

def validateBstTest2():
	root = TreeNode(4, None, TreeNode(6, None, TreeNode(9, TreeNode(8), None)))
	
	clear()
	print("Expecting True: ", validateBst(root))
	
def validateBstTest3():
	root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6, TreeNode(5), TreeNode(7)))
	
	clear()
	print("Expecting True: ", validateBst(root))
	
validateBstTest()
validateBstTest2()
validateBstTest3()

"""
14.2

find next node for input value in bst

seems that we can make a simple binary search for the input value in the BST
if the key exists, find next node
if the key does not exist, look at prev
if prev > input, return prev

if prev < input, find next node

finding next node:
it is either the leftmost child of cur.right or one of the parents
"""

def findNextNode(tree, value):
	def leftmostChild(node):
		while node.left is not None:
			node = node.left
		return node

	if tree is None:
		return None
		
	cur = tree
	prev = None
	nextLargest = float('inf')
	
	# perform a binary search for the value
	# prev contains the last node seen
	while cur is not None:
		prev = cur
		#track the next largest valued parent
		if cur.val > value and cur.val < nextLargest:
			nextLargest = cur.val
			
		# traverse
		if value < cur.val:
			cur = cur.left
		elif value > cur.val:
			cur = cur.right
		else:
			# value is cur, break
			prev = cur
			cur = None
	
	# prev is the next largest node
	if value < prev.val:
		return prev.val
	
	# prev is just before the next largest node
	# case where next value is in the parents, we tracked it in nextLargest
	if prev.right is not None:
		# case where next value is leftmostchild of right
		return leftmostChild(prev.right).val
	elif nextLargest == float('inf'):
		# there is no larger key
		return None
	else:
		# next largest key is in parents
		return nextLargest
		
def findNextNode2(tree, value):
	subtree = tree
	first_so_far = None
	
	while subtree:
		if subtree.val > value:
			first_so_far, subtree = subtree, subtree.left
		else:
			subtree = subtree.right
	
	if first_so_far:
		return first_so_far.val
	else:
		return None

def findNextNodeTest():
	tree = TreeNode(8, TreeNode(4, TreeNode(2), TreeNode(6)), TreeNode(12, TreeNode(10), TreeNode(14)))
	
	clear()
	print("expecting 10", findNextNode(tree, 9))
	print("expecting 10", findNextNode2(tree, 9))
	
def findNextNodeTest2():
	tree = TreeNode(8, TreeNode(4, TreeNode(2), TreeNode(6)), TreeNode(12, TreeNode(10), TreeNode(14)))
	
	clear()
	print("expecting None", findNextNode(tree, 14))
	print("expecting None", findNextNode2(tree, 14))
	
def findNextNodeTest3():
	tree = TreeNode(8, TreeNode(4, TreeNode(2), TreeNode(6)), TreeNode(12, TreeNode(10), TreeNode(14)))
	
	clear()
	print("expecting 12", findNextNode(tree, 10))
	print("expecting 12", findNextNode2(tree, 10))
	
def findNextNodeTest4():
	tree = TreeNode(8, TreeNode(4, TreeNode(2), TreeNode(6)), TreeNode(12, TreeNode(10), TreeNode(14)))
	
	clear()
	print("expecting 10", findNextNode(tree, 8))
	print("expecting 10", findNextNode2(tree, 8))
	

findNextNodeTest()
findNextNodeTest2()
findNextNodeTest3()
findNextNodeTest4()

"""
14.3
find the k largest elements in a BST

brute force:
	do an inorder traversal, save the last k elements and return them
	o(n) space and runtime
	
better:
	do a reversed inorder traversal!
	node.right
	#do work
	add to list
	node.left
	
	o(h + k) runtime, o(k) space
	

"""
def kLargestElements(root, k):
	list = []
	
	def helper(cur):
		if cur is None or len(list) >= k:
			return
		helper(cur.right)
		if len(list) < k:
			list.append(cur.val)
		helper(cur.left)
	
	helper(root)
	return list

def kLargestElementsTest():
	tree = TreeNode(8, TreeNode(4, TreeNode(2), TreeNode(6)), TreeNode(12, TreeNode(10), TreeNode(14)))
	
	clear()
	print("Expecting 14, 12", kLargestElements(tree, 2))

def kLargestElementsTest2():
	tree = TreeNode(8, TreeNode(4, TreeNode(2), TreeNode(6)), TreeNode(12, TreeNode(10), TreeNode(14)))
	
	clear()
	print("Expecting []", kLargestElements(tree, 0))

def kLargestElementsTest3():
	tree = TreeNode(4, None, TreeNode(8, None, TreeNode(64)))
	
	clear()
	print("Expecting 4, 8, 64", kLargestElements(tree, 4))
	
kLargestElementsTest()
kLargestElementsTest2()
kLargestElementsTest3()


"""
14.4
Compute the lowest common ancestor in a BST

we can perform a BST traversal

we follow the range of the two nodes passed

once the node we are at is less than the largest and greater than the smallest, we return the node

runtime is o(h) , mem is o(1)
"""

# assuming there are no equal nodes in the tree
# assuming nodes passed are in the tree
def lcaBst(root, nodeA, nodeB):
	cur = root
	
	while cur:
		if (cur.val > nodeA.val and cur.val < nodeB.val) or (cur.val < nodeA.val and cur.val > nodeB.val):
			return cur
		elif cur.val > nodeA.val and cur.val > nodeB.val:
			cur = cur.left
		else:
			cur = cur.right
	
	return None

def lcaBstTest():
	a = TreeNode(4, TreeNode(2), TreeNode(6))
	b = TreeNode(16, TreeNode(14), TreeNode(18))
	root = TreeNode(30, TreeNode(8, a, b), None)
	
	clear()
	print("expecting 8: ", lcaBst(root, a, b).val)
	
def lcaBstTest2():
	a = TreeNode(4, TreeNode(2), TreeNode(6))
	b = TreeNode(16, TreeNode(14), TreeNode(18))
	root = TreeNode(1, None, TreeNode(8, a, b))
	
	clear()
	print("expecting 8: ", lcaBst(root, a, b).val)
	
lcaBstTest()
lcaBstTest2()


"""
14.5
Reconstruct a BST from traversal data!

preorder and postorder have unique traversals

we need to use the bst property to terminate traversals
"""


# REMEMBER!!! WINDOW IS DECREASING FOR BST CREATION / VALIDATION
# A is a preorder array
def bstFromPre(A):
	# tracks our position in the preorder array
	rootIndex = [0]
	
	#builds the binary tree
	def helper(maxSeen, minSeen):
		if rootIndex[0] == len(A):
			return None
		
		root = A[rootIndex[0]]
		
		if root >= minSeen and root <= maxSeen:
			# key is in correct position of the tree, thus we iterate
			rootIndex[0] += 1
			
			leftSubtree = helper(min(root, maxSeen), minSeen)
			rightSubtree = helper(maxSeen, max(root, minSeen))
			
			return TreeNode(root, leftSubtree, rightSubtree)
		else:
			# key is in incorrect tree position
			return None
	
	return helper(float('inf'), float('-inf'))

def bstFromPreTest():
	arr = [43,23,37,29,31,41,47,53]
	
	clear()
	print("Expecting ", arr)
	printTreePre(bstFromPre(arr))
	
bstFromPreTest()
		
def bstFromPost(A):
	
	# current index, using array to have a global pos
	rootIndex = [len(A) - 1]
	
	# generates the tree. Similar to BST validation, we need to maintain a window of valid values for the BST
	# if the window is breached, this key is in the wrong position, so return up recursively
	def helper(maxSeen, minSeen):
		# too far, post order is in reverse
		if rootIndex[0] < 0:
			return None
		
		# get key
		root = A[rootIndex[0]]
		
		if root >= minSeen and root <= maxSeen:
			# valid position for key
			# iterate, in reverse since post order traversal tells us info in reverse (root is last, right subtree before root, left subtree before right subtree)
			rootIndex[0] -= 1
			
			# right appears first in reversed post order string
			rightSubtree = helper(maxSeen, max(minSeen, root))
			leftSubtree = helper(min(maxSeen, root), minSeen)
			
			return TreeNode(root, leftSubtree, rightSubtree)
		else:
			# invalid position for root
			return None
		
	return helper(float('inf'), float('-inf'))

def bstFromPostTest():
	arr = [31,29,41,37,23,53,47,43]
	
	clear()
	print("Expecting ", arr)
	printTreePost(bstFromPost(arr))
	
bstFromPostTest()



		
"""
14.7

Enumerate numbers of the form a + b root 2

brute force:
	compute all combinations of (0 - k)a and (0-k)b, sort to get the k smallest
	o(k^2) runtime
	o(k^2) mem
	
better:
	use a heap, compute all combinations of (0 - k)a and (0-k)b, heap extract min k times

best:
	create a bst class with extract min and insert
	we insert 0 + 0 root2 at the start
	we extract minimum and insert two entries to the bst, (minimum.a+1) and (minimum.b+1)
	insert will cover situations with two insertions of equal values
	
	call min and insert 2 k times
	
	
"""
def calcAbRoot2(a, b):
	return a + (b * math.sqrt(2))

class AbNode():
	def __init__(self, a=0, b=0, left=None, right=None):
		self.a = a
		self.b = b
		self.left = left
		self.right = right
	def calcValue(self):
		return calcAbRoot2(self.a, self.b)

class AbTree:
	def __init__(self):
		self.root = AbNode(0, 0, None, None)
	def insert(self, a, b):
		nodeToInsert = AbNode(a, b, None, None)
		
		# root is None, insert at root
		if self.root is None:
			self.root = nodeToInsert
			return nodeToInsert
		
		# root is not None, need to perform a binary search
		prev = None
		cur = self.root
		value = calcAbRoot2(a, b)
		
		# perform a binary search
		while cur:
			prev = cur
			if value < cur.calcValue():
				cur = cur.left
			elif value > cur.calcValue():
				cur = cur.right
			else:
				# no value will be inserted, since this key is already inside the BST
				return None
		
		# insert the node
		if value < prev.calcValue():
			prev.left = nodeToInsert
		else:
			prev.right = nodeToInsert
		
		return nodeToInsert
		
	def extractMin(self):
		if self.root is None:
			return None
		
		prev = None
		cur = self.root
		
		# navigate to leftmost node
		while cur.left:
			prev = cur
			cur = cur.left
		
		# means that root is not the leftmost Node
		if prev:
			prev.left = None
		else:
			# root is the leftmost node, pull up right
			self.root = self.root.right
			
		return cur
		
def kSmallestAb(k):
	ans = []
	
	# initalized to 0, 0 as root
	abTree = AbTree()
	
	# extractmin k times, each time inserting slightly larger a, b nodes
	while len(ans) < k:
		minInTree = abTree.extractMin()
		
		ans.append((minInTree.a, minInTree.b))
		abTree.insert(minInTree.a + 1, minInTree.b)
		abTree.insert(minInTree.a, minInTree.b + 1)
	
	return ans
	
	

def AbTest():

	clear()
	print(kSmallestAb(8))

AbTest()

"""
14.8

Build a minimum height BST from a sorted array

We can continuously select the middle value of the array, then pass the left and right subarrays into a recursive function to do it again

this will create a balanced min height BST	
"""

def buildMinHeightBst(A):
	def helper(A, lowBound, highBound):
		if lowBound > highBound:
			return None
		elif lowBound == highBound:
			return TreeNode(A[lowBound])
		
		middle = int((lowBound + highBound) / 2)
		leftSubtree = helper(A, lowBound, middle - 1)
		rightSubtree = helper(A, middle + 1, highBound)
		
		return TreeNode(A[middle], leftSubtree, rightSubtree)
	
	return helper(A, 0, len(A) - 1)

def buildMinHeightBstTest():
	arr = [1, 2, 3, 4, 5, 6, 7]
	
	clear()
	print("Expecting: ", arr)
	printTree(buildMinHeightBst(arr))
	
buildMinHeightBstTest()


"""
EPI Chapter 18
1 2 3 5 7

Graphs!!

"""

"""
18.1 

find a path in a maze to the end!

Maze consists of 2d array of walls and open spaces

top right is exit
bottom left is start

we need the path from start to exit

we can do this using a graph
vertices are array entries (0, 0) (0, 1) etc
edges are neighbors that are open
"""


"""
We can simplify here, we dont need a graph class, we just need our start nodes, with it's children enumerated

val can just be the position of the node, so we can easily construct the path
"""
def findMazePath(maze):
	class Node:
		def __init__(self, val, children):
			self.val = val
			self.children = children
			self.visited = False
	class Graph:
		def __init__(self, nodes={}):
			self.nodes = nodes
	
	def buildGraph(maze):
		nodes = {}
		
		for i in range(0, len(maze)):
			for j in range(0, len(maze)):
				newNode = Node((i, j), [])
				
				# add valid graph edges
				if i > 0 and maze[i - 1][j]:
					newNode.children.append((i - 1, j))
				if i < len(maze) - 1 and maze[i + 1][j]:
					newNode.children.append((i + 1, j))
				if j > 0 and maze[i][j - 1]:
					newNode.children.append((i, j - 1))
				if j < len(maze[i]) - 1 and maze[i][j + 1]:
					newNode.children.append((i, j + 1))
				nodes[(i, j)] = newNode
				print(newNode.val, newNode.children)
		return Graph(nodes)
	
	# assuming start is always bottom left and open
	def findPath(graph, start, end):
		def helper(cur, path):
			# stop traversal
			if cur is None:
				return (False, None)
			
			# mark as traversed, continue path
			cur.visited = True
			path.append(cur.val)
			
			# stop traversal
			if cur is end:
				return (True, path)
			
			print(cur.val)
			
			for child in cur.children:
				childNode = graph.nodes[child]
				if childNode.visited == False:
					childResponse = helper(childNode, path[:])
					print(childResponse)
					if childResponse[0]:
						return childResponse
			
			return (False, None)
		return helper(start, [])
		
	graph = buildGraph(maze)
	print(graph)
	return findPath(graph, graph.nodes[(len(maze) - 1, 0)], graph.nodes[(0, len(maze[0]) - 1)])

def findMazePathTest():
	maze = [[True, True, True, True], [True, True, True, True], [True, True, True, True], [True,True,True,True]]
	
	clear()
	print("Expecting not None: ", findMazePath(maze))
	
def findMazePathTest2():
	maze = [[True, True, True, True], [False, False, False, False], [True, True, True, True], [True,True,True,True]]
	
	clear()
	print("Expecting None: ", findMazePath(maze))

findMazePathTest()
findMazePathTest2()

"""
18.2 paint a boolean matyrix

its like a mspaint fill
if there exists a path from start to node x (path exists if they share the same color), then flip the color

O(R) runtime (size of of region is R)
"""

def paint(matrix, start):
	initColor = matrix[start[0]][start[1]]
	
	def traverse(cur):
		row = cur[0]
		col = cur[1]
		if matrix[row][col] != initColor:
			return
		
		matrix[row][col] = not initColor
		
		# now traverse
		if row > 0 and matrix[row - 1][col] == initColor:
			traverse((row - 1, col))
		if row < len(matrix) - 1 and matrix[row + 1][col] == initColor:
			traverse((row + 1, col))
		if col > 0 and matrix[row][col - 1] == initColor:
			traverse((row, col - 1))
		if col < len(matrix[row]) - 1 and matrix[row][col + 1] == initColor:
			traverse((row, col + 1))
	
	traverse(start)
	return matrix

def paintTest():
	matrix = [[True, True, True, True], [True, True, True, True], [True, True, True, True], [True,True,True,True]]
	
	print("expecting all False: ", paint(matrix, (0, 0)))
	
def paintTest2():
	matrix = [[True, True, True, True], [True, True, False, False], [False, False, True, True], [True,True,True,True]]
	
	print("expecting all True except third row with two Falses: ", paint(matrix, (1, 3)))

paintTest()
paintTest2()

"""
18.3
compute enclosed regions

replace all white enclosed regions with black (enclosed means cannot reach the edge)

wrong:
perform a dfs, if this node or any of its children can reach the boundary return true, else set to black and return false


correct:
compute the inverse of the answer by traversing from edges inwards, marking them as Traversed

all traversed nodes are set to W, else B
"""

# def computeEnclosedRegions(grid):
	# def isNotEnclosed(coordinate):
		# return coordinate[0] == 0 or coordinate[0] == len(grid) - 1 or coordinate[1] == 0 or coordinate[1] == len(grid[coordinate[0]]) - 1
	# def traverseNeighbors(coordinate):
		# if coordinate in traversed or grid[coordinate[0]][coordinate[1]] == 'B':
			# return False
		# if isNotEnclosed(coordinate):
			# return True
		
		# ans = set()
		# traversed.add(coordinate)
		
		# #traverse neighbors
		# if coordinate[0] > 0:
			# new = coordinate
			# new[0] -= 1
			# ans.add(traverseNeighbors(new))
		# if coordinate[0] < len(grid):
			# new = coordinate
			# new[0] += 1
			# ans.add(traverseNeighbors(new))
		# if coordinate[1] > 0:
			# new = coordinate
			# new[1] -= 1
			# ans.add(traverseNeighbors(new))
		# if coordinate[1] < len(grid[coordinate[0]]):
			# new = coordinate
			# new[1] += 1
			# ans.add(traverseNeighbors(new))
		
		# # set to black if enclosed
		# if True not in ans:
			# grid[coordinate[0]][coordinate[1]] = 'B'
			
		# return True in ans
	
	# traversed = {}
	
	# for i in range(len(grid)):
		# for j in range(len(grid[i])):
			# cur = ((i, j), grid[i][j])
			
			# if cur[1] == 'W' and cur[0] not in traversed:
				# traversed[cur[0]] = False
				
				# if isNotEnclosed(cur[0]):
					# traversed[cur[0]] = True
					# continue
				
				# # check children IF IT IS ENCLOSED
				# traverseNeighbors(cur[0])
	
	# return grid

def computeEnclosedRegions(grid):
	n = len(grid)
	m = len(grid[0])
	
	#queue of edge nodes
	q = deque([(i, j) for k in range(0, m) for i, j in ((k, 0), (k, m - 1))] + [(i, j) for k in range(0, n) for i, j in ((0, k), (n - 1, k))])
	
	while q:
		cur = q.popleft()
		row, col = cur[0], cur[1]
		if 0 <= row <= n - 1 and 0 <= col <= m - 1 and grid[row][col] == 'W':
			# mark as traversing
			grid[row][col] = 'T'
			
			q.extend([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
	
	grid[:] = [['B' if c != 'T' else 'W' for c in r] for r in grid]


	
def computeEnclosedRegionsTest():
	grid = [['W', 'W', 'B', 'B'],['B', 'W', 'B', 'B'],['B', 'B', 'W', 'B'],['B', 'B', 'B', 'W']]
	clear()
	print(grid)
	computeEnclosedRegions(grid)
	print(grid)
				
computeEnclosedRegionsTest()

"""
18.4 deadlock detection

check if a DAG contains a cycle

We can use the white, grey, black method to find cycles

All nodes start out as white, as nodes are traversed they are marked as grey. If the traversed node's children are all traversed, the node is marked as black.

If we ever see a grey node while traversing, we know there is a back edge, so a cycle exists.

runtime: O(E)
mem: O(1) (or n if you count marking the nodes as w, g, b)
"""

class CycleNode:
	def __init__(self, val, color, children):
		self.val = val
		self.color = color
		self.children = children
	
def detectCycle(start):
	def traverse(cur):
		# found cycle
		if cur.color == 'G' or cur.color == 'B':
			return True
		
		cur.color = 'G'
		
		# check children for cycles
		for child in cur.children:
			hasCycle = traverse(child)
			if hasCycle:
				return True
		
		cur.color = 'B'
		return False
	
	return traverse(start)

def detectCycleTest():
	start = CycleNode(0, 'W', [])
	node1 = CycleNode(1, 'W', [])
	node2 = CycleNode(2, 'W', [])
	node3 = CycleNode(3, 'W', [])
	node4 = CycleNode(4, 'W', [])
	node5 = CycleNode(5, 'W', [])
	node6 = CycleNode(6, 'W', [])
	node7 = CycleNode(7, 'W', [])
	node8 = CycleNode(8, 'W', [])
	
	start.children.append(node1)
	start.children.append(node2)
	node1.children.append(node3)
	node1.children.append(node4)
	node2.children.append(node5)
	node2.children.append(node6)
	node3.children.append(node7)
	node6.children.append(node8)
	node8.children.append(node2)
	
	clear()
	print("Expecting True, ", detectCycle(start))

def detectCycleTest2():
	start = CycleNode(0, 'W', [])
	node1 = CycleNode(1, 'W', [])
	node2 = CycleNode(2, 'W', [])
	node3 = CycleNode(3, 'W', [])
	node4 = CycleNode(4, 'W', [])
	node5 = CycleNode(5, 'W', [])
	node6 = CycleNode(6, 'W', [])
	node7 = CycleNode(7, 'W', [])
	node8 = CycleNode(8, 'W', [])
	
	start.children.append(node1)
	start.children.append(node2)
	node1.children.append(node3)
	node1.children.append(node4)
	node2.children.append(node5)
	node2.children.append(node6)
	node3.children.append(node7)
	node6.children.append(node8)
	
	clear()
	print("Expecting False, ", detectCycle(start))

detectCycleTest()
detectCycleTest2()

"""
18.5 Clone a directed graph

brute force:
we can use a hash table, mapping old nodes to new nodes while we traverse the graph
this will ensure that we dont loop on cyclic dags infinitely

O(N) runtime
O(N) space
"""

def bruteClone(start):
	class Node:
		def __init__(self, val, neighbors):
			self.val = val
			self.neighbors = neighbors
			
	oldNewMap = {}
	
	def copy(cur):
		if cur in oldNewMap:
			return oldNewMap[cur]
		
		newNode = Node(cur.val, [])
		oldNewMap[cur] = newNode
		
		for neighbor in cur.neighbors:
			newNeighbor = copy(neighbor)
			newNode.neighbors.append(newNeighbor)
		
		return cur
	
	return copy(start)

def BfsClone(start):
	class Node:
		def __init__(self, val, neighbors):
			self.val = val
			self.neighbors = neighbors
			
	oldNewMap = {start: Node(start.val, [])}
	
	q = deque()
	q.append(start)
	
	while q:
		cur = q.popleft()
		
		for neighbor in cur.neighbors:
			q.append(neighbor)
			
			if neighbor not in oldNewMap:
				oldNewMap[neighbor] = Node(neighbor.val, [])
			oldNewMap[cur].neighbors.append(oldNewMap[neighbor])
	
	return oldNewMap[start]


"""
18.7

transform one string to another

given s, t, and a dictionary D
where s PRODUCES t means that there is an array of one character changes leading from s to t

ex:
D = {cat, cot, bat, bot, dog, dot}
s = cat
t = dog

solution = [cat, cot, dot, dog]

solution:
we can create a undirected graph where vertices are the words in the dictionary, and edges are words that are one character away

if we can traverse from s to t, then a solution exists, equal to the traversal path. 
"""

def transformString(D, s, t):
	class Node:
		def __init__(self, val, neighbors):
			self.val = val
			self.neighbors = neighbors
	
	# the problem text says we can assume that strings are the same length
	def isOneCharAway(key, k):
		# if abs(len(key) - len(k)) > 1:
			# # never true
			# return False
		# elif abs(len(key) - len(k)) > 0:
			# # should be all the same except the extra character
			# minLen = min(len(key), len(k))
			
			# for i in range(minLen):
				# if key[i] != k[i]:
					# return False
			
			# return True
		# else:
		#should have exactly one difference
		seenDiff = False
		for i in range(len(key)):
			if key[i] != k[i]:
				if seenDiff:
					return False
				else:
					seenDiff = True
		
		# covers case where they are the same
		return seenDiff
	
	def buildGraph(D):
		stringNodeMap = {}
		
		for key in D:
			if key not in stringNodeMap:
				stringNodeMap[key] = Node(key, [])
			
			for k in D:
				if k not in stringNodeMap:
					stringNodeMap[k] = Node(k, [])
				if isOneCharAway(key, k):
					stringNodeMap[key].neighbors.append(stringNodeMap[k])
		
		return stringNodeMap
	
	traversed = set()
	def traverse(cur, path):
		if cur in traversed:
			return False, None
		
		traversed.add(cur)
		path.append(cur.val)
		if cur.val == t:
			return True, path
		
		for neighbor in cur.neighbors:
			res = traverse(neighbor, path)
			if res[0]:
				return res
		
		return False, None
	
	stringNodeMap = buildGraph(D)
	res = traverse(stringNodeMap[s], [])
	
	return res[1]

def transformString2(D, s, t):
	StringWithDistance = namedtuple('StringWithDistance', ('candidate_string', 'distance'))
	q = deque([StringWithDistance(s, 0)])
	
	traversed = {}
	while q:
		cur = q.popleft()
		
		if cur.candidate_string == t:
			return cur.distance
		
		traversed.append(cur.candidate_string)
		
		for str in D:
			if str not in traversed:
				continue
			seenDiff = False
			for i in range(len(s)):
				if cur[i] != str[i]:
					if seenDiff:
						continue
				if seenDiff:
					q.append(StringWithDistance(str, cur.distance + 1))

def transformString3(D, s, t):
	StringWithDistance = namedtuple('StringWithDistance', ('candidate_string', 'distance'))
	q = deque([StringWithDistance(s, 0)])
	
	while q:
		cur = q.popleft()
		
		if cur.candidate_string == t:
			return cur.distance
		
		for i in len(cur.candidate_string):
			for c in string.ascii_lowercase:
				cand = cur.candidate_string[:i] + c + cur.candidate_string[i+1:]
				
				if cand in D:
					q.append(StringWithDistance(cand, cur.distance + 1))
	
	return -1

def transformStringTest():
	s = "cat"
	t = "dog"
	D = {"cat", "pog", "dat", "dog", "log", "dot"}
	
	clear()
	print(transformString(D, s, t))

transformStringTest()