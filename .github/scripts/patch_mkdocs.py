#!/usr/bin/env python3
import os
import sys
import yaml

def filter_nav(nav, branch):
    """
    Recursively filter nav to only keep entries containing the branch path.
    """
    filtered = []
    found = False

    for item in nav:
        if isinstance(item, dict):
            key, value = list(item.items())[0]

            if isinstance(value, list):
                # Recurse into submenus
                sub_filtered, sub_found = filter_nav(value, branch)
                if sub_found:
                    filtered.append({key: sub_filtered})
                    found = True
            elif isinstance(value, str):
                if f"books/{branch}/" in value:
                    filtered.append({key: value})
                    found = True
        else:
            # nav entries should always be dicts, but just in case
            if isinstance(item, str) and f"books/{branch}/" in item:
                filtered.append(item)
                found = True

    return filtered, found

def main():
    branch = os.environ.get("BRANCH")
    if not branch:
        print("Error: BRANCH environment variable not set", file=sys.stderr)
        sys.exit(1)

    with open("mkdocs.yml", "r") as f:
        config = yaml.safe_load(f)

    # Patch site_name
    config["site_name"] = f"TTL Books - This is a work in progress site for the branch {branch}"

    # Patch nav
    if "nav" in config:
        filtered_nav, found = filter_nav(config["nav"], branch)
        if not found:
            print(f"Error: branch '{branch}' not found in mkdocs.yml nav", file=sys.stderr)
            sys.exit(1)
        config["nav"] = filtered_nav

    # Save patched mkdocs.yml
    with open("mkdocs.yml", "w") as f:
        yaml.dump(config, f, sort_keys=False, width=1000)

if __name__ == "__main__":
    main()