<h1 align="center">Markdown to HTML</h1>

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1346/format:webp/1*7xWQaJtUL3UU2YE8Q0qp6Q.gif" alt="Markdown Logo" >
</p>

> Novice Level  
> By: Guillaume, CTO at Holberton School  
> Weight: 1  

---

## 📖 Description

Markdown is awesome! All your `README.md` files are written in Markdown, but do you know how GitHub renders them behind the scenes?

This project is about building a simple Markdown-to-HTML converter using Python. You will parse Markdown syntax and convert it to corresponding HTML, without using external Markdown libraries.

---

## ✅ Requirements

- All files are interpreted/compiled on **Ubuntu 18.04 LTS** using **Python 3 (version 3.7 or higher)**
- The **first line** of all your files should be exactly:
  ```python
  #!/usr/bin/python3
  ```
- A `README.md` file at the root of the folder is **mandatory**
- Your code must follow **PEP 8 style guide** (version 1.7.\*)
- All your files must be **executable**
- All your Python modules must be **documented**:
  ```bash
  python3 -c 'print(__import__("my_module").__doc__)'
  ```
- Your code should **not execute** when imported:
  ```python
  if __name__ == "__main__":
      # entry point
  ```
- You **are not allowed** to use the built-in Python Markdown library

---

## 🚀 Features

- Converts Markdown to HTML:
  - Headers
  - Emphasis (bold and italic)
  - Unordered lists
  - Paragraphs

---

## 🛠 Usage

```bash
./markdown2html.py README.md README.html
```

- Converts the Markdown file `README.md` into `README.html`.

---

## 📌 Example

Given a simple Markdown file:

```markdown
# My Title

This is **bold** and *italic* text.

- Item 1
- Item 2
```

Your HTML output should be:

```html
<h1>My Title</h1>
<p>This is <strong>bold</strong> and <em>italic</em> text.</p>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
```

---

## 👤 Author

Created by **Youssef Saad**  
Part of the **holbertonschool-web_front_end** curriculum.
