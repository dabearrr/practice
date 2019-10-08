from collections import deque
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
Chapter 9

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

def lcaTest():
	root = TreeNodeParent(0)
	nodeA = TreeNodeParent(2, TreeNode(1), TreeNode(3), root)
	nodeB = TreeNodeParent(6, TreeNode(5), TreeNode(7), root)
	
	clear()
	print("Should return 0 (a node) ", lcaParent(nodeA, nodeB).val)

def lcaTest2():
	root = TreeNodeParent(0)
	root2 = TreeNodeParent(1)
	nodeA = TreeNodeParent(5, None, None, root)
	nodeB = TreeNodeParent(7, None, None, root2)
	
	clear()
	print("Should return None ", lcaParent(nodeA, nodeB))
	
lcaTest()
lcaTest2()