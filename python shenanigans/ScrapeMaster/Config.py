import os
import sys

class Config:
    data_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "data")
    timeout = 1
    wait_time = None
    use_proxy = True
    auto_y = True
