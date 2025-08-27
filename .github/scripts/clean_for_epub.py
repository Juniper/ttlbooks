#!/usr/bin/env python3
import re
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} input.md output.md")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Read input file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Regex for fenced code blocks (```...```) and inline code (`...`)
code_pattern = re.compile(r'(```.*?```|`[^`]+`)', re.DOTALL)

# Regex for <...> placeholders
placeholder_pattern = re.compile(r'<([A-Za-z0-9\-\/_]+)>')

def escape_placeholders(text):
    """Escape <...> unless they are real HTML tags (a, img, p, etc.)"""
    # whitelist of real HTML tags
    html_tags = {"a", "p", "img", "div", "span", "ul", "ol", "li",
                 "table", "thead", "tbody", "tr", "th", "td",
                 "h1", "h2", "h3", "h4", "h5", "h6",
                 "br", "hr", "strong", "em", "code", "pre"}
    
    def replacer(match):
        text = match.group(1)
        if text.lower() in html_tags:
            return f"<{text}>"
        return f"&lt;{text}&gt;"
    
    escaped = placeholder_pattern.sub(replacer, text)
    
    # remove any line containing only \pagebreak (or optional spaces)
    escaped = re.sub(r'^\s*\\pagebreak\s*$\n?', '', escaped, flags=re.MULTILINE)
    
    return escaped

# Split into segments: code vs non-code
parts = []
last_end = 0
for m in code_pattern.finditer(content):
    # normal text before code → escape placeholders + remove \pagebreak
    parts.append(escape_placeholders(content[last_end:m.start()]))
    # code block or inline code → keep as is
    parts.append(m.group(0))
    last_end = m.end()

# remaining text after last code → escape placeholders + remove \pagebreak
parts.append(escape_placeholders(content[last_end:]))

# Write output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("".join(parts))

print(f"Processed '{input_file}' → '{output_file}'")