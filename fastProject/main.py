from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": "Here your posts"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"New post": f"Title {payload['title']}, body {payload['body']}"}
