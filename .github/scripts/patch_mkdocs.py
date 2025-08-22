import sys, yaml, os

branch = os.environ["BRANCH"]

with open("mkdocs.yml") as f:
    cfg = yaml.safe_load(f)

# Override site_name
cfg["site_name"] = f"TTL Books - This is a work in progress site for the branch {branch}"

def filter_nav(nav):
    new_nav = []
    for item in nav:
        for title, value in item.items():
            if isinstance(value, str):
                if f"books/{branch}/" in value:
                    new_nav.append({title: value})
            elif isinstance(value, list):
                children = filter_nav(value)
                if children:
                    new_nav.append({title: children})
    return new_nav

cfg["nav"] = filter_nav(cfg["nav"])

with open("mkdocs.yml", "w") as f:
    yaml.dump(cfg, f, sort_keys=False)