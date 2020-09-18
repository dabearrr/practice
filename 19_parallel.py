"""
EPI
Chapter 19, Parallel computing
3 6 8 9 + 20.9
"""

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
19.1 
"""

"""
19.2
"""


"""
19.3 sync two interleaving threads

print evens with one thread and odds with one threads

print nums in order
"""

def printNumbers(limit):
	class Counter:
		def __init__(self, value):
			self.value = value
			self.isEven = not (value & 1 == 1)
			self._lock = threading.Lock()
		def increment(self, threadName):
			with self._lock:
				self.value += 1
				self.isEven = not self.isEven
				print(self.value, threadName)

	def printHelper(counter, isEven, limit):
		while counter.value < limit:
			if counter.isEven == isEven:
				counter.increment('even thread' if isEven else 'odd thread')
	
	counter = Counter(0)
	t1 = threading.Thread(target=printHelper, args=(counter, False, limit))
	t2 = threading.Thread(target=printHelper, args=(counter, True, limit))
	
	t1.start()
	t2.start()
	
	while t1.is_alive() or t2.is_alive():
		time.sleep(0.5)
		print('[',time.ctime(),']', t1.getName(), t1.is_alive())
		print('[',time.ctime(),']', t2.getName(), t2.is_alive())

class OddEvenMonitor(threading.Condition):
	ODD_TURN = True
	EVEN_TURN = False
	
	def __init__(self):
		super().__init__()
		self.turn = self.ODD_TURN
	
	def wait_turn(self, old_turn):
		with self:
			while self.turn != old_turn:
				self.wait()
	
	def toggle_turn(self):
		with self:
			self.turn ^= True
			self.notify()

class OddThread(threading.Thread):
	def __init__(self, monitor):
		super().__init__()
		self.monitor = monitor
	
	def run(self):
		for i in range(1, 101, 2):
			self.monitor.wait_turn(OddEvenMonitor.ODD_TURN)
			print(i)
			self.monitor.toggle_turn()

class EvenThread(threading.Thread):
	def __init__(self, monitor):
		super().__init__()
		self.monitor = monitor
	
	def run(self):
		for i in range(2, 101, 2):
			self.monitor.wait_turn(OddEvenMonitor.EVEN_TURN)
			print(i)
			self.monitor.toggle_turn()

	

def printNumbersTest():
	printNumbers(100)
	
printNumbersTest()

"""
19.6 The readers writers problem

want to control read / write access to an object

states:
when writing:
no other thread may read or write to object

when reading:
other readers may access the object

not reading or writing:
readers or writers may access the object

solution:
have a writer lock
for each reader thread check if writer lock is locked before reading

"""

def readersWriters():
	writerLock = threading.Lock()
	target = [1]
	
	class Reader(threading.Thread):
		def __init__(self, target, lock):
			super().__init__()
			self.target = target
			self.lock = lock
		
		def run(self):
			waitingToRead = True
			while waitingToRead:
				if not self.lock.locked():
					print(self.target)
					waitingToRead = False
	
	class Writer(threading.Thread):
		def __init__(self, target, lock):
			super().__init__()
			self.target = target
			self.lock = lock
		
		def run(self):
			with self.lock:
				self.target.append(self.target[-1] + 1)
	
	Reader(target, writerLock).run()
	Reader(target, writerLock).run()
	Writer(target, writerLock).run()
	Writer(target, writerLock).run()
	Reader(target, writerLock).run()
	Reader(target, writerLock).run()
	Reader(target, writerLock).run()
	Reader(target, writerLock).run()
	Writer(target, writerLock).run()

readersWriters()

"""
16.8 Implement a Timer class

input: list of tasks (runnables to thread)

we want to use two data structures:
a min heaps with key: run time and value: thread to run.

We need a dispatcher thread to check the min heap and run tasks. It sleeps until a new runnable is add to the heap or until the next scheduled time

We need a hash table with thread ids as the keys and entries in the min heap as values.
If we need to cancel a thread, we delete it from the heap.

Add a lock for all ht and heap operations
"""

