#!/bin/python
#
# A script to verify the Xenon translations in .U.CC files 
# 
# Looks for any known problem before the merge step
#

import glob
import os
import re

#error_found = False

def check_files():
    # Pattern to match more than 3 consecutive spaces
    pattern_spaces = re.compile(r' {4,}')
    pattern_unifield_ellipsis = '…'
    pattern_hyphen = '–'

    # Max line size
    max_line_size = 240

    # Initialize as not error found
    error_found = False

    files = glob.glob(os.path.join("..", "scene_TLs", "*.txt"))

    if not files:
        print("No .txt files found in ../scene_TLs/")
        return

    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                if pattern_spaces.search(line):
                    error_found = True
                    print("WARNING: more than 3 spaces found, will make the game crash")
                    print(f"  File: {filepath}")
                    print(f"  Line: {line_number}")
                    print(f"  Content: {line.rstrip()}")
                    print("-" * 50)
                if pattern_unifield_ellipsis in (line):
                    error_found = True
                    print("WARNING: composite … found, it might not render properly on the game")
                    print(f"  File: {filepath}")
                    print(f"  Line: {line_number}")
                    print(f"  Content: {line.rstrip()}")
                    print("-" * 50)
                if len(line) > max_line_size:
                    error_found = True
                    print("WARNING: line exceeds %s characters, needs to be shortened to fit on a text box" % max_line_size)
                    print(f"  File: {filepath}")
                    print(f"  Line: {line_number}")
                    print(f"  Content: {line.rstrip()}")
                    print("-" * 50)
                if pattern_hyphen in (line):
                    error_found = True
                    print("WARNING: invalid – found, will make the game misbehave")
                    print(f"  File: {filepath}")
                    print(f"  Line: {line_number}")
                    print(f"  Content: {line.rstrip()}")
                    print("-" * 50)
                

    if not error_found:
        print("No errors found in files.")

if __name__ == "__main__":
    check_files()
