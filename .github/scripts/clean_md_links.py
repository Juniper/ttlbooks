#!/usr/bin/env python3
"""
Clean Markdown links for a single file:
- Converts [text](somefile.md#anchor) -> [text](#anchor)
- Usage: python clean_md_links.py path/to/file.md
"""

import sys
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python clean_md_links.py <file.md>")
    sys.exit(1)

md_file = Path(sys.argv[1])
if not md_file.is_file():
    print(f"File not found: {md_file}")
    sys.exit(1)

# Match Markdown links with .md files and an anchor
link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+\.md)#([^\)]+)\)')

with md_file.open("r", encoding="utf-8") as f:
    content = f.read()

new_content = link_pattern.sub(r'[\1](#\3)', content)

with md_file.open("w", encoding="utf-8") as f:
    content = f.write(new_content)
    
print(f"Cleaned links in {md_file}")