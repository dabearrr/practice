"""
EPI
Chapter 15, Recursion

1 2 3 4 6 9 10
"""

import collections
import math
import random
import heapq
import bisect 
import operator
import functools
import copy
import timeit

def clear():
	print("-----------------------")
	
"""
sample
gcd 20, 5

= gcd(15, 5)
= gcd(10, 5)
= gcd(5, 5)

gcd 18, 3
15 3
12 3
9 3
6 3
3 3
"""
def gcd(y, x):
	if y == 0:
		return x
	return gcd(y % x, x)

"""
13.1 Tower of hanoi
input: 3 pegs (p1 full, sorted) 
output: 3 pegs (p2 full, sorted)

move rings from peg1 to peg2

a larger ring cannot be placed on top of a smaller ring.

sample 3:
p1
1 2 3
p2
x
p3

step1:
p1
2 3
p2
1
p3
x

step2:
p1
3
p2
2
p3
1

step3:
p1
3
p2
x
p3
1 2

step3:
p1
x
p2
3
p3
1 2

step4:
p1
1
p2
3
p3
2

step5:
p1
1
p2
2 3
p3
x

step6:
p1
x
p2
1 2 3
p3
x

sample 2:
p1
1 2
p2
x
p3
x
step1:
p1
2
p2
x
p3
1

step2:
p1
x
p2
2
p3
1

step3:
p1
x
p2
1 2
p3
x


class Peg
vars
stack

methods
push (throws if top is lower)
pop
top

algorithm:
move n - 1 rings to one peg
move ring n to the target peg
move n - 2 rings to one peg
move ring n - 1 to target peg 
"""

def hanoi(num_rings):
	NUM_PEGS = 3
	def hanoi_steps(num_rings_to_move, from_peg, to_peg, use_peg):
		if num_rings_to_move > 0:
			hanoi_steps(num_rings_to_move - 1, from_peg, use_peg, to_peg)
			pegs[to_peg].append(pegs[from_peg].pop())
			result.append([from_peg, to_peg])
			hanoi_steps(num_rings_to_move - 1, use_peg, to_peg, from_peg)
	
	result = []
	pegs = [list(reversed(range(1, num_rings + 1)))] + [[] for _ in range(1, NUM_PEGS)]
	hanoi_steps(num_rings, 0, 1, 2)
	
	return result

def hanoiTest():
	clear()
	print(hanoi(3))
	
hanoiTest()


"""
15.2 N-Queens

input: N (int)
output: all valid board states with n queens on n x n board

we need to recognize this as a "backtracking" problem

means we have to traverse through LEGAL gamestates like a tree: 
backtracking if the gamestate hits a bad state (no legal moves before solution is found) 
or if solution is found we save and backtrack
"""

def n_queens(n):
	class Board:
		def __init__(self, n):
			self.board = [["." for x in range(n)] for x in range(n)]
		def validate_placement(self, row, col):
			for curCol in range(col):
				if self.board[row][curCol] == 'Q':
					return False
			for curRow in range(row - 1, -1, -1):
				if self.board[curRow][col] == 'Q':
					return False
				if col - (row - curRow) >= 0 and self.board[curRow][col - (row - curRow)] == 'Q':
					return False
				if col + (row - curRow) < len(self.board) and self.board[curRow][col + (row - curRow)] == 'Q':
					return False
			return True
		def place_queen(self, row, col):
			self.board[row][col] = "Q"
		def remove_queen(self, row, col):
			self.board[row][col] = "."
		def visualize(self):
			output = ""
			for row in range(len(self.board)):
				for col in range(len(self.board)):
					output += self.board[row][col] + ' '
				output += '\n'
			
			return output
	
	def dfs(row):
		if row == n:
			# end state reached
			output.append(board.visualize())
			return
		
		for col in range(n):
			if board.validate_placement(row, col):
				board.place_queen(row, col)
				dfs(row + 1)
				board.remove_queen(row, col)
	output = []
	board = Board(n)
	dfs(0)
	
	return '\n'.join(output)

def n_queens_test():
	clear()
	
	print(n_queens(4))
	
n_queens_test()

