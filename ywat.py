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

# Built-in collections



# Built-in bool
True
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

1 < 2 <= 3 > -1 >= -2 != -3 == -3

if False:
    print(1)
elif True:
    print(2)
else:
    print(3)

(lambda x: x**2) (20)
(lambda x, y, z: x(y(z))) (lambda a: a + 1, (2).__pow__, 3)
(lambda xi: (xi) (xi)) (lambda xip1: (xip1) (xip1))