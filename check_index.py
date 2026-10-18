from search import client

col = client.get_collection("smart")
for m in col.get(limit=3)["metadatas"]:
    print(m)