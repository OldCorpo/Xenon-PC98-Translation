import sys
import os
import argparse

N = 500
TRUE = True
FALSE = False

lines = 0
no_indentation = False


def japanese_space():
    # Equivalent to -127, 64 in signed char (C)
    # We'll reproduce raw byte behavior using latin-1
    return bytes([129, 64]).decode("latin-1")


def insert_spaces(name_size):
    if name_size == 0:
        return ""

    space = japanese_space()
    spaces = ""

    i = 0
    while i < name_size:
        spaces += space
        i += 2

    if name_size % 2 == 0:
        spaces += " "

    return spaces


def find_colon(line):
    try:
        return line.index(":")
    except ValueError:
        return 0


def name_size(line):
    if no_indentation:
        return 0
    if line.startswith("["):
        return find_colon(line)
    return 0


def remove_problem_indicator(line):
    must_not_be_formatted = False

    if line.startswith("/*"):
        line = line[2:]
    elif line.startswith("<>"):
        line = line[2:]
        must_not_be_formatted = True

    return line, must_not_be_formatted


def remove_comment(line):
    index = line.find("//")
    if index != -1:
        line = line[:index] + "\n"
    return line


def find_last_word_before_x60(line, end_line_position):
    last_cr = end_line_position
    i = last_cr + 61

    if i >= len(line):
        return -1, False

    while i > last_cr and line[i] != " ":
        i -= 1

    delete_space = (i == last_cr + 61)
    return i, delete_space


def need_to_do_something(line, end_line_position):
    return len(line) - end_line_position + 1 > 60


def format60(line):
    end_line_position = -1
    ancient_pos = -1

    while need_to_do_something(line, end_line_position):
        pos, delete_space = find_last_word_before_x60(line, end_line_position)

        if pos >= 0:
            first_part = line[:pos]
            name_sz = name_size(first_part)
            spaces = insert_spaces(name_sz)

            if delete_space:
                second_part = line[pos + 1:]
                line = first_part + spaces + second_part
                end_line_position = pos - 1
            else:
                second_part = line[pos + 1:]
                line = first_part + "\\n" + spaces + second_part
                end_line_position = pos + 1

        if pos != ancient_pos:
            ancient_pos = pos
        else:
            break

    return line


def size(line):
    return line.find("\n") if "\n" in line else len(line)


def no_tag(line):
    return "<" not in line


def check_spaces(line):
    for i in range(len(line) - 2):
        if line[i] == line[i + 1] == line[i + 2] == " ":
            print(f'Line #{lines}: "{line.strip()}" has more than 3 spaces in a row. Aborting...')
            sys.exit(1)


def format_line(line):
    if line == "\n":
        return line

    line, must_not_be_formatted = remove_problem_indicator(line)
    line = remove_comment(line)
    check_spaces(line)

    if size(line) > 60 and no_tag(line) and not must_not_be_formatted:
        line = format60(line)

    return line


def main():
    global no_indentation, lines

    parser = argparse.ArgumentParser(description="Xenon script formatter")
    parser.add_argument("input", help="Input file")
    parser.add_argument("output", help="Output file")
    parser.add_argument("-i", "--no-indent", action="store_true",
                        help="Disable indentation in dialogues")

    args = parser.parse_args()

    '''
    if len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    elif len(sys.argv) == 4 and sys.argv[1] == "-i":
        no_indentation = True
        input_file = sys.argv[2]
        output_file = sys.argv[3]
    else:
        sys.exit(1)

    print(f"Opening file {input_file}")
    print(f"Writing in file {output_file}")

    no_comment_lines = 0

    with open(input_file, "r", encoding="latin-1") as read, \
         open(output_file, "w", encoding="latin-1") as write:
    '''

    no_comment_lines = 0

    print(f"Opening file {args.input}")
    print(f"Writing in file {args.output}")

    with open(args.input, "r", encoding="latin-1") as read, \
         open(args.output, "w", encoding="latin-1") as write:

        for line in read:
            if not line.startswith("#"):
                if no_comment_lines % 2 == 1:
                    write.write(format_line(line))
                else:
                    write.write(line)
                no_comment_lines += 1
            lines += 1


if __name__ == "__main__":
    main()
