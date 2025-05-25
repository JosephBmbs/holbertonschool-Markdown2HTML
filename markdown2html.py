#!/usr/bin/python3
"""
This script converts a Markdown file to HTML,
handling headings (# to ######), unordered lists (- item),
and ordered lists (* item).
"""

import sys
import os
import re


def convert_markdown(lines):
    """
    Convert a list of Markdown lines to HTML lines.
    Returns a list of HTML lines.
    """
    html_lines = []
    in_ul = False  # Are we inside a <ul> block?
    in_ol = False  # Are we inside an <ol> block?

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            continue

        # Ordered list item (*)
        if re.match(r'^\* ', stripped):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            item = stripped[2:].strip()
            html_lines.append(f"<li>{item}</li>")
            continue

        # Unordered list item (-)
        if re.match(r'^- ', stripped):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            item = stripped[2:].strip()
            html_lines.append(f"<li>{item}</li>")
            continue

        # If we leave any list
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.*)', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2).strip()
            html_lines.append(f"<h{level}>{content}</h{level}>")
        else:
            html_lines.append(f"<p>{stripped}</p>")

    # Close any open list at end of file
    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")

    return html_lines


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
        with open(input_file, 'r') as f_in:
            lines = f_in.readlines()

        html_output = convert_markdown(lines)

        with open(output_file, 'w') as f_out:
            for html_line in html_output:
                f_out.write(html_line + '\n')

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
