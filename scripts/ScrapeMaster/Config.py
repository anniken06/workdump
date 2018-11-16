import os
import sys


class Config:
    src_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    data_path = os.path.join(src_path, "data")
    timeout = 1
    wait_time = None
    use_proxy = True
    auto_y = True
