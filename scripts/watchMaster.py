#!/usr/bin/env python3

import argparse
import re
import shlex
import subprocess
import time


def checked_returncode(processor):
    def inner(command):
        return_value = processor(command)
        if return_value['returncode'] != 0:
            raise Exception(return_value)
        return return_value
    return inner

@checked_returncode
def run_subprocess(command):
    start_time = time.time()
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()
    return {
        'command': command,
        'stdout': stdout,
        'stderr': stderr,
        'returncode': process.returncode,
        'duration': time.time() - start_time,
    }

def parse_download_results(download_results):
    download_logs = download_results['stdout'].decode('utf-8')
    file_path_pattern = re.compile("(?:\\[download\\] )(.+)(?: has already been downloaded\n)|"
            + "(?:\\[download\\] Destination: )(.+)(?:\n)")
    pattern_matches = re.findall(file_path_pattern, download_logs).pop()
    file_path = next(match for match in pattern_matches if match)
    return file_path

parser = argparse.ArgumentParser(description='youtube-dl + vlc wrapper')
parser.add_argument('url', type=str, help='youtube video url')
parser.add_argument('-f', '--format', type=int, help='chosen format', default=None)
parser.add_argument('-d', '--delete', type=bool, help='delete file after play', default=False)
args = parser.parse_args()

if args.format == None:
    query_results = run_subprocess(f"youtube-dl -F {args.url}")
    print(query_results['stdout'].decode('utf-8'))
    args.format = input("input your chosen format from the list: ")

print(f"Downloading format: {args.format} of URL: {args.url}")
download_results = run_subprocess(f"youtube-dl {args.url} -f {args.format}")
download_file_path = parse_download_results(download_results)

run_subprocess(f"vlc {download_file_path} --play-and-exit")
run_subprocess(f"rm {download_file_path}")
