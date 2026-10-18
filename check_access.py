import os
from collections import defaultdict
from loader import load_files, REPO_PATH
from access import access_of

groups = defaultdict(list)
for d in load_files(REPO_PATH):
    groups[access_of(d["path"])].append(os.path.relpath(d["path"], REPO_PATH))

for lvl in ("public", "staff", "admin"):
    print(f"\n== {lvl} ({len(groups[lvl])}) ==")
    for f in sorted(groups[lvl]):
        print("  ", f)