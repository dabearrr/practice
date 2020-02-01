import math

def clear():
	print("------------------------------------------")
	
"""
6.1
string to int and int to string

char to int for each character
for each place multiply by 10
O(N) runtime O(1) space
"""

def stringToInt(s):
	value = 0
	for i in range(len(s)):
		# ord converts the char to its ascii value
		# starting from the back, i subtract the character value of '0' from the current char
		# that gets me the digit value. then I need to consider the digit's place
		# multiplying by 10 * i considers the digit's place
		value += (ord(s[-(i+1)]) - ord('0')) * math.pow(10, i)
	
	return value

def intToString(i):
	string = ""
	temp = i
	
	while temp > 0:
		string += chr((temp % 10) + ord('0'))
		temp = int(temp / 10)
	
	return string[::-1]

#simple test
def stringIntTest():
	a = 1234
	b = "1234"
	
	clear()
	print(intToString(a))
	print(stringToInt(b))

#length is one
def stringIntTest2():
	a = 1
	b = "1"
	
	clear()
	print(intToString(a))
	print(stringToInt(b))

#going to assume no empty string or None ints

stringIntTest()
stringIntTest2()

"""
6.2

change of base
params: string: integer, int: base1, int: base2

traverse int string in reverse order, multiplying by base1 ^ i to get number in base 10

convert base 10 number to base2
"""
def mapping():
	dict = {}
	
	dict[10] = 'A'
	dict[11] = 'B'
	dict[12] = 'C'
	dict[13] = 'D'
	dict[14] = 'E'
	dict[15] = 'F'
	
	return dict

def numToChar(num):
	map = mapping()
	print(map)
	
	if num < 10:
		return chr(ord('0') + num)
	else:
		return map[num]

def changeBase(number, base1, base2):
	baseTenNum = 0
	for i in reversed(range(len(number))):
		baseTenNum += int(number[i]) * int(math.pow(base1, len(number) - 1 - i))
	
	ans = ""
	while baseTenNum > 0:
		ans = ans + numToChar(baseTenNum % base2)
		baseTenNum = int(baseTenNum / base2)
	
	return ans[::-1]

def changeBaseTest():
	str = "22"
	base1 = 16
	base2 = 12
	
	clear()
	print(changeBase(str, base1, base2))
	
changeBaseTest()

"""
6.3

map letters to values
can subtract 'A' to avoid building a hash table
ord(letter) - ord('A') + 1

there is no A0
26 -> 27
goes Z -> AA

BA = 53

multiply by 26 ^ digit place

"""

def convertToNum(a):
	return ord(a) - ord('A') + 1

def computeSpread(A):
	ans = 0
	for i in range(len(A)):
		ans += convertToNum(A[len(A) - 1 - i]) * math.pow(26, i)
	
	return ans

def computeSpreadTest():
	str = "AA"
	ans = 27
	clear()
	print("returns {}, should be {}", computeSpread(str), ans)

def computeSpreadTest2():
	str = "Z"
	ans = 26
	clear()
	print("returns {}, should be {}", computeSpread(str), ans)
	
def computeSpreadTest3():
	str = "ZZ"
	ans = 702
	clear()
	print("returns {}, should be {}", computeSpread(str), ans)

def computeSpreadTest4():
	str = "AAA"
	ans = 703
	clear()
	print("returns {}, should be {}", computeSpread(str), ans)

computeSpreadTest()
computeSpreadTest2()
computeSpreadTest3()
computeSpreadTest4()
"""
6.4

replace and remove

replace as with two ds
delete bs

brute force is to build a new string while traversing the original
adding dd instead of a in the string and skipping bs

o(n) runtime o(n) space

better method traverse the string from two points
right size of the passed size and the end of the string, building it in reverse

O(size passed) runtime O(1) space since we reuse passed in array
"""

# assumes array passed in is correct size
def repRemove(A, size):
	i = size - 1
	j = len(A) - 1
	
	while j >= 0 and i >= 0:
		if A[i] == 'a':
			A[j] = 'd'
			A[j-1] = 'd'
			j -= 2
		elif A[i] != 'b':
			A[j] = A[i]
			j-=1
		i-=1
	
	return A

def repRemove2(A, size):
	newSize = size
	for i in range(size):
		if A[i] == 'a':
			newSize += 1
		elif A[i] == 'b':
			newSize -= 1
	

	i = size - 1
	j = newSize - 1
	
	while j >= 0 and i >= 0:
		if A[i] == 'a':
			A[j] = 'd'
			A[j-1] = 'd'
			j -= 2
		elif A[i] != 'b':
			A[j] = A[i]
			j-=1
		i-=1
	
	return A

def repRemoveTest():
	A = ['a', 'b', 'a', 'c', 'e']
	s = 4
	
	print(repRemove(A, s))
	
def repRemoveTest2():
	A = ['a', 'b', 'a', 'c', 'e', 'l', 'l', 'l']
	s = 4
	
	print(repRemove(A, s))
	
repRemoveTest()
repRemoveTest2()

def repRemove2Test():
	A = ['a', 'b', 'a', 'c', 'e']
	s = 4
	
	print(repRemove2(A, s))

def repRemove2Test2():
	A = ['a', 'b', 'a', 'c', 'e', 'l', 'l', 'l']
	s = 4
	
	print(repRemove2(A, s))
	
repRemove2Test()
repRemove2Test2()

"""
6.5

Test palindomicity

check if a string is a palindrome

ex:
tacocat
tacoocat

ex2:
a man, a plan, a canal, Panama
amanaplanacanalpanama

brute force
make a reversed copy of string

check string == reversedString

O(n) runtime O(n) memory

better:
traverse the string from both sides until the middle, comparing the two sides

O(n) runtime, O(1) memory
"""

def isAlphanumeric(a):
	return (ord(a) >= ord('a') and ord(a) <= ord('z')) or \
	(ord(a) >= ord('A') and ord(a) <= ord('Z')) or \
	(ord(a) >= ord('0') and ord(a) <= ord('9'))

def convertIfNeeded(c):
	if ord(c) >= ord('A') and ord(c) <= ord('Z'):
		return chr(ord(c) - ord('A') + ord('a'))
	else:
		return c
		
	
def palindrome(str):
	i = 0
	j = len(str) - 1
	
	while i < j and i >= 0 and j >= 0:
		if isAlphanumeric(str[i]) and isAlphanumeric(str[j]):
			print(str[i])
			print(str[j])
			if convertIfNeeded(str[i]) != convertIfNeeded(str[j]):
				return False
			i += 1
			j -= 1
		else:
			if not isAlphanumeric(str[i]):
				i += 1
			if not isAlphanumeric(str[j]):
				j -= 1
	return True
		
def palindromeTest():
	s = "tacocat"
	
	clear()
	print(palindrome(s))
	
def palindromeTest2():
	s = "tacoocat"
	
	clear()
	print(palindrome(s))
	
def palindromeTest3():
	s = "tacodfgsdgocat"
	
	clear()
	print(palindrome(s))
	
def palindromeTest4():
	s = "a man, a plan, a canal, Panama"
	
	clear()
	print(palindrome(s))

palindromeTest()
palindromeTest2()
palindromeTest3()
palindromeTest4()

"""
6.6
"""

"""
6.7
"""

"""
6.8
"""

"""
6.9
"""

"""
6.11
"""