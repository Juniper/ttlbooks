#!/usr/bin/env python3
import re
import unicodedata
import sys
from pathlib import Path

FIGURE_RE = re.compile(r'!\[(.*?)\]\((.*?)\)')
TABLE_PREFIX_RE = re.compile(r'^\s*Table:\s*(.+)$', re.IGNORECASE)

class MarkdownNumberer:
    def __init__(self):
        self.current_counters = []
        self.figure_counter = 0
        self.table_counter = 0

    def slugify(self, text):
        """Create an anchor ID from heading text."""
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        text = re.sub(r'[\s]+', '-', text)
        return text

    def number_headings(self, line):
        match = re.match(r'^(#{1,6})\s+(.*)', line)
        if not match:
            return line

        level = len(match.group(1))
        title_with_anchor = match.group(2).strip()

        # Extract existing anchor if present
        anchor_match = re.search(r'{#([a-zA-Z0-9_-]+)}$', title_with_anchor)
        if anchor_match:
            anchor = anchor_match.group(1)
            title = title_with_anchor[:anchor_match.start()].strip()
        else:
            title = title_with_anchor
            anchor = self.slugify(title)

        # Numbering logic
        while len(self.current_counters) < level:
            self.current_counters.append(0)
        while len(self.current_counters) > level:
            self.current_counters.pop()

        self.current_counters[level - 1] += 1
        for i in range(level, len(self.current_counters)):
            self.current_counters[i] = 0

        numbering = '.'.join(str(n) for n in self.current_counters if n > 0)

        return f"{match.group(1)} {numbering}. {title} {{#{anchor}}}"

    def number_figures(self, line):
        # ![alt](url)
        def repl(match):
            self.figure_counter += 1
            alt_text = match.group(1)
            url = match.group(2)
            return f"![Figure {self.figure_counter}: {alt_text}]( {url} )"
        return FIGURE_RE.sub(repl, line)

    def number_tables(self, line, prev_line_holder):
        match = TABLE_PREFIX_RE.match(line)
        if match:
            self.table_counter += 1
            caption = match.group(1).strip()
            return None, f"Table: Table {self.table_counter}: {caption}"
        else:
            return line, None

    def process(self, markdown):
        new_lines = []
        in_code_block = False
        prev_line = None
        for line in markdown.splitlines():
            if re.match(r'^(```|~~~)', line):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue

            if in_code_block:
                new_lines.append(line)
                continue

            # Heading numbering
            if re.match(r'^(#{1,6})\s+', line):
                line = self.number_headings(line)

            # Figure numbering
            line = self.number_figures(line)

            # Table numbering
            line, table_caption = self.number_tables(line, prev_line)
            if line is not None:
                new_lines.append(line)
            if table_caption:
                new_lines.append(table_caption)

            prev_line = line

        return "\n".join(new_lines)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <markdown-file>")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    if not md_file.is_file():
        print(f"File not found: {md_file}")
        sys.exit(1)

    markdown = md_file.read_text(encoding="utf-8")
    numberer = MarkdownNumberer()
    numbered_md = numberer.process(markdown)

    md_file.write_text(numbered_md, encoding="utf-8")
    print(f"Processed file: {md_file}")
    print(f"Total figures: {numberer.figure_counter}, Total tables: {numberer.table_counter}")


if __name__ == "__main__":
    main()