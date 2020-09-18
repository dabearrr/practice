
import collections
import math
import random
import heapq
import bisect 
import operator
import functools
import copy
import time
import timeit
import threading

def clear():
	print("-----------------------")
	
"""
find median of 2 sorted arrays
"""
def find_median(nums1, nums2):
	total_len = len(nums1) + len(nums2)
	if total_len % 2 == 0:
		return (
			find_kth(total_len // 2, nums1, nums2) +
			find_kth((total_len // 2) - 1, nums1, nums2)
		) / 2
	
	return find_kth(total_len // 2, nums1, nums2)

"""
find kth largest number of two sorted arrays
"""
def find_kth(k, nums1, nums2):
	print(k, nums1, nums2)
	if not nums1:
		return nums2[k]
	if not nums2:
		return nums1[k]
	
	mid1 = len(nums1) // 2
	mid2 = len(nums2) // 2
	
	# its on the right side
	if k > mid1 + mid2:
		# middle of nums1 greater, get rid of left side nums2
		if nums1[mid1] > nums2[mid2]:
			return find_kth(k - mid2 - 1, nums1, nums2[mid2 + 1:])
		else:
			return find_kth(k - mid1 - 1, nums1[mid1 + 1:], nums2)
	else: # on the left
		if nums1[mid1] < nums2[mid2]:
			return find_kth(k, nums1, nums2[:mid2])
		else:
			return find_kth(k, nums1[:mid1], nums2)

	
def find_median_optimized(nums1, nums2):
	total_len = len(nums1) + len(nums2)
	
	if total_len % 2 == 0:
		return (
			find_kth_optimized(total_len // 2, nums1, 0, len(nums1), nums2, 0, len(nums2)) + 
			find_kth_optimized(total_len // 2 - 1, nums1, 0, len(nums1), nums2, 0, len(nums2))
		) / 2
	
	return find_kth_optimized(total_len // 2, nums1, 0, len(nums1), nums2, 0, len(nums2))
	
def find_kth_optimized(k, nums1, start1, end1, nums2, start2, end2):
	print(k, nums1, start1, end1, nums2, start2, end2)
	if end1 <= start1:
		return nums2[start2 + k]
	elif end2 <= start2:
		return nums1[start1 + k]
	
	mid1 = start1 + (end1 - start1) // 2
	mid2 = start2 + (end2 - start2) // 2
	
	# its on the right
	if k > (mid1 - start1) + (mid2 - start2):
		if nums1[mid1] > nums2[mid2]: # get rid of smallest items, so left of nums2
			return find_kth_optimized(k - (mid2 - start2 + 1), nums1, start1, end1, nums2, mid2 + 1, end2)
		else: # get rid of left side of nums1
			return find_kth_optimized(k - (mid1 - start1 + 1), nums1, mid1 + 1, end1, nums2, start2, end2)
	else: # on the left
		if nums1[mid1] < nums2[mid2]: # get rid of right side of nums2, its too big
			return find_kth_optimized(k, nums1, start1, end1, nums2, start2, mid2)
		else: # get rid of right side of nums1
			return find_kth_optimized(k, nums1, start1, mid1, nums2, start2, end2)
			
			
	
			
def find_kth_test():
	print(find_kth())
	
def find_median_test():
	print(find_median([1, 3], [2]) == 2)
	print(find_median([1, 2], [3, 4]) == 2.5)
	print(find_median([1, 1, 1], [1, 1, 1]) == 1)
	print(find_median([1, 2, 2], [1, 2, 3]) == 2)
	
	clear()
	
	print(find_median_optimized([1, 3], [2]) == 2)
	print(find_median_optimized([1, 2], [3, 4]) == 2.5)
	print(find_median_optimized([1, 1, 1], [1, 1, 1]) == 1)
	print(find_median_optimized([1, 2, 2], [1, 2, 3]) == 2)
	
find_median_test()