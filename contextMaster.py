import sys
from io import StringIO
import contextlib

#process = subprocess.Popen("python inner.py thereare myinputs", stdout=subprocess.PIPE)

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def getProcessReturn(code):
    with stdoutIO() as s:
        try:
            exec(code)
            return s.getvalue()
        except Exception as e:
            print("Something wrong with the code: ", e)


if __name__ == '__main__':
    code = """
# my code is here
i = [0,1,2]
for j in i :
    print(j)
"""
    capturedStdout = getProcessReturn(code)
    print(capturedStdout)