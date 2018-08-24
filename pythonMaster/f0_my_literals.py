## Comments are preceded by the symbol #

EVERYTHING IS AN OBJECT
FUNCTIONS ARE OBJECTS
LAMBDAS ARE OBJECTS
CLASSES ARE OBJECTS

## None Literals
None

## Boolean Literals
True
False

## Integer Literals: https://docs.python.org/3/reference/lexical_analysis.html#integer-literals
100  # Decimal Literal 
0b111  # Binary Literal
0o777  # Octal Literal
0xfff  # Hexadecimal Literal
+1_000_0_00  # Signed literal with grouping delimiters
-0xdead_beef  # Signed literal with grouping delimiters

## Float Literals: https://docs.python.org/3/reference/lexical_analysis.html#floating-point-literals
3.14
+10.
-.001
+314000e-3  # Signed literal in scientific notation
3.14_15_93  # Literal with grouping delimiters

## Complex Literals: https://docs.python.org/3/reference/lexical_analysis.html#imaginary-literals
3.14j
+10.j
-.001j
+314000e-3j  # Signed literal in scientific notation
3.14_15_93j  # Literal with grouping delimiters

## String / Byte Literals: 
"I'm JP"
'JP said "This sentence is false."'
"""multiline string begins here
I'm JP
multiline string ends here OwO"""
'''multiline string begins here
JP said "This sentence is false."
multiline string ends here OwO'''
r"I'm an escaped string"
f"I can auto-inject pre-existing variables {__name__}"
"I\'m a manually escaped string"
b"I\'m a manually escaped bytecode"

## Tuple Literals - these are immutable arrays
()  # Empty tuple
(1, )  # Singleton tuple: removing the , symbol will confuse the parser
(
+1, 
2.0j, 
True, 
"foo", 
(1, 2, 3), 
)

## List Literals - these are mutable arrays
[] # Empty list
[1, ]  # Singleton list: removing the , symbol will not confuse the parser
[
+1, 
2.0j, 
True, 
"foo", 
[1, 2, 3], 
(1, 2, 3), 
]

## Dictionary / HashMap Literals - hashes of the immutable keys refer to the paired values
{}  # Empty dictionary
{
10: True, 
-2.5: 10, 
True: -2.5, 
(11, 12, 13): "typeMaster", 
(21, 22, 23): [1, 2, 3], 
}
