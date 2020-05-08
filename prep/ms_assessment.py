import collections
import math
import random
import heapq
import bisect
import operator
import functools
import copy

"""
Test helper functions, used for output formatting
"""
def clear():
	print("-----------------------")


def questionTestPreoutput(questionNumber, additionalText = ""):
	clear()
	print("Question #{} tests: {}".format(questionNumber, additionalText))


"""
Questions w/ tests below
"""


def firstQuestion():
	return 1


def firstQuestionTest():
	questionTestPreoutput(1)
	print(1 == 1)


def secondQuestion():
	return 1


def secondQuestionTest():
	questionTestPreoutput(2)
	print(1 == 1)


def thirdQuestion():
	return 1


def thirdQuestionTest():
	questionTestPreoutput(3)
	print(1 == 1)


"""
Execute tests below
"""
firstQuestionTest()
secondQuestionTest()
thirdQuestionTest()
