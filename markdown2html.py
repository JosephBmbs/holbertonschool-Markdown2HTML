#!/usr/bin/python3
"""
Convert Markdown to HTML with:
- Headings (# to ######)
- Unordered lists (-)
- Ordered lists (*)
- Paragraphs with <br /> for line breaks inside paragraphs
- Bold (**text**), Italic (__text__)
- Special syntaxes [[text]] -> md5(text), ((text)) -> remove all c/C
"""

import sys
import os
import re
import hashlib


def replace_bold_italic(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text


def replace_special_syntax(text):
    def md5_replacer(match):
        content = match.group(1)
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def remove_c_replacer(match):
        content = match.group(1)
        return re.sub(r'[cC]', '', content)

    text = re.sub(r'\[\[(.+?)\]\]', md5_replacer, text)
    text = re.sub(r'\(\((.+?)\)\)', remove_c_replacer, text)
    return text


def convert_markdown(lines):
    html_lines = []
    in_ul = False
    in_ol = False
    paragraph_buffer = []

    def flush_paragraph():
        nonlocal paragraph_buffer
        if not paragraph_buffer:
            return
        html_lines.append("<p>")
        for i, pline in enumerate(paragraph_buffer):
            line = replace_bold_italic(pline)
            line = replace_special_syntax(line)
            if i < len(paragraph_buffer) - 1:
                html_lines.append(f"{line}<br/>")
            else:
                html_lines.append(line)
        html_lines.append("</p>")
        paragraph_buffer = []

    for line in lines:
        stripped = line.rstrip('\n').rstrip()

        if not stripped:
            # Empty line: flush paragraph and close lists if open
            flush_paragraph()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            continue

        if re.match(r'^\* ', stripped):
            flush_paragraph()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            item = stripped[2:].strip()
            item = replace_bold_italic(item)
            item = replace_special_syntax(item)
            html_lines.append(f"<li>{item}</li>")
            continue

        if re.match(r'^- ', stripped):
            flush_paragraph()
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            item = stripped[2:].strip()
            item = replace_bold_italic(item)
            item = replace_special_syntax(item)
            html_lines.append(f"<li>{item}</li>")
            continue

        # If a list was open but now no list item, close it
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.*)', stripped)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            content = heading_match.group(2).strip()
            content = replace_bold_italic(content)
            content = replace_special_syntax(content)
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        # Otherwise, accumulate line in paragraph buffer
        paragraph_buffer.append(stripped)

    # End of file: flush any remaining paragraph and close lists
    flush_paragraph()
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

    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()

    html_output = convert_markdown(lines)

    with open(output_file, 'w') as f_out:
        for html_line in html_output:
            f_out.write(html_line + '\n')


if __name__ == "__main__":
    main()