"""
15.3 generate permutations

pick a number
[1 2 3]

1
[2 3]

1 2
[3]

1 3
[2]

1 2 3
1 3 2

2
[1 3]

2 1
[3]

2 3
[1]

2 1 3
2 3 1

3
[1 2]

3 1
[2]

3 2
[1]

3 1 2

3 2 1

algorithm:
pick a number
remove that number from the pool and add to result
repeat until pool is empty

do this for each number in the pool

"""

"""
simple implementation

issues:
lots of array slicing and copies of the same data.
there should be a way to reduce all the copies of the same data
"""
def generate_permutations(P):
	permutations = []
	def helper(cur_picks, pool):
		if not pool:
			permutations.append(cur_picks)
			return
		
		for i in range(len(pool)):
			helper(cur_picks + [pool[i]], pool[:i] + pool[i + 1:])
	
	helper([], P)
	return permutations
	
"""
assuming distinct entries, we can use a set for the pool
"""
def generate_permutations_2(P):
	permutations = []
	def helper(cur_picks, pool):
		if not pool:
			permutations.append(copy.deepcopy(cur_picks))
			return
		
		for item in pool:
			# we can use the same array / set, we just perform addition / subtraction operations around the recursive call
			cur_picks.append(item)
			pool.remove(item)
			
			helper(cur_picks, pool)
			
			pool.add(item)
			cur_picks.pop()
	
	helper([], set(P))
	return permutations
	
"""
we dont need to generate the power set for this.

swapping intellignetly cant get us there
"""
def generate_permutations_3(P):
	def helper(i):
		if i == len(P) - 1:
			permutations.append(P.copy())
			return
		
		for j in range(i, len(P)):
			P[i], P[j] = P[j], P[i]
			helper(i + 1)
			P[i], P[j] = P[j], P[i]
			
	permutations = []
	helper(0)
	return permutations

def generate_permutations_test():
	clear()
	print("Expecting 6 different permutations", generate_permutations([1, 2, 3]))
	print("Expecting 6 different permutations", generate_permutations_2([1, 2, 3]))
	print("Expecting 6 different permutations", generate_permutations_3([1, 2, 3]))
	
generate_permutations_test()


"""
15.4 Generate the Power set

the power set of S is the set of all subsets of S.

input: set S
output: array of sets of all of the subsets of S

[1 2 3]

we can pick a number

1
[2 3]

now pick another
1 2
[3]

now pick another

1 2 3
[]

branch
1 3
[2]

1 3 2

algorithm:
pick a number from the set, then remove it from the set
repeat until the set is empty

perform all possible picks to get the power set

problem:
this gives permutations

quick fix:
result is a set

bad:
wasted work during generation, same combination of numbers in different permutations will be made

consider a reverse algorithm:

we have 1 2 3

let's remove items

1 2 3

try removing each one
r3
1 2

r2
1 3

r1
2 3

r3r2
1

r2r1
3

r1r2
3

still repeated work

unless!!

we check if we have already reached a branch at every step ex:

r2r1 occurs first
state : [3]
then r1r2 occurs
state : [3]

if state in result already, stop this branch and return -- stops all repeated work.
"""

def power_set(S):
	def helper(curSet, pool):
		immutable_set_copy = frozenset(curSet)
		# prevents duplicate work, however, takes same time to create it -- so not a good solution for it here
		if immutable_set_copy in result:
			return
			
		result.add(immutable_set_copy)
		for item in pool:
			curSet.add(item)
			pool.remove(item)
			
			helper(curSet, pool)
			
			curSet.remove(item)
			pool.add(item)
			
	result = set()
	helper(set(), S)
	
	return result
	
def power_set_2(S):
	def directed_power_set(pool, current):
		if pool == len(S):
			result.append(list(current))
			return
		
		directed_power_set(pool + 1, current)
		
		directed_power_set(pool + 1, current + [S[pool]])
		
	result = []
	directed_power_set(0, [])
	
	return result
	
def power_set_3(S):
	result = []
	
	for int_for_subset in range(1 << len(S)):
		bit_array = int_for_subset
		subset = []
		
		while bit_array:
			subset.append(int(math.log2(bit_array & ~(bit_array - 1))))
			bit_array &= bit_array - 1
		
		result.append(subset)
	
	return result
	
def power_set_test():
	clear()
	
	print("Expecting [], [1], [2], [3], [1 2], [1 3], [2, 3], [1 2 3] : ", power_set(set([1, 2, 3])))
	print("Expecting [], [1], [2], [3], [1 2], [1 3], [2, 3], [1 2 3] : ", power_set_2([1, 2, 3]))
	print("Expecting [], [1], [2], [3], [1 2], [1 3], [2, 3], [1 2 3] : ", power_set_3([1, 2, 3]))

