# The = symbol in Python does not refer to "store" or "write", it means "bind"

x = 99999
y = 99999
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))

x = 88888
y = x
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))

x = [1,2,3]
y = x
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))
x.pop()  # trigger pop on the shared list object -> affects y
print(x, y)

x = [1,2,3]
y = x
print("{} == {} := {}".format(x, y, x == y))
print("id:{} == id:{} := {}".format(id(x), id(y), x is y))
x = x[:-1]  # rebinds x to a new list -> leaves y alone
print(x, y)


def norebind_pop(inner_f):  # operates on the same object binding
    inner_f.pop()
    return inner_f


def rebind_pop(inner_f):  # operates on a different object binding
    inner_f = inner_f[0:1] + inner_f[1:]
    inner_f.pop()
    return inner_f


f = [1,2,3]
norebind_pop(f)
f

f = [1,2,3]
rebind_pop(f)
f


# Default kwargs are binded only once on declaration
def append_None(my_list=[]):
    my_list.append(None)
    return my_list


append_None([1,2])
append_None([3,4])

append_None()  # Uses the default my_list binding
append_None()  # Uses the default my_list binding, which now has contains pre-existing elements [None]


# Rebinding is kew
def rebind_append_None(my_list=[]):
    my_list = my_list[:]
    my_list.append(None)
    return my_list


rebind_append_None([1,2])
rebind_append_None([3,4])

rebind_append_None()  # Uses the default my_list binding
rebind_append_None()  # Uses the default my_list binding, which now has contains pre-existing elements [None]

