from fastapi import FastAPI
from random import randrange
from schema import Post

app = FastAPI()
my_posts = [{"title": "titile of post1 ", "body": "Body of posts 1", "id": 1},
            {"title": "titile of post2 ", "body": "Body of posts 2", "id": 2}]


def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/createposts")
def create_post(data: Post):
    data = data.dict()
    data['id'] = randrange(0, 100000)
    my_posts.append(data)
    return {"New post": data}


@app.get('/posts/{id}')
def get_post(id: int):
    data = find_post(int(id))
    return ({"post_detail": data})