power_set_test()

"""
15.6 Generate strings of matched parens

input: n (count of matched parens)
output: all strings of n matched parens 

0
""

1
"()"

2
"()()", "(())"

3
"()()()", "((()))", "(())()", "()(())", "(()())"

"""

"""
doesnt actually work

it cannot generate two nested sets. (()) (())

wasteful, generates the same one multiple times

can save the traced paths to save some time?
costs a lot of mem if we save every path to a set.

last time with pwer sets, we mapped our vector space to a integer's bits
"""
def generate_parens(n):
	def helper(cur, count):
		if count == 0:
			result.add(cur)
			return
		
		
		helper("({})".format(cur), count - 1)
		helper("(){}".format(cur), count - 1)
		helper("{}()".format(cur), count - 1)
	
	result = set()
	helper("", n)
	
	return result
	

def generate_parens_2(n):
	def helper(cur, count):
		if count == 0:
			return cur
		
		for newCur in ["({})".format(cur), "(){}".format(cur), "{}()".format(cur)]:
			for i in range(1, count - 1):
				helper(newCur, i) + helper(newCur, count - i)
	
	result = set()
	helper("", n)
	
	return result
	
# same as 1
"""
can we look back?
2 = 1 + 1
3 = 2 + 1
4 = 2 + 2 or 3 + 1
5 = 41 23
6 = 222 33 51 42 111111
"""
def generate_parens_3(n):
	result = [set() for x in range(n + 1)]
	
	result[0].add("")
	
	for i in range(n):
		for item in result[i]:
			result[i+1].add("({})".format(item))
			result[i+1].add("(){}".format(item))
			result[i+1].add("{}()".format(item))
	
	return result[n]
	
"""
Should have considered the fact that we don't always need to add them at the same time.
"""
def generate_parens_4(n):
	def helper(left_needed, right_needed, validPrefix):
		if left_needed > 0:
			helper(left_needed - 1, right_needed, validPrefix + "(")
		if left_needed < right_needed and right_needed > 0:
			helper(left_needed, right_needed - 1, validPrefix + ")")
		
		if not right_needed:
			result.append(validPrefix)
	
	result = []
	helper(n, n, "")
	return result

def generate_parensTest():
	clear()
	print(generate_parens(0))
	print(generate_parens(1))
	print(generate_parens(2))
	print(generate_parens(3))
	print(generate_parens(4))
	clear()
	print(generate_parens_4(0))
	print(generate_parens_4(1))
	print(generate_parens_4(2))
	print(generate_parens_4(3))
	print(generate_parens_4(4))
	
	if '(())(())' not in generate_parens_4(4):
		print("doesnt work")
	
generate_parensTest()
"""
15.9 Sudoku solver
sudoku solution:
all rows, all columns, and all 3x3 sections of the board have unique digits in [1, 9]

we can try a backtracking style solution, trying all possible steps in a dfs manner, until we reach an end state (invalid state or solution state)

sol = None
dfs():
	if board reached complete state:
		sol = board state
	
	for move in possible moves:
		if isLegalMove(move):
			perform move
			dfs() // progress
			undo move
	
dfs (row, col):
	if row == maxRow and col > maxCol or col == maxCol and row > maxRow:
		// solution found
		sol = board state
	elif row > maxRow or col > maxCol:
		return
	elif board.at(row, col) != 0:
			dfs(row + 1, col)
			dfs(row, col + 1)
	
	for i in range(0, 10):
		if isLegalMove(row, col, i):
			executeMove(row, col, i)
			dfs(row + 1, col)
			dfs(row, col + 1)
			undoMove(row, col)
			
		
"""

