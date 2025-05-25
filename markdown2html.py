#!/usr/bin/python3
"""
This is a script that converts a Markdown file to HTML,
specifically parsing Markdown headings (# to ######)
into corresponding HTML <h1> to <h6> tags.
"""

import sys
import os
import re


def convert_markdown_line(line):
    """
    Convert a single Markdown line to HTML.
    """
    heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
    if heading_match:
        level = len(heading_match.group(1))
        content = heading_match.group(2).strip()
        return f"<h{level}>{content}</h{level}>"
    else:
        content = line.strip()
        if content:
            return f"<p>{content}</p>"
        return ''


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    try:
        with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
            for line in f_in:
                html_line = convert_markdown_line(line)
                if html_line:
                    f_out.write(html_line + '\n')
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
