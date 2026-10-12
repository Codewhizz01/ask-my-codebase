import re, os

MAX_LINES = 60
MIN_LINES = 8
JS_START = re.compile(r"^(async\s+function|function|const\s+\w+\s*=\s*(async\s*)?\(|exports\.|module\.exports|router\.|app\.|class\s)")
MD_START = re.compile(r"^#{1,4}\s")

def blocks_with_start(lines, is_start):
    blocks, cur, start = [], [], 0
    for i, line in enumerate(lines):
        if is_start(line) and cur:
            blocks.append((start, cur))
            cur, start = [], i
        cur.append(line)
    if cur:
        blocks.append((start, cur))
    return blocks

def chunk_smart(docs):
    chunks = []
    for d in docs:
        ext = os.path.splitext(d["path"])[1]
        lines = d["text"].splitlines()
        if ext in (".js", ".ts"):
            blocks = blocks_with_start(lines, lambda l: bool(JS_START.match(l)))
        elif ext == ".md":
            blocks = blocks_with_start(lines, lambda l: bool(MD_START.match(l)))
        else:
            blocks = [(0, lines)]
        merged = []
        for start, blk in blocks:
            if merged and len(blk) < MIN_LINES and len(merged[-1][1]) + len(blk) <= MAX_LINES:
                merged[-1] = (merged[-1][0], merged[-1][1] + blk)
            else:
                merged.append((start, blk))
        name = os.path.basename(d["path"])
        for start, blk in merged:
            for off in range(0, len(blk), MAX_LINES):
                piece = blk[off:off + MAX_LINES]
                body = "\n".join(piece).strip()
                if not body:
                    continue
                s = start + off + 1
                chunks.append({
                    "path": d["path"],
                    "start_line": s,
                    "end_line": s + len(piece) - 1,
                    "text": f"File: {name}\n{body}",
                })
    return chunks