def sudokuSolver(initial_state):
	Section = collections.namedtuple('Section', ['row', 'col'])
	class Board:
		def __init__(self, initial_state):
			self.board = initial_state
		
		def isEmptySpace(self, row, col):
			return self.board[row][col] == 0
		
		def _findSectionHelper(self, index):
			if index < 3:
				return 0
			elif index > 5:
				return 2
			else:
				return 1
				
		def _findSection(self, row, col):
			return Section(self._findSectionHelper(row), self._findSectionHelper(col))
		
		def _isLegalSection(self, row, col, value):
			section = self._findSection(row, col)
			sectionPos = (section.row * 3, section.col * 3)
			
			for r in range(sectionPos[0], sectionPos[0] + 3):
				for c in range(sectionPos[1], sectionPos[1] + 3):
					if self.board[r][c] == value:
						return False
			
			return True
		
		def isLegalMove(self, row, col, value):
			if value in self.board[row]:
				return False
			
			for i in range(len(self.board)):
				if value == self.board[i][col]:
					return False
					
			return self._isLegalSection(row, col, value)
		
		def setValue(self, row, col, value):
			self.board[row][col] = value
			
		def getState(self):
			return copy.deepcopy(self.board)
		
		def visualize(self):
			output = ""
			for row in range(len(self.board)):
				for col in range(len(self.board)):
					output += str(self.board[row][col]) + ' '
				output += '\n'
			
			return output 
	"""
	def dfs(row, col):
		print(row, col)
		if row == 0 and col > 8 :
			# solution found
			sol = board.getState()
			return
		elif row > 8 or col > 8:
			return
		elif not board.isEmptySpace(row, col):
			dfs(row + 1, col)
			dfs(row, col + 1)
			return
		
		for i in range(1, 10):
			if board.isLegalMove(row, col, i):
				board.setValue(row, col, i)
				dfs(row + 1, col)
				dfs(row, col + 1)
				board.setValue(row, col, 0)
	"""
	
	def dfs(pos):
		row = int(pos / 9)
		col = pos % 9
		if pos > 80:
			# solution found
			sol.append(board.visualize())
		elif not board.isEmptySpace(row, col):
			dfs(pos + 1)
		else:
			for i in range(1, 10):
				if board.isLegalMove(row, col, i):
					board.setValue(row, col, i)
					dfs(pos + 1)
					board.setValue(row, col, 0)
	
	
	sol = []
	board = Board(initial_state)
	dfs(0)
	return sol[0]
	
def sudokuSolverTest():
	S = [[5,3,0,0,7,0,0,0,0], [6,0,0,1,9,5,0,0,0], [0,9,8,0,0,0,0,6,0], [8,0,0,0,6,0,0,0,3], [4,0,0,8,0,3,0,0,1], [7,0,0,0,2,0,0,0,6], [0,6,0,0,0,0,2,8,0], [0,0,0,4,1,9,0,0,5], [0,0,0,0,8,0,0,7,9]]
	clear()
	print(sudokuSolver(S))
	
sudokuSolverTest()
"""
15.10 Grey Code computation

an n-bit grey code is a permutation of (0, 1, 2, ..., 2^n-1) s.t. the binary representations of successive integers differ only by 1

1 bit
0 1

2 bit
00 01 11 10

3 bit
000 100 101 111 110 010 011 001

this can be done with backtracking

trying all in set (0 -> 2^n-1)

if legal move (first is always legal)

repeat

trying all in set (0 -> 2^n-1) - first pick

if legal move

repeat
"""

"""
Correct answer, but it does unnecessary work
it computes ALL legal grey codes. If we only want one, we need to terminate quick
"""
def grayCode(n):
	def getPool(n):
		pool = set()
		for i in range(int(math.pow(2, n))):
			pool.add(i)
		
		return pool
	
	def differsByOneBit(a, b):
		MASK = 1
		seenDiff = False
		
		while a or b:
			if a & MASK != b & MASK:
				if seenDiff:
					return False
				seenDiff = True
			a >>= 1
			b >>= 1
		
		return seenDiff
	
	def isLegalMove(item, cur):
		if not cur:
			return True
		
		return differsByOneBit(item, cur[-1])
	
	def dfs(pool):
		count[0] += 1
		if not pool:
			result[0] = copy.deepcopy(cur)
			return
		
		for item in pool:
			if isLegalMove(item, cur):
				cur.append(item)
				pool.remove(item)
				
				dfs(pool)
				
				cur.pop()
				pool.add(item)
				
	
	count = [0]
	result = [None]
	cur = []
	dfs(getPool(n))
	
	print(count[0], " calls to dfs")
	return result[0]


