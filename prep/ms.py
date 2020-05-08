import collections
import itertools

def threeConsec(S):
	prev, count, moves = None, 0, 0
	for char in S:
		if prev != char:
			prev = char
			count = 1
		else:
			count += 1
			if count == 3:
				moves += 1
				count = 0
	
	return moves


def threeConsec2(S):
	moves = 0
	
	for key, groupIterator in itertools.groupby(S):
		print("This group consists of all " + key + "s")
		currentGroup = list(groupIterator)
		print("This group is of length " + str(len(currentGroup)))
		moves += len(currentGroup) // 3
		print("moves is now {}".format(moves))
	
	return moves
			
def threeConsecTest():
	a = "baaab"
	print(threeConsec(a) == 1)
	
	a = "baaaaab"
	print(threeConsec(a) == 1)
	
	a = "baaaaaaaab"
	print(threeConsec(a) == 2)
	
	a = "baaaaaaaaab"
	print(threeConsec(a) == 3)
	
	a = "baab"
	print(threeConsec(a) == 0)
	
	a = "baabaabbba"
	print(threeConsec(a) == 1)
	
	a = "bbaabbaabbaabbbbbaabbbbbbbaaabaaabbbaaaaaaaaaabbbbbbbbbbb"
	print(threeConsec(a) == 12)

def threeConsec2Test():
	a = "baaab"
	print(threeConsec2(a) == 1)
	
	a = "baaaaab"
	print(threeConsec2(a) == 1)
	
	a = "baaaaaaaab"
	print(threeConsec2(a) == 2)
	
	a = "baaaaaaaaab"
	print(threeConsec2(a) == 3)
	
	a = "baab"
	print(threeConsec2(a) == 0)
	
	a = "baabaabbba"
	print(threeConsec2(a) == 1)
	
	a = "bbaabbaabbaabbbbbaabbbbbbbaaabaaabbbaaaaaaaaaabbbbbbbbbbb"
	print(threeConsec2(a) == 12)
	
threeConsec2Test()


def occursXTimes(A):
	counter = collections.Counter(A)
	
	for key, count in counter.items():
		if key == count:
			return key
	
	return 0

def occursXTimesTest():
	a = [1, 1, 2, 3, 3, 3, 3, 5, 5, 5, 5, 5, 4, 4, 4, 4, 5]
	print(occursXTimes(a) == 4)
	
	a = [1, 1]
	print(occursXTimes(a) == 0)
	
	a = [1, 2, 2, 2, 3, 3, 3, 3, 1]
	print(occursXTimes(a) == 0)
	
	a = [1, 2, 2]
	print(occursXTimes(a) == 1 or occursXTimes(a) == 2)


occursXTimesTest()
