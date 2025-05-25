#!/usr/bin/python3
"""
This script converts a Markdown file to HTML,
handling headings (# to ######), unordered lists (- item),
ordered lists (* item), and paragraphs with line breaks.
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
    in_ul = False
    in_ol = False
    paragraph_buffer = []  # pour accumuler les lignes d'un paragraphe

    def flush_paragraph():
        """Convert accumulated paragraph lines to HTML and append to html_lines."""
        nonlocal paragraph_buffer
        if not paragraph_buffer:
            return
        html_lines.append("<p>")
        # On joint les lignes avec <br/> sauf la dernière
        for i, pline in enumerate(paragraph_buffer):
            if i < len(paragraph_buffer) - 1:
                html_lines.append(f"{pline}<br/>")
            else:
                html_lines.append(pline)
        html_lines.append("</p>")
        paragraph_buffer = []

    for line in lines:
        stripped = line.rstrip('\n').rstrip()

        # Ligne vide : on doit finir paragraphes et listes en cours
        if not stripped:
            flush_paragraph()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            continue

        # Liste ordonnée (* )
        if re.match(r'^\* ', stripped):
            flush_paragraph()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            item = stripped[2:].strip()
            html_lines.append(f"<li>{item}</li>")
            continue

        # Liste non ordonnée (- )
        if re.match(r'^- ', stripped):
            flush_paragraph()
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            item = stripped[2:].strip()
            html_lines.append(f"<li>{item}</li>")
            continue

        # Si on était dans une liste, on la ferme
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

        # Titres
        heading_match = re.match(r'^(#{1,6})\s+(.*)', stripped)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            content = heading_match.group(2).strip()
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        # Tout ce qui reste c'est du texte (paragraphe)
        paragraph_buffer.append(stripped)

    # Fin du fichier : flush paragraph et listes ouvertes
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
