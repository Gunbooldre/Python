from fastapi import FastAPI
from fastapi.params import Body

from schema import Post

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": "Here your posts"}


@app.post("/createposts")
def create_post(data: Post):
    print(f"new Post {data}")
    return {"New post": "New post"}
