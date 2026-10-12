import chromadb
import os
import re
from sentence_transformers import SentenceTransformer
from loader import load_files, REPO_PATH
from chunker import chunk_naive

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")

def build_index(chunks, name="naive"):
    try:
        client.delete_collection(name)
    except Exception:
        pass
    col = client.create_collection(name)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, batch_size=16, show_progress_bar=True).tolist()
    col.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"path": c["path"], "start_line": c["start_line"],
                    "end_line": c["end_line"]} for c in chunks],
    )
    return col

def search(question, name="naive", k=5):
    col = client.get_collection(name)
    emb = model.encode([question]).tolist()
    res = col.query(query_embeddings=emb, n_results=k)
    return list(zip(res["metadatas"][0], res["documents"][0]))

def search_capped(question, name="smart", k=5, fetch=15, max_md=1):
    results = search(question, name=name, k=fetch)
    out, md = [], 0
    for meta, doc in results:
        if meta["path"].lower().endswith(".md"):
            if md >= max_md:
                continue
            md += 1
        out.append((meta, doc))
        if len(out) == k:
            break
    return out

STOP = {"the", "a", "an", "is", "are", "how", "where", "what", "which", "does",
        "do", "to", "of", "in", "and", "for", "on", "it", "work", "works"}

def _split_camel(text):
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

def _tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def search_hybrid(question, name="smart", k=5, fetch=15, max_md=1):
    # 1) meaning-based results (embeddings)
    emb = search(question, name=name, k=fetch)

    # 2) keyword-based results, with a bonus for matching the file name
    col = client.get_collection(name)
    data = col.get()
    q = _tokens(question) - STOP
    kw = []
    for doc, meta in zip(data["documents"], data["metadatas"]):
        fname = _tokens(_split_camel(os.path.basename(meta["path"])))
        score = len(q & _tokens(_split_camel(doc))) + 3 * len(q & fname)
        if score > 0:
            kw.append((score, meta, doc))
    kw.sort(key=lambda x: -x[0])
    kw = kw[:fetch]

    # 3) merge both rankings (reciprocal rank fusion)
    def key(m):
        return (m["path"], m["start_line"])
    fused = {}
    for rank, (meta, doc) in enumerate(emb):
        fused.setdefault(key(meta), [0, meta, doc])[0] += 1 / (60 + rank)
    for rank, (score, meta, doc) in enumerate(kw):
        fused.setdefault(key(meta), [0, meta, doc])[0] += 1 / (60 + rank)
    ranked = sorted(fused.values(), key=lambda x: -x[0])

    # 4) same README cap as before
    out, md = [], 0
    for _, meta, doc in ranked:
        if meta["path"].lower().endswith(".md"):
            if md >= max_md:
                continue
            md += 1
        out.append((meta, doc))
        if len(out) == k:
            break
    return out


if __name__ == "__main__":
    chunks = chunk_naive(load_files(REPO_PATH))
    build_index(chunks)
    print("Index built:", len(chunks), "chunks")
    while True:
        q = input("\nAsk (or 'exit'): ")
        if q.strip().lower() == "exit":
            break
        for meta, doc in search(q):
            print(f"\n{meta['path']} (lines {meta['start_line']}-{meta['end_line']})")
            print(doc[:200])