from collections import deque
import math

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