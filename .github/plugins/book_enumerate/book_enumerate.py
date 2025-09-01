from mkdocs.plugins import BasePlugin
import re
import unicodedata

class BookEnumeratePlugin(BasePlugin):
    """
    Number headings per book, continuous across pages, skip /menu/, follow nav order.
    Keeps original anchors for references.
    """

    def __init__(self):
        self.counters_per_book = {}
        self.current_counters = []
        self.page_order_per_book = {}

    def on_nav(self, nav, config, files):
        for page in nav.pages:
            src = page.file.src_path
            if src.startswith("books/") and "/menu/" not in src:
                book = src.split("/")[1]
                self.page_order_per_book.setdefault(book, []).append(src)
        return nav

    def slugify(self, text):
        """
        Create an anchor ID from heading text.
        """
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'[^\w\s-]', '', text).strip().lower()
        text = re.sub(r'[\s]+', '-', text)
        return text

    def on_page_markdown(self, markdown, page, config, files):
        src = page.file.src_path

        if not src.startswith("books/") or "/menu/" in src:
            return markdown

        book = src.split("/")[1]
        if book not in self.page_order_per_book:
            return markdown

        self.current_counters = self.counters_per_book[book] = []
        page_index = self.page_order_per_book[book].index(src)

        new_lines = []
        in_code_block = False

        for line in markdown.splitlines():
            if re.match(r'^(```|~~~)', line):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue

            if in_code_block:
                new_lines.append(line)
                continue

            match = re.match(r'^(#{1,6})\s+(.*)', line)
            if not match:
                new_lines.append(line)
                continue

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
            if level == 1:
                while len(self.current_counters) < level:
                    self.current_counters.append(page_index)
            else:
                while len(self.current_counters) < level:
                    self.current_counters.append(0)
                while len(self.current_counters) > level:
                    self.current_counters.pop()

            self.current_counters[level - 1] += 1
            for i in range(level, len(self.current_counters)):
                self.current_counters[i] = 0

            numbering = '.'.join(str(n) for n in self.current_counters if n > 0)

            # Build line with numbering and preserve anchor
            new_lines.append(f"{match.group(1)} {numbering}. {title} {{#{anchor}}}")

        return "\n".join(new_lines)