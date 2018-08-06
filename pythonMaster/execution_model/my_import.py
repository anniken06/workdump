print("Begun loading file...")

def spill_secret():
	print("secretMaster")


# Running Python file as a script:
#$ python my_import.py
if __name__ == '__main__':
	print("Script loaded as {}.\nSpilling secrets: ".format(__name__))
	spill_secret()
# Running Python file as a module:
#$ python -c "import my_import"
else:
	print("Script loaded as {}.\nLying about secrets: ".format(__name__))
	print("Nothing to see here")
