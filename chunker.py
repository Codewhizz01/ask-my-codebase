from loader import load_files, REPO_PATH

CHUNK_LINES = 30   # lines per chunk
OVERLAP = 5        # lines shared between neighbouring chunks

def chunk_naive(docs):
    chunks = []
    for d in docs:
        lines = d["text"].splitlines()
        step = CHUNK_LINES - OVERLAP
        for start in range(0, max(len(lines), 1), step):
            piece = lines[start:start + CHUNK_LINES]
            text = "\n".join(piece).strip()
            if not text:
                continue
            chunks.append({
                "path": d["path"],
                "start_line": start + 1,
                "end_line": start + len(piece),
                "text": text,
            })
    return chunks

if __name__ == "__main__":
    docs = load_files(REPO_PATH)
    chunks = chunk_naive(docs)
    print(f"{len(docs)} files -> {len(chunks)} chunks")
    c = chunks[3]
    print(f"\nSample: {c['path']} (lines {c['start_line']}-{c['end_line']})")
    print(c["text"][:400])