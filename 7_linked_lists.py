class Node:
	def __init__(self, val=0, next=None):
		self.val = val
		self.next = next



def clear():
	print("------------------------------------------")

def printLl(A):
	if A is None:
		print("NONE")
	temp = A
	while temp:
		print(temp.val)
		temp = temp.next


"""
CTCI LL questions
remove dups
create set
1 pass
O(n) runtime and spaec

cant use any memory?

O(n^2) run time O(1) space compare each node to every node in front of it
if they are the same, remove the one in front

"""

def removeDups(A):
	seen = set()
	cur = A
	
	prev = None
	while (cur is not None):
		if cur.val in seen:
			# remove cur, need prev
			prev.next = cur.next
		else:
			seen.add(cur.val)
			# this should not happen on remove step, see example 1->1->1
			prev = cur
		cur = cur.next

	return A
	
def removeDupsTest():
	clear()
	head = Node(1, Node(2, Node(2, Node(3))))
	printLl(removeDups(head))
	
def removeDupsTest2():
	clear()
	head = Node(1, Node(1, Node(1, Node(1))))
	printLl(removeDups(head))

def removeDupsTest3():
	clear()
	head = Node(1, Node(1, Node(1, Node(2))))
	printLl(removeDups(head))

removeDupsTest()
removeDupsTest2()
removeDupsTest3()

"""
CTCI
return kth to last

requires at LEAST ONE PASS o(n) to know length

can do it in one pass if we keep a hash table with key index and value Node
O(n) runtime, O(n) space

can do it in two passes with O(1) space O(n) runtime
one pass to get length
second pass to find length - kth node
"""

# assume k >= 0
def kthToLast(A, k):
	# index will start at one here
	index, cur = 0, A
	
	while cur is not None:
		index += 1
		cur = cur.next
	
	#index should be equal to length now that we have reached the end
	length = index
	
	# k is too big
	if k >= length:
		return None
	
	indexToFind = length - k
	index = 0
	cur = A
	while cur is not None:
		index += 1
		if index == indexToFind:
			return cur
		cur = cur.next
	
	# should never be reached, k is checked for size
	return None
	
	#simple
def kthToLastTest():
	clear()
	head = Node(1, Node(2, Node(2, Node(3))))
	printLl(kthToLast(head, 1))
# k too big
def kthToLastTest2():
	clear()
	head = Node(1, Node(2, Node(2, Node(3))))
	printLl(kthToLast(head, 4))

# k is first element
def kthToLastTest3():
	clear()
	head = Node(1, Node(2, Node(2, Node(3))))
	printLl(kthToLast(head, 3))

kthToLastTest()
kthToLastTest2()
kthToLastTest3()

"""
delete middle node
params: node that we want to delete
if we dont have prev, deleting this node is difficult
if we dont care about preserving the original Nodes, we can set cur.val = next.val
then set the last node to None
this is O(N) runtime, O(1) space

If we MUST preserve the Nodes...not sure if this can be done in python
in c++ perhaps we could change the addresses? no we cant
thinking
"""

#assuming non null inputs, only middle nodes
def deleteMiddleNode(A):
	# we know this is not a first node, so we dont have to worry about deleting a first node being impossible without the head ptr
	prev = A
	cur = A.next
	
	while cur is not None and cur.next is not None:
		prev.val = cur.val
		prev = cur
		cur = cur.next
	prev.val = cur.val
	prev.next = None

#simple 1st to start
def deleteMiddleNodeTest():
	clear()
	middle = Node(2, Node(3, Node(4)))
	head = Node(1, middle)
	deleteMiddleNode(middle)
	printLl(head)

# 1st to last, same values
def deleteMiddleNodeTest2():
	clear()
	middle = Node(1, Node(1))
	head = Node(1, middle)
	deleteMiddleNode(middle)
	printLl(head)

deleteMiddleNodeTest()
deleteMiddleNodeTest2()

"""
partition around a value x

list should go

less than x -> more than x

make two dummies

dummy1 will be used to construct the left side

dummy2 will be used to construct the right side

dummy1end -> dummy2start

dummy2end-> None

return dummy1.next

O(n) operation
O(1) space
"""

