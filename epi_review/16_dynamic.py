"""
EPI Chapter 14 Review

Dynamic Programming
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
import itertools


def clear():
	print("-----------------------")

"""
samples
"""	
def fib(n):
	if n < 2:
		return n
	
	prev_2 , prev_1, cur = 0, 1, 1
	n -= 2
	while n > 0:
		prev_2 = prev_1
		prev_1 = cur
		cur = prev_1 + prev_2
		n -= 1
	
	return cur

"""
more beautifully
"""
def fib_2(n):
	if n <= 1:
		return n
	
	f_minus_2, f_minus_1 = 0, 1
	
	for _ in range(1, n):
		f = f_minus_2 + f_minus_1
		f_minus_2, f_minus_1 = f_minus_1, f
	
	return f_minus_1

def fib_test():
	clear()
	print(0 == fib(0))
	print(1 == fib(1))
	print(1 == fib(2))
	print(2 == fib(3))
	print(3 == fib(4))
	print(5 == fib(5))
	print(21 == fib(8))
	
fib_test()

def max_subarray_sum(A):
	max_sum, min_sum = A[0], 0
	for running_sum in itertools.accumulate(A):
		print("min sum is {}, max sum is {}, running sum is {}".format(min_sum, max_sum, running_sum))
		max_sum = max(max_sum, running_sum - min_sum)
		min_sum = min(min_sum, running_sum)
	
	print("min sum is {}, max sum is {}, running sum is {}".format(min_sum, max_sum, running_sum))
	return max_sum

def max_subarray_sum_test():
	A = [904, 40, 523, 12, -335, -385, -124, 481, -31]
	B = [-335, -385, -124, -31]
	
	clear()
	print(max_subarray_sum(A) == 956 + 523)
	print(max_subarray_sum(B) == -31)

max_subarray_sum_test()


"""
16. 1 score combinations

considered a lookback alg, was insufficient
(2 = 1, 3 = 1, 7 = 1, each number check num - 3, -2, -7)

now trying knapsack

consider choosing only 2
then 2 & 3 
then 2 & 3 & 7
	0	1	2	3	4	5	6	7	8	9	10	11	12
0	0	0	0	0	0	0	0	0	0	0	0	0	0
2	0	0	1	0	1	0	1	0	1	0	1	0	1
3	0	0	1	1	1	1	2	1	2	2	1	2	3
7	0	0	1	1	1	1	2	2	2	3	2	3	4

each space is up + look back (2, 3, or 7) + (1 if target == (2, 3, or 7))


"""

def score_combos(goal_types, score):
	dp_table = [ [1] + [0] * (score)] * (len(goal_types) + 1)
	
	for row in range(1, len(dp_table)):
		for col in range(1, len(dp_table[row])):
			goal_type = goal_types[row - 1]
			res = 0
			
			if col >= goal_type:
				res += dp_table[row][col - goal_type]
			res += dp_table[row - 1][col]
			
			dp_table[row][col] = res
	
	print(dp_table)
	print(len(goal_types))
	print(score)
	return dp_table[len(goal_types)][score]

def score_combos_2(goal_types, score):
	dp_table = [1] + [0] * (score)
	
	for goal_type in goal_types:
		for col in range(1, len(dp_table)):
			if col >= goal_type:
				dp_table[col] += dp_table[col - goal_type]
	
	print(dp_table)
	print(len(goal_types))
	print(score)
	return dp_table[score]

def score_combos_test():
	goal_types = [2, 3, 7]
	
	clear()
	print(score_combos(goal_types, 12) == 4)
	print(score_combos_2(goal_types, 12) == 4)
	
score_combos_test()