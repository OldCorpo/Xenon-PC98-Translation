#!/usr/bin/env python3

import sys
import glob
import re
import unicodedata

COLUMN = 60
MAX_MULTIPLES = 4
LIMITS = [COLUMN * i for i in range(1, MAX_MULTIPLES + 1)]
MAX_LEN = COLUMN * MAX_MULTIPLES


def char_width(ch):
    """Return visual width."""
    if ch == "　":
        return 2
    if unicodedata.east_asian_width(ch) in ("F", "W"):
        return 2
    return 1


def build_visual_map(line):
    """
    Map string indices to visual columns.
    """
    cols = []
    col = 0
    for ch in line:
        cols.append(col)
        col += char_width(ch)
    return cols, col


def detect_crossings(line):
    """
    Detect words crossing visual column boundaries.
    """
    results = []

    col_map, _ = build_visual_map(line)

    for match in re.finditer(r'\S+', line):
        word = match.group()
        start = match.start()
        end = match.end()

        start_col = col_map[start]
        end_col = col_map[end - 1] + char_width(line[end - 1])

        for boundary in LIMITS:
            if start_col < boundary < end_col:
                split_pos = boundary - start_col
                split_word = word[:split_pos] + "|" + word[split_pos:]
                results.append((boundary, word, split_word))

    return results


def detect_space_overshoot(line):
    """
    Detect spaces overshooting boundaries.
    """
    results = []

    visual_col = 0
    i = 0
    n = len(line)

    while i < n:
        ch = line[i]
        w = char_width(ch)

        prev_col = visual_col
        visual_col += w

        for boundary in LIMITS:
            if prev_col < boundary <= visual_col:

                j = i + 1
                ascii_spaces = 0
                wide_spaces = 0

                while j < n and line[j] in (" ", "　"):
                    if line[j] == " ":
                        ascii_spaces += 1
                        visual_col += 1
                    else:
                        wide_spaces += 1
                        visual_col += 2
                    j += 1

                count = ascii_spaces + wide_spaces

                if count > 0:
                    space_type = "wide-space" if wide_spaces else "ascii space"

                    start = max(0, i - 5)
                    end = min(n, j + 5)
                    snippet = line[start:end].replace("\n", "")

                    results.append((space_type, count, boundary + 1, snippet))

                i = j - 1
                break

        i += 1

    return results


def process_file(path):
    with open(path, "rb") as f:
        data = f.read()

    lines = re.split(rb'(\r\n|\n|\r)', data)

    lineno = 1
    i = 0

    while i < len(lines):
        line = lines[i]
        if i + 1 < len(lines):
            newline = lines[i + 1]
        i += 2

        try:
            text = line.decode("utf-8", errors="replace")
        except:
            text = line.decode("latin1", errors="replace")

        stripped = text.lstrip()

        if stripped.startswith("//") or stripped.startswith("#"):
            lineno += 1
            continue

        crossings = detect_crossings(text)
        overshoots = detect_space_overshoot(text)

        visual_len = sum(char_width(c) for c in text)
        too_long = visual_len > MAX_LEN

        if crossings or overshoots or too_long:
            print(f"{path}:{lineno}:")

            for boundary, word, split_word in crossings:
                if boundary <= 61:
                    nameboundary = 'first'                
                elif boundary <= 121:
                    nameboundary = 'second'
                elif boundary <= 181:
                    nameboundary = 'third'
                elif boundary <= 241:
                    nameboundary = 'fourth'
                else:
                    nameboundary = 'out of bound'

                split_index = split_word.index("|")

                if boundary == MAX_LEN and too_long:
                    print(
                        f"{split_index} char, word '{split_word}' crosses column {boundary} and out of bound."
                    )
                    #print(f"{split_index} characters before break.")
                else:
                    #print(f"word '{split_word}' crosses column {boundary}")
                    print(f"{split_index} char, word '{split_word}' crosses {nameboundary} column.")
                    #print(f"{split_index} characters before break.")

            for space_type, count, col, snippet in overshoots:
                print(
                    f"{space_type} '|{snippet}' overshooted column, {count} times, at {col}"
                )

            if too_long:
                print(f"WARNING: line exceeds visual column {MAX_LEN}")

            print()

        lineno += 1


def main():
    if len(sys.argv) < 2:
        print("Usage: check_columns.py <file_or_pattern> [...]")
        sys.exit(1)

    files = []
    for arg in sys.argv[1:]:
        files.extend(glob.glob(arg))

    if not files:
        print("No files matched.")
        sys.exit(1)

    for f in sorted(files):
        process_file(f)


if __name__ == "__main__":
    main()
