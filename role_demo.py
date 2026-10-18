import os
from search import search_role

for role in ("guest","staff","admin"):
    print("\n==",role)
    for m, _  in search_role("Where is the database configured?",role=role):
        print(" ", os.path.basename(m["path"]), "-",m["access"])