#!/usr/bin/env python3
"""
Generate 'enumerate-headings' plugin blocks in mkdocs.yml for each book folder.
Skips folders named 'menu'.
"""

import os
import yaml

DOCS_DIR = "docs/books"
MKDOCS_YML = "mkdocs.yml"
EXCLUDE_FOLDERS = {"menu"}

def main():
    # Load existing mkdocs.yml
    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        mkdocs_config = yaml.safe_load(f)

    # Remove any existing enumerate-headings entries
    plugins = mkdocs_config.get("plugins", [])
    plugins = [p for p in plugins if not (isinstance(p, dict) and "enumerate-headings" in p)]

    # Scan books folders
    if not os.path.isdir(DOCS_DIR):
        print(f"No books folder found at {DOCS_DIR}")
        return

    for book_name in sorted(os.listdir(DOCS_DIR)):
        if book_name in EXCLUDE_FOLDERS:
            continue

        book_path = os.path.join(DOCS_DIR, book_name)
        if not os.path.isdir(book_path):
            continue

        # Add enumerate-headings block for this book
        block = {
            "enumerate-headings": {
                "increment_across_pages": True,
                "toc_depth": 6,
                "strict": False,
                "include": [f"books/{book_name}/*.md"]
            }
        }
        plugins.append(block)
        print(f"Added enumerate-headings for {book_name}")

    # Save updated mkdocs.yml
    mkdocs_config["plugins"] = plugins
    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        yaml.dump(mkdocs_config, f, sort_keys=False)

    print("mkdocs.yml updated with enumerate-headings per book.")

if __name__ == "__main__":
    main()