## The = symbol in Python does not refer to "store" or "write", it means "bind"

## Bindings
x = 123
x
x = None
x
x = "Hello world!"
x

## Functions
def f(inner_x):
    return inner_x
x = 123
f(x)
x = None
f(x)
x = "Hello world!"
f(x)

## Lambdas
g = lambda inner_x: inner_x
x = 123
g(x)
x = None
g(x)
x = "Hello world!"
g(x)
(lambda inner_x: inner_x)("I'm running with no name!")

## Classes
class MyClass:
    x = 123
    def f(x):
        return x
    static_f = staticmethod(f)
    g = lambda gx: gx

MyClass.f(123)
MyClass.static_f(123)
a = MyClass()
a.f(123)
a.static_f(123)
#https://www.programiz.com/python-programming/methods/built-in/staticmethod


## Helper AND MAGIC functions
print("I'll get printed")
dir()
help()  # use q to exit
breakpoint()  # use continue to exit
MAGIC
SCHLICHE
SLICE

def addMaster(x, y):  # Dynamically typed
    print(x, y)
    print(x + y) # magic method already?
    print(x.__add__(y))

def addMaster2(x, y):  # Strongly typed
    print(x, y)
    # Incompatibility error: print(x + y)
    print(x.__add__(x.__class__(y)))

#FUNCTIONS
#LAMBDAS
#SIDE EFFECTS
#HELPER FUNCTIONS breakpoint()

x = 99999
y = 99999
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))

x = 88888
y = x
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))

x = [1, 2, 3]
y = x
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))
x.pop()  # trigger pop on the shared list object -> affects y
print(x, y)

x = [1, 2, 3]
y = x
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))
x = x[:-1]  # rebinds x to a new list -> leaves y alone
print(x, y)