def partition(A, x):
	dummy1 = Node()
	dummy1Cur = dummy1
	dummy2 = Node()
	dummy2Cur = dummy2
	
	cur = A
	while cur is not None:
		if cur.val < x:
			#left
			dummy1Cur.next = cur
			dummy1Cur = dummy1Cur.next
		else:
			#right
			dummy2Cur.next = cur
			dummy2Cur = dummy2Cur.next
		cur = cur.next
	
	dummy1Cur.next = dummy2.next
	
	#terminate 
	dummy2Cur.next = None
	
	return dummy1.next

# simple
def partitionTest():
	clear()
	head = Node(4, Node(5, Node(1, Node(2, Node(3)))))
	printLl(partition(head, 3))

def partitionTest2():
	clear()
	head = Node(4, Node(5, Node(1, Node(2, Node(3)))))
	printLl(partition(head, 1))
	
def partitionTest3():
	clear()
	head = Node(4, Node(5, Node(1, Node(2, Node(3)))))
	printLl(partition(head, 5))
	
partitionTest()
partitionTest2()
partitionTest3()
			
"""
Sum List
brute force
turn lists into numbers, add them then convert back

doesnt work if they are larger than int max size
O(N) runtime and memory

A 1 2 3 4
B 4 5 6

startdummy ->A.start
add to a
A 5 7 9 4

return start dummy.next

A 1 2 3
B 4 5 6 7

startdummy ->A.start
add to a
A 5 7 9

B is longer, point cur.next to B.next
A 5 7 9 -> 7




"""

def sumLists(A, B):
	if A is None:
		return B
	if B is None:
		return A
		
	startDummy = Node()
	startDummy.next = A
	prev, carry, cur = startDummy, 0, A
	while(cur is not None and B is not None):
		sum = cur.val + B.val + carry
		carry = int(sum / 10)
		cur.val = sum % 10
		B = B.next
		prev = cur
		cur = cur.next
		
	if B is not None:
		prev.next = B
		cur = B
		
	while cur is not None and carry > 0:
		sum = cur.val + carry
		carry = int(sum / 10)
		cur.val = sum % 10
		
	return startDummy.next

#simple
def sumListTest():
	A = Node(1, Node(2, Node(3)))
	B = Node(4, Node(5, Node(6)))
	clear()
	
	printLl(sumLists(A, B))
	
# complex A is bigger
def sumListTest2():
	A = Node(9, Node(9, Node(9, Node(9))))
	B = Node(4, Node(5, Node(6)))
	clear()
	
	printLl(sumLists(A, B))

# complex B is bigger	
def sumListTest3():
	A = Node(9, Node(9, Node(9)))
	B = Node(9, Node(9, Node(9, Node(9))))
	clear()
	
	printLl(sumLists(A, B))

sumListTest()
sumListTest2()
sumListTest3()

"""
brute force
A[0] A[length-1]
A[1] A[length-2]
O(n^2) run O(1) space

use an array to store the values as you traverse
compare the array as normal

noon
noaon
"""
def palindrome(A):
	B = []
	
	cur = A
	while cur is not None:
		B.append(cur.val)
		cur = cur.next
	
	i, j = 0, len(B) - 1
	
	while i < j:
		if B[i] != B[j]:
			return False
		i = i + 1
		j = j - 1
	return True

def palTest():
	clear()
	A = Node("A", Node("D", Node("A")))
	print(palindrome(A))
def palTest2():
	clear()
	A = Node("A", Node("D", Node("D", Node("A"))))
	print(palindrome(A))
def palTest3():
	clear()
	A = Node("A", Node("D", Node("B", Node("A"))))
	print(palindrome(A))
def palTest4():
	clear()
	A = Node("A", Node("D", Node("B")))
	print(palindrome(A))

palTest()
palTest2()
palTest3()
palTest4()

"""
Intersection
O(n^2) runtime O(1) space operation to brute force compare each node
O(n) runtime O(n) space operation to use a hash table
"""

def intersection(A, B):
	setA = set()
	
	cur = A
	while cur is not None:
		setA.add(cur)
		cur = cur.next
	
	cur = B
	while cur is not None:
		# the first match should be the intersection
		if cur in setA:
			return cur
	
	return None

def intersection2(A, B):
	cur = A
	lastA = A
	lengthA = 1
	while cur.next is not None:
		cur = cur.next
		lengthA += 1
	lastA = cur
	
	cur = B
	lastB = B
	lengthB = 1
	while cur.next is not None:
		cur = cur.next
		lengthB += 1
	lastB = cur
	
	if lastA is not lastB:
		return None
	
	#intersection found
	curA = A
	curB = B
	while lengthA != lengthB:
		if lengthA > lengthB:
			curA = curA.next
			lengthA -= 1
		else:
			curB = curB.next
			lengthB -= 1
	
	while curA is not curB:
		curA = curA.next
		curB = curB.next
	
	return curA

