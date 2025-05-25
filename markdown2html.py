#!/usr/bin/python3
"""
This is a script that converts a Markdown file to HTML.
"""

import sys
import os

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    # Minimal conversion: wrap each line in <p>
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            f_out.write("<p>{}</p>\n".format(line.strip()))

    sys.exit(0)

if __name__ == "__main__":
    main()
