#!/usr/bin/python3
"""
A Script that converts a Markdown file to HTML.
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

    with open(input_file, 'r') as md_file:
        markdown_text = md_file.read()

    with open(output_file, 'w') as html_file:
        html_file.write(markdown_text)

    sys.exit(0)

if __name__ == "__main__":
    main()