def intersectionTest():
	link = Node(1, Node(2, Node(3)))
	A = Node(8, Node(7))
	B = Node(6)
	A.next = link
	B.next = link
	
	clear()
	printLl(intersection2(A, B))

def intersectionTest2():
	link = Node(1, Node(2, Node(3)))
	B = Node(8, Node(7))
	A = Node(6)
	A.next = link
	B.next = link
	
	clear()
	printLl(intersection2(A, B))

def intersectionTest3():
	A = Node(8, Node(7))
	B = Node(6)
	
	clear()
	printLl(intersection2(A, B))
intersectionTest()
intersectionTest2()
intersectionTest3()

"""
loop detection

brute force
make a set as you traverse
if cur node in the set, we are in a loop
O(N) runtime and space

better:
detect if a loop exists by using a fast and slow pointer
if they are ever equal, there is a loop

if a loop exists, find the length of the loop

1-2-3-4-|
  ^-----|

then traverse the list again checking if Node + length is the same
O(N) runtime O(1) space
"""
def loopDetection(A):
	cur, fast = A, A
	hasLoop = False
	while fast is not None and fast.next is not None and fast.next.next is not None:
		cur = cur.next
		fast = fast.next.next
		
		if fast is cur:
			hasLoop = True
			break
	
	if not hasLoop:
		# no loop
		return None
	
	# get length of loop
	length = 1
	fast = cur.next
	while fast is not cur:
		fast = fast.next
		length += 1
	
	# go to start and put fast length nodes forward
	fast, cur = A, A
	for _ in range(length):
		fast = fast.next
	
	# once the first loop node is reached, they are equal
	while cur is not fast:
		cur = cur.next
		fast = fast.next
	
	return cur
	
def loopDetectionTest():
	loop = Node(3, Node(4, Node(5)))
	loop.next.next.next = loop
	start = Node(1, Node(2))
	start.next = loop
	
	#true, 3
	clear()
	print(loopDetection(start).val)

def loopDetectionTest2():
	noloop = Node(1, Node(2, Node(3)))
	
	#None
	clear()
	printLl(loopDetection(noloop))

def loopDetectionTest3():
	loop = Node(1, Node(2, Node(3)))
	loop.next.next.next = loop
	
	#true, 3
	clear()
	print(loopDetection(loop).val)

loopDetectionTest()
loopDetectionTest2()
loopDetectionTest3()

"""
A B cur
2 3 -
5 3 2
5 11 3
7 11 5
None 11 7
None None 11

return ->2
"""
def merge(A, B):
	if not A:
		return B
	elif not B:
		return A
		
	start = cur = Node()
	
	while(A or B):
		if A and (not B or A.val < B.val):
			cur.next = A
			cur = cur.next
			A = A.next
		else:
			cur.next = B
			cur = cur.next
			B = B.next
	
	return start.next
	
A = Node(2, Node(5, Node(7)))
B = Node(3, Node(11))

printLl(A)
printLl(B)
printLl(merge(A, B))

"""
7.2
reverse sublist

L, s, f

reverse LL from node index s to node index f
"""
def reverseSub(L, s, f):
	if L is None:
		return L
	if s >= f:
		return L

	head = L
	beforeRev = None
	startRev = None
	index = 1
	prev = None
	cur = L
	areReversing = False
	while cur is not None and index <= f:
		if index == s:
			areReversing = True
			beforeRev = prev
			startRev = cur
		elif index == f:
			if beforeRev is None:
				# means s == 1
				head = cur
			else:
				beforeRev.next = cur
			startRev.next = cur.next
			cur.next = prev
			break
		if areReversing:
			cur.next, cur, prev = prev, cur.next, cur
		else:
			cur, prev = cur.next, cur
		index += 1
		
	return head

def testReverseSub():
	L = Node(11, Node(3, Node(5, Node(7, Node(2)))))
	s = 2
	f = 4
	clear()
	printLl(reverseSub(L, s, f))

def testReverseSubWithS1():
	L = Node(11, Node(3, Node(5, Node(7, Node(2)))))
	s = 1
	f = 5
	clear()
	printLl(reverseSub(L, s, f))
	
