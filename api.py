import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import search_capped

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","http://127.0.0.1:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def api_search(q:str , k:int =5):
    results=search_capped(q,name="smart",k=k)
    return{
        "question":q,
        "sources":[
            {
                "file":os.path.basename(m["path"]),
                "start_line":m["start_line"],
                "end_line":m["end_line"],
                "text": doc,
            }
            for m, doc in results
        ],
    }