"""
stops after 1st sol!!

:)

we can improve though. On each legal move search we search all items in the pool 0 - 2^n

if this pool is greater than n,
it is faster to just check items with one bit flipped from the last pick (n candidates)
"""
def grayCode2(n):
	def getPool(n):
		pool = set()
		for i in range(int(math.pow(2, n))):
			pool.add(i)
		
		return pool
	
	def differsByOneBit(a, b):
		MASK = 1
		seenDiff = False
		
		while a or b:
			if a & MASK != b & MASK:
				if seenDiff:
					return False
				seenDiff = True
			a >>= 1
			b >>= 1
		
		return seenDiff
	
	def isLegalMove(item, cur):
		if not cur:
			return True
		
		return differsByOneBit(item, cur[-1])
	
	def dfs(pool):
		count[0] += 1
		# solution already found
		if result[0]:
			return
		# solution just found
		if not pool:
			result[0] = copy.deepcopy(cur)
			return
		
		for item in pool:
			if isLegalMove(item, cur):
				cur.append(item)
				pool.remove(item)
				
				dfs(pool)
				
				cur.pop()
				pool.add(item)
		
		return
				
			
	count = [0]
	result = [None]
	cur = []
	dfs(getPool(n))
	
	print(count[0], " calls to dfs")
	return result[0]
	
def grayCode3(n):
	def getPool(n):
		pool = set()
		for i in range(int(math.pow(2, n))):
			pool.add(i)
		
		return pool
	
	def differsByOneBit(a, b):
		MASK = 1
		seenDiff = False
		
		while a or b:
			if a & MASK != b & MASK:
				if seenDiff:
					return False
				seenDiff = True
			a >>= 1
			b >>= 1
		
		return seenDiff
	
	def isLegalMove(item, cur):
		if not cur:
			return True
		
		return differsByOneBit(item, cur[-1])
	
	def executeMove(item, pool):
		cur.append(item)
		pool.remove(item)
		
		dfs(pool)
		
		cur.pop()
		pool.add(item)
		
	def flipIthBit(num, i):
		MASK = 1 << i
		
		# bit is 1, so flip to 0
		if num & MASK:
			return num & ~MASK
		else:
			# flip bit from 1 to 0
			return num | MASK
		
	
	def dfs(pool):
		count[0] += 1
		# solution already found
		if result[0]:
			return
		# solution just found
		if not pool:
			result[0] = copy.deepcopy(cur)
			return
		
		
		if len(pool) < n or not cur:
			for candidate in pool:
				if isLegalMove(candidate, cur):
					executeMove(candidate, pool)
					
		else:
			for i in range(n):
				candidate = flipIthBit(cur[-1], i)
				if candidate in pool:
					executeMove(candidate, pool)
		
	count = [0]
	result = [None]
	cur = []
	dfs(getPool(n))
	
	print(count[0], " calls to dfs")			
	return result[0]

"""
no pool implementation
"""
def grayCode4(n):
	def executeMove(item):
		cur.append(item)
		dfs()
		cur.pop()
		
	def flipIthBit(num, i):
		MASK = 1 << i
		
		# bit is 1, so flip to 0
		if num & MASK:
			return num & ~MASK
		else:
			# flip bit from 1 to 0
			return num | MASK
		
	
	def dfs():
		count[0] += 1
		# solution already found
		if result[0]:
			return
			
		# solution just found
		if len(cur) == math.pow(2, n):
			result[0] = copy.deepcopy(cur)
			return
		
		for i in range(n):
			candidate = None
			if cur:
				candidate = flipIthBit(cur[-1], i)
			else:
				candidate = flipIthBit(0, i)
			
			# can optimize here with a set, ordered dict can be used to keep order
			if candidate not in cur:
				executeMove(candidate)
		
	count = [0]
	result = [None]
	cur = []
	dfs()
	
	print(count[0], " calls to dfs")			
	return result[0]
	
def grayCode5(num_bits):
	if num_bits == 0:
		return [0]
	
	gray_code_num_bits_minus_1 = grayCode5(num_bits - 1)
	
	leading_bit_one = 1 << (num_bits - 1)
	
	return gray_code_num_bits_minus_1 + [
		leading_bit_one | i for i in reversed(gray_code_num_bits_minus_1)
	]

def grayCodeTest():
	clear()
	# print(grayCode(5))
	clear()
	print(grayCode2(5))
	clear()
	print(grayCode3(5))
	clear()
	print(grayCode4(5))
	clear()
	print(grayCode5(5))
	
grayCodeTest()