def testReverseSubWithNullHead():
	L = null
	s = 1
	f = 5
	clear()
	printLl(reverseSub(L, s, f))
	
def testReverseSubWithSLarger():
	L = Node(11, Node(3, Node(5, Node(7, Node(2)))))
	s = 6
	f = 1
	clear()
	printLl(reverseSub(L, s, f))
testReverseSub()
testReverseSubWithS1()

"""
7.3 cyclicity
"""

def cycle(A):
	cur = A
	fast = A
	cycleDetected = False
	
	while fast and fast.next and fast.next.next and not cycleDetected:
		if cur is fast:
			cycleDetected = True
		cur = cur.next
		fast = fast.next.next
	
	if not cycleDetected:
		return None
	
	cycleLength = 0
	fast = cur
	while fast is not cur or cycleLength == 0:
		cycleLength += 1
		fast = fast.next
	
	dummy = Node()
	dummy.next = A
	
	fast = None
	cur = dummy
	while fast is not cur:
		cur = cur.next
		fast = cur
		for _ in range(cycleLength):
			fast = fast.next
	
	return cur
	
def cycleTest():
	a = Node(1)
	b = Node(2)
	c = Node(3)
	a.next = b
	b.next = c
	c.next = b
	
	print(cycle(a).val)
	
def cycleTest2():
	a = Node(1, Node(2, Node(3, Node(4, Node(5)))))
	a.next = a
	
	print(cycle(a).val)
cycleTest()
cycleTest2()

"""
7.4
Test for overlapping lists
brute force
O(N) run time and memory -- just use a set IDIOT

check lengths
O(N) 

4 5 6 -|
        7 - 8 - 9 
1 2 3 -|
if the lists are the same length, at some point in normal traversal curA is curB

if the lists are different lengths, we can artifically cut off the extra size from the list
A
   4 5 -|
        6 7 8
 1 2 3 -|
B

take A length and B length
curB is advanced B-A length before normal traversal
return curA when curA is curB
"""
def overlapping(A, B):
	if A is None or B is None:
		return None

	# get lengths and last nodes
	curA = A
	curB = B
	
	lengthA = 1
	while curA.next is not None:
		lengthA += 1
		curA = curA.next
	
	lengthB = 1
	while curB.next is not None:
		lengthB += 1
		curB = curB.next
	
	# if last nodes match then overlap exists
	if curA is not curB:
		# no overlap
		return None
	
	# need to even the lengths to find overlap node
	curA, curB = A, B
	while lengthA != lengthB:
		if lengthA > lengthB:
			lengthA -= 1
			curA = curA.next
		else:
			lengthB -= 1
			curB = curB.next
	
	
	while curA is not curB:
		curA, curB = curA.next, curB.next
	
	return curA

# simple
def overlappingTest():
	A = Node(1, Node(2, Node(3)))
	B = Node(4, Node(5, Node(6)))
	
	overlap = Node(7, Node(8))
	
	A.next.next.next = overlap
	B.next.next.next = overlap
	
	clear()
	printLl(overlapping(A, B))
	
# complex different lengths
def overlappingTest2():
	A = Node(1, Node(2))
	B = Node(3, Node(4, Node(5)))
	
	overlap = Node(6, Node(7))
	
	A.next.next = overlap
	B.next.next.next = overlap
	
	clear()
	printLl(overlapping(A, B))
	
overlappingTest()
overlappingTest2()

"""
7.7
kth to last element

brute force:
pass through once to get length
pass through again to get kth to last node

O(n) runtime O(1) memory, 2 passes

One pass solution:
iterate through the nodes to get the length
while doing this, have a slow iterator to keep the kth to last node saved

return the kth to last node


0 1
1 2

"""
def kToLast(A, k):
	slow = Node()
	slow.next = A
	
	cur, index = slow, 0
	while cur.next is not None:
		if index >= k:
			slow = slow.next
		
		cur = cur.next
		index += 1
	
	# length is too short for k
	if slow.next is A:
		return None
	
	return slow

# simple
def kToLastTest():
	head = Node(1, Node(2, Node(3)))
	k = 2
	
	clear()
	printLl(kToLast(head, k))
	
# k too big
def kToLastTest2():
	head = Node(1, Node(2, Node(3)))
	k = 3
	
	clear()
	printLl(kToLast(head, k))
	
