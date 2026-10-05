import os

REPO_PATH = r"D:\resumeflow-projects\resumeflow-mysql-api"

SKIP_DIRS = {"node_modules", "dist", ".git", ".angular", "venv", "__pycache__"}
EXTENSIONS = {".ts", ".js", ".md", ".json", ".html", ".sql"}

def load_files(repo_path):
    docs = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if os.path.splitext(name)[1] in EXTENSIONS and name != "package-lock.json":
                path = os.path.join(root, name)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        docs.append({"path": path, "text": f.read()})
                except Exception:
                    pass
    return docs

if __name__ == "__main__":
    docs = load_files(REPO_PATH)
    print(f"Loaded {len(docs)} files")
    for d in docs[:10]:
        print(d["path"])