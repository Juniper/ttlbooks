#!/usr/bin/env python3
import os
import sys
import yaml

branch = os.environ.get("BRANCH")
if not branch:
    print("Error: BRANCH environment variable not set", file=sys.stderr)
    sys.exit(1)

mkdocs_file = "mkdocs.yml"
with open(mkdocs_file) as f:
    config = yaml.safe_load(f)

# Update site_name
config["site_name"] = f"Day One Books - This is a work in progress site for the branch {branch}"

# Update site_dir based on branch
if branch == "main":
    config["site_dir"] = "/var/www/html/main"
else:
    config["site_dir"] = f"/var/www/html/{branch}"

def filter_nav(nav):
    """
    Recursively filter nav items: keep only those that contain the branch in their path,
    and preserve parent items if they lead to branch files.
    """
    new_nav = []
    for item in nav:
        if isinstance(item, dict):
            key, value = list(item.items())[0]
            if isinstance(value, str):
                if branch in value:
                    new_nav.append({key: value})
            elif isinstance(value, list):
                filtered_children = filter_nav(value)
                if filtered_children:
                    # Rename "All Books" -> "Your Book"
                    if key == "All Books":
                        key = "Your Book"
                    new_nav.append({key: filtered_children})
        else:
            if branch in str(item):
                new_nav.append(item)
    return new_nav

filtered_nav = filter_nav(config.get("nav", []))

if not filtered_nav:
    print(f"Error: No nav entries found for branch '{branch}'", file=sys.stderr)
    sys.exit(1)

config["nav"] = filtered_nav

with open(mkdocs_file, "w") as f:
    yaml.dump(config, f, sort_keys=False)