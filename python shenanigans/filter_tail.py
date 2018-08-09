#!/usr/bin/env python

import os
import re
import subprocess
import sys
import time


##### Parameters #####
do_clear = False
tail_template = "tail -f -n +0"
trigger_pattern = re.compile(r".*(Exception|failed).*")
continuation_pattern = re.compile(r"\s.*")
max_lookbehind_length = 6
max_line_length = 512
##### Parameters #####


def print_help():
    help_message = """
Usage:
    $ python filter_tail.py <OPTIONS>

    OPTIONS:
    --clear-file: clears file contents before tailing

    To explore log files in ssh:
        Open the log file with: 
            $ nano -c <log_path>
        Navigate with:
            Alt + G, <line_num>, Enter
        Exit with:
            Esc, Ctrl + X, N, Enter
"""
    print(help_message)


def fake_print(obj):  # Work-around for OS bug
    sobj = str(obj).rstrip()
    end = "......" if len(sobj) == max_line_length else ""
    print(sobj + end)
    time.sleep(1/5)


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
    will_clear = True if "--clear-file" in sys.argv else do_clear

    if will_clear:
        clear_file(log_path)

    try:
        tail_command = "{} '{}'".format(tail_template, log_path)
        trigger_save = lambda line: (
            trigger_pattern.match(line) 
            and "Cannot convert null object to JSON" not in line
            and "Invalid UUID string" not in line
            and "quest/new" not in line
            and "Exception occurred accessing endpoint user in null.null" not in line
            and "HTTP 404 Not Found" not in line
            and not line.startswith(" ")
            and not line.startswith("\t")
            and not continuation_pattern.match(line))
        continuation_save = lambda line: (continuation_pattern.match(line))

        lines_lookbehind = []
        save_triggered = False
        with open(pyout_path, 'w') as pyout_file:
            process = subprocess.Popen(tail_command, stdout=subprocess.PIPE, universal_newlines=True, bufsize=-1, shell=True)
            for line_num, line in enumerate(iter(process.stdout.readline, ""), 1):
                line = line[ :max_line_length]
                lines_lookbehind = lines_lookbehind[-max_lookbehind_length + 1: ]
                if trigger_save(line) or (save_triggered and continuation_save(line)):
                    if not save_triggered:
                        save_triggered = True
                        fake_print("================================================================================")
                        pyout_file.write("\n" + "================================================================================" + "\n")
                        fake_print("==================== Lookbehind for Line:{} ====================".format(line_num))
                        pyout_file.write("\n" + "==================== Lookbehind for Line:{} ====================".format(line_num) + "\n")
                        for lookbehind in lines_lookbehind:
                            fake_print(lookbehind)
                            pyout_file.write(lookbehind)
                            pyout_file.flush()
                        fake_print("==================== Save Line Triggered on Line:{} ====================".format(line_num))
                        pyout_file.write("\n" + "==================== Saved Line Triggered on Line:{} ====================".format(line_num) + "\n")
                    fake_print(line)
                    pyout_file.write(line)
                    pyout_file.flush()
                else:
                    save_triggered = False
                lines_lookbehind += [line]
    except Exception as e:
        raise(e)


if __name__ == '__main__':
    main()
