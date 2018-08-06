#!/usr/bin/python3
# Python's native console is a Read-Eval-Print-Loop (REPL)

# REPL enables real-time execution
1 > 2

# REPL only variable for latest eval
_

# Some statements do not have an explicit REPL response, use print in these cases
x = "Hello " + "World" + "!"*3
print(x)

# Using white space for code blocks standardizes code and make it more readable
if True: 
    print("I'm a code block") 

# Importing libraries
import math
import math as jpMath
math == jpMath

# Importing a chosen set of attributes
from math import exp
from math import exp as jpExp
math.exp == jpMath.exp == exp == jpExp

# Show object contents
dir(math)
dir(math.gcd)
help(math.gcd) # Show help documentation

# Built-in int
10
0b10 # Base 2
0o10 # Base 8
0x10 # Base 16
int("10", base=16) # Casting str to int with base parameter
int("10") # Casting str to int with default base=10
10 // 3 # Integer division

# Built-in float
2.5
3e4 # Scientific notation
10 / 3 # Real division
float("0.12345") # Casting str to float
float('nan') # Defining an NaN or indeterminate number
float('inf') # Defining a positive infinity
1 / float('inf') # This is 0
float('inf') + float('-inf') # This is an indeterminate

# Built-in null value
None
X = None

# Built-in string
"Hi. I'm JP"
'"Hello JP", said JP'
multiline1 = """ Zen of Python #8
Special cases aren't special enough to break the rules."""
multiline2 = ''' Zen of Python #9
Although practicality beats purity.'''
print(multiline1)
print(multiline2)

print("escape\nMaster \' \" \\") # Special characters escape
print(r"raw\nMaster \!@#$%^&*()_:") # Raw / No escape characters

str(1)
str(3*10e8)
str(False)

my_string = "H\u00e5llo world!"
my_bytes = my_string.encode("utf-8") # Data usually gets transferred over networks in bytes, not unicode characters
print(my_string)
print(my_bytes)
my_bytes.decode("utf-8") == my_string

# Built-in lists
my_list = [1, "apple", True, ["metalist",]]
my_list[0]
my_list[-1]

# Built-in dictionary
my_dictionary = {1: 2, "hello": "world", 8: "sqrtMaster"}
my_dictionary[64**0.5]
my_dictionary["hello"]

# Built-in bool and conditionals
True
1 < 2 <= 3 > -1 >= -2 != -3 == -3
bool(None)
bool(0)
bool(-42)
bool(0.00001)
bool(0.00000)
bool("")
bool("(o'u'o)")
bool("False") # nono
bool([])
bool([1,2,3])
bool(())
bool((1,2,3))
bool({})
bool({"hello": "world"})

# If statements
if False:
    print(1)
elif True:
    print(2)
else:
    print(3)

# While statements
while True:
    print("break here")
    break
else:
    print("Entered else?")

i = 3
while i < 0:
    print(i)
    i -= 1
else:
    print("executed while loop with no breaks")

# For statements
for i in [1,2,"3",4]:
    if type(i) == str:
        print("Strings have no power here, breaking...")
        break
    print(i**0.5)
else:
    print("Entered else?")

for c in "hi":
    print(c)
else:
    print("Did not break")






(lambda x: x**2) (20)
(lambda x, y, z: x(y(z))) (lambda a: a + 1, (2).__pow__, 3)
(lambda xi: (xi) (xi)) (lambda xip1: (xip1) (xip1))

https://app.pluralsight.com/player?course=python-fundamentals&author=austin-bingham&name=python-fundamentals-m02-strings&clip=0&mode=live

def numbers(i=0):
    while True:
        yield i
        i += 1

y = numbers()
next(y)
next(y)
next(y)
next(y) # which magic method


# COMPLEX - LARGE RANGE
# COMPLICATED - LARGE NUMBER OF SPECIAL CASES

import this
import antigravity
