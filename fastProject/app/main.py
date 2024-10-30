from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
from schema import Post
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()
my_posts = [{"title": "titile of post1 ", "body": "Body of posts 1", "id": 1},
            {"title": "titile of post2 ", "body": "Body of posts 2", "id": 2}]


try:
    conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='123', port="5433",
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connected succesfully")
except Exception as e:
    print("Connection to database failed")
    print(f"Errors {e}")

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i


def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_post(data: Post):
    data = data.dict()
    data['id'] = randrange(0, 100000)
    my_posts.append(data)
    return {"New post": data}


@app.get('/posts/{id}')
def get_post(id: int):
    data = find_post(int(id))
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post with id {id} was not found"}
    return {"data": data}


@app.delete('/posts/{id}')
def delete_post(id: int):
    index = find_index(int(id))
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, data: Post):
    index = find_index(int(id))
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')
    data = data.dict()
    data['id'] = id
    my_posts[index] = data
    return Response(status_code=status.HTTP_200_OK)