from loader import load_files, REPO_PATH
from chunker2 import chunk_smart
from search import build_index
from eval import hit_rate

chunks = chunk_smart(load_files(REPO_PATH))
print(len(chunks), "smart chunks")
build_index(chunks, name="smart")
hit_rate("smart")