# k = 0
def kToLastTest3():
	head = Node(1, Node(2, Node(3)))
	k = 0
	
	clear()
	printLl(kToLast(head, k))
	
kToLastTest()
kToLastTest2()
kToLastTest3()
"""
7.10
merge even - odd Ll
ex:
0 1 2 3 4
becomes
0 2 4 1 3

Brute force
hash table, point even number to next even number
point odd number to next odd number
last even -> first odd
O(N) runtime O(N) space

better:
O(N) runtime
O(1) space

even ptr
odd ptr

if cur index % 2 == 0:
	even.next = cur
else:
	odd.next = cur

evenEnd.next = oddStart

return evenStart
"""
def evenOdd(A):
	if A is None:
		return A

	evenStart, oddStart = Node(), Node()
	evenStart.next = oddStart.next = cur = A
	even = evenStart
	odd = oddStart
	
	index = 0
	while cur is not None:
		if index % 2 == 0:
			#even
			even.next = cur
			even = even.next
		else:
			#odd
			odd.next = cur
			odd = odd.next
		
		cur = cur.next
		index += 1
	
	# to terminate the separate lists
	even.next = None
	odd.next = None
	
	# this occurs when size > 1, else odds do not exist
	if oddStart is not A:
		#link evens to odds, since oddStart is dummy, return oddStart.next
		even.next = oddStart.next
	
	# even start is a dummy, return evenStart.next
	return evenStart.next

#simple case
def evenOddTest():
	A = Node(0, Node(1, Node(2, Node(3, Node(4)))))
	
	clear()
	printLl(evenOdd(A))

# A is None
def evenOddTest2():
	A = None
	
	clear()
	printLl(evenOdd(A))

# A is size 1
def evenOddTest3():
	A = Node(0)
	
	clear()
	printLl(evenOdd(A))
	
#even size case
def evenOddTest4():
	A = Node(0, Node(1, Node(2, Node(3))))
	
	clear()
	printLl(evenOdd(A))

evenOddTest()
evenOddTest2()
evenOddTest3()
evenOddTest4()
"""
7.11

Palindrome Linked List

brute force can recreate the Linked list in an array
then do the palindrome check normally
O(N) runtime O(N) space

another solution is to do the palindrome comparisons
by traversing to necessary nodes

O(N^2) run time O(1) memory

better:
get length of list
reverse the second half of the list

compare first half to reversed second half!
O(N) runtime O(1) memory

~3 pass
1 pass length
2nd pass reverse second half
3rd pass compare halves
"""

def isPalindrome(A):
	if A is None:
		return True
	
	# get length
	cur, length = A, 1
	while cur.next is not None:
		cur = cur.next
		length += 1
	
	# go to second half
	cur, index = A, 0
	while index < (length + 1) / 2:
		cur = cur.next
		index += 1
	
	
	# start reversing
	prev = None
	while cur is not None:
		# this throws error? what is the difference?
		# cur, prev, cur.next = cur.next, cur, prev
		temp = cur.next
		cur.next = prev
		prev = cur
		cur = temp
	
	# now prev has reversed second half
	secondHalf = prev
	firstHalf = A
	
	# traverse both halves, comparing Ll[n] with Ll[length - 1 - n]
	while secondHalf is not None and firstHalf is not None:
		if firstHalf.val != secondHalf.val:
			return False
		
		firstHalf = firstHalf.next
		secondHalf = secondHalf.next
	
	return True

# even length
def isPalindromeTest():
	A = Node(1, Node(1, Node(1, Node(1))))
	
	clear()
	print(isPalindrome(A))

# odd length
def isPalindromeTest2():
	A = Node(1, Node(2, Node(3, Node(2, Node(1)))))
	
	clear()
	print(isPalindrome(A))

# even not palindromic
def isPalindromeTest3():
	A = Node(1, Node(2, Node(1, Node(1))))
	
	clear()
	print(isPalindrome(A))
	
# odd not palindromic
def isPalindromeTest4():
	A = Node(1, Node(1, Node(2)))
	
	clear()
	print(isPalindrome(A))
	
# None
def isPalindromeTest5():
	A = None
	
	clear()
	print(isPalindrome(A))
	
# Size 1
def isPalindromeTest6():
	A = Node(1)
	
	clear()
	print(isPalindrome(A))
	
isPalindromeTest()
isPalindromeTest2()
isPalindromeTest3()
isPalindromeTest4()
isPalindromeTest5()
isPalindromeTest6()
