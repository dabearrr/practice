#!/usr/bin/env python
import math


def call_all_parities(x):
	print("Calling parities on value: ", x)
	print(parity1(x), parity2(x), parity3(x), parity4(x))
	
	print("parity 5:", parity5(x) )
	
	clear()

def clear():
	print("------------------------------------------------")
	
def count_bits(x):
	num_bits = 0
	while x:
		num_bits += x & 1
		x >>= 1
	
	print(num_bits)
	return num_bits
	

# o(n)
def parity1(x):
	num_one_bits = 0
	while x:
		num_one_bits += x & 1
		x >>= 1
	
	# print(bool(num_one_bits & 1))
	return bool(num_one_bits & 1)

# o(n) with less needed logic, making use of XOR and the binary result
def parity2(x):
	result = 0
	
	while x:
		result ^= x & 1
		x >>= 1
		
	# print(result)
	return result

# o(k) such that k is the number of bits, uses the x & (x-1) trick to remove a one bit
# not is a pitfall, use x = x ^ 1 to flip the bit
def parity3(x):
	result = 0
	
	while x:
		result ^= 1
		x &= (x-1)
	
	# print(result)
	return result

# this would be a hash table with cached values
def PRECOMPUTED_PARITY(x):
	return parity3(x)

# 1 1 1 1
# 1 1 1 0
# 1 0 1 0
# 0 0 0 1
# 0 0 0 0
# O(n/k) where k is the size of the mask used Assuming max integer is 64 bit and k = 16, O(4) - > O(1) Assuming table is initialized as well
def parity4(x):
	# bits for mask
	BITMASK = 16
	mask = int(math.pow(2, BITMASK) - 1)
	
	result = 0
	
	while(x):
		result ^= PRECOMPUTED_PARITY(x & mask)
		
		x >>= 16
	
	# print(result)
	return result

def parity5(x):
	x ^= x >> 32
	print(bin(x))
	x ^= x >> 16
	print(bin(x))
	x ^= x >> 8
	print(bin(x))
	x ^= x >> 4
	print(bin(x))
	x ^= x >> 2
	print(bin(x))
	x ^= x >> 1
	print(bin(x))
	
	return x & 0x1
	
# ( x & ~(x-1) gets the isolated rightmost bit. Using this, we subtract 1 to get the needed right propagation. 
# Then we or this with the original value to get the answer
def right_prop(x):
	if x < 2:
		return x
	return x | (( x & ~(x-1) ) - 1)

def mod_power(x, a):
	if x < 1:
		return 0
	return x & ( (1 << a) - 1 )

# should only have one 1 bit. if x - rightmost bit = 0, it only has one one bit
# assume x > 0
def is_power(x):
	if x < 0:
		return false
	return (x - (x & ~(x-1)) == 0)

#input x: integer
# input i, j: indices 
def swap_bits(x, i, j):
	i_val = (x >> i) & 1
	j_val = (x >> j) & 1
	
	if i_val != j_val:
		if i_val == 1:
			return x & ~(1 << i) | (1 << j)
		else:
			return x & ~(1 << j) | (1 << i)
	
	return x

#input x: integer
# input i, j: indices 
def swap_bits2(x, i, j):
	if (x >> i) & 1 != (x >> j) & 1:
		return x ^ ((1 << i) | (1 << j))
	
	return x
	
call_all_parities(0)
call_all_parities(1)
call_all_parities(6)
call_all_parities(7)
call_all_parities(int(math.pow(2, 16) - 1))
call_all_parities(int(math.pow(2, 64) - 1))

print(mod_power(10, 3))
clear()

print(swap_bits(9, 1, 3))
print(swap_bits(10, 1, 3))
print(swap_bits(5, 1, 3))