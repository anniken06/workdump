import sys

print("__name__ :", __name__)
print("sys.argv :", sys.argv)  # process arguments
if __name__ == '__main__':
    print("Executed main block!")
else:
    print("Did not execute main block!")