#!/usr/bin/env python

import os
import re
import subprocess
import sys
import time


##### Parameters #####
tail_template = "tail -f -n +0"
trigger_pattern = re.compile(r".*(Exception|failed).*")
continuation_pattern = re.compile(r"\s.*")
##### Parameters #####


def print_help():
    help_message = """
Usage:
    $ python filter_tail.py [OPTIONS]

    OPTIONS:
    --clear-file: clears file contents before tailing
"""
    print(help_message)


def fake_print(obj):  # Work-around for OS bug
    print(obj.rstrip())
    time.sleep(1/8)


def find_file(suffix=".out"):
    local_files = os.listdir(os.getcwd())
    local_files.sort(key=os.path.getmtime, reverse=True)
    file = next((filename for filename in local_files if filename.endswith(suffix)), None)
    print("File found: {}.".format(file))
    return file


def clear_file(file):
    clear_command = "echo > {}".format(file)
    subprocess.Popen(clear_command, shell=True).communicate()
    print("Cleared log file.")


def main():
    print_help()

    log_path = find_file()
    pyout_path = log_path + ".PYOUT"
    if "--clear-file" in sys.argv: clear_file(log_path)

    try:
        tail_command = "{} '{}'".format(tail_template, log_path)
        trigger_save = lambda line: (trigger_pattern.match(line))
        continuation_save = lambda line: (continuation_pattern.match(line))
        with open(pyout_path, 'w') as pyout_file:
            save_triggered = False
            process = subprocess.Popen(tail_command, stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, shell=True)
            for line_num, line in enumerate(iter(process.stdout.readline, ""), 1):
                if trigger_save(line) or (save_triggered and continuation_save(line)):
                    if not save_triggered:
                        save_triggered = True
                        fake_print("==================== Saved Line {} ====================".format(line_num))
                        pyout_file.write("\n" + "==================== Saved Line {} ====================".format(line_num) + "\n")
                    fake_print(line)
                    pyout_file.write(line)
                    pyout_file.flush()
                else:
                    save_triggered = False
                    if False:
                        fake_print("Ignored Line {}: \n".format(line_num))
                        fake_print(line)
    except Exception as e:
        raise(e)


if __name__ == '__main__':
    main()
