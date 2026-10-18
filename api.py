import os
import json
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import search_role
from access import ROLE_LEVEL

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIT_FILE = "audit.log"

def audit(role, question, files):
    entry = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "question": question,
        "files_returned": files,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

@app.get("/search")
def api_search(q: str, k: int = 5, role: str = "guest"):
    if role not in ROLE_LEVEL:
        role = "guest"  # unknown roles get the least access
    results = search_role(q, role=role, k=k)
    files = [os.path.basename(m["path"]) for m, _ in results]
    audit(role, q, files)
    return {
        "question": q,
        "role": role,
        "sources": [
            {
                "file": os.path.basename(m["path"]),
                "start_line": m["start_line"],
                "end_line": m["end_line"],
                "access": m["access"],
                "text": doc,
            }
            for m, doc in results
        ],
    }