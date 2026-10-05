import os
from search import search

# (question, file that should contain the answer)
EVAL = [
    ("How does user registration work?", "authController.js"),
    ("Where is the password hashed?", "authController.js"),
    ("Which routes handle login and forgot password?", "authRoutes.js"),
    ("How is a resume exported?", "exportController.js"),
    ("Where is the database configuration?", "config.js"),
    ("How are documents handled?", "documentController.js"),
    ("How are job applications handled?", "applicationController.js"),
    ("Where is the Express server started?", "app.js"),
    ("How does login verify the password?", "authController.js"),
    ("How is the forgot password flow handled?", "authController.js"),
    ("How does reset password work?", "authController.js"),
    ("What does the login endpoint return?", "authController.js"),
    ("Which route registers a new user?", "authRoutes.js"),
    ("Which routes belong to exporting a resume?", "exportRoutes.js"),
    ("Which routes handle resume versions?", "versionRoutes.js"),
    ("How are resume versions saved?", "versionRoutes.js"),
    ("How is a document created?", "documentController.js"),
    ("How is a document updated or deleted?", "documentController.js"),
    ("How does the export controller generate the file?", "exportController.js"),
    ("How is a job application created?", "applicationController.js"),
    ("How are job applications listed or updated?", "applicationController.js"),
    ("Which database name and host are configured?", "config.js"),
    ("Which packages does the project depend on?", "package.json"),
    ("Which middleware and routes does app.js use?", "app.js"),
    ("What is the callback example with error-first handling?", "callback-practice.js"),
    ("How do promises work in the practice file?", "promises-practice.js"),
]

def hit_rate(name="naive", k=5, search_fn=search):
    hits = 0
    for q, expected in EVAL:
        results = search_fn(q, name=name, k=k)
        files = [os.path.basename(m["path"]) for m, _ in results]
        exp = expected if isinstance(expected, (list, tuple, set)) else [expected]
        ok = any(e in files for e in exp)
        hits += ok
        print("OK  " if ok else "MISS", q, "->", files[:3])
    print(f"\nHit rate@{k}: {hits}/{len(EVAL)} = {hits/len(EVAL):.0%}")

if __name__ == "__main__":
    hit_rate()