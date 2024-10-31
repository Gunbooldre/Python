from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
from schema import Post
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()
my_posts = [{"title": "titile of post1 ", "body": "Body of posts 1", "id": 1},
            {"title": "titile of post2 ", "body": "Body of posts 2", "id": 2}]

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='123', port="5433",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected succesfully")
        break
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
    cursor.execute(""" SELECT  * FROM posts """)
    post = cursor.fetchall()
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(data: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING 
    * """,
                   (data.title, data.body, data.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get('/posts/{id}')
def get_post(id: str):
    cursor.execute("""SELECT * FROM POSTS WHERE ID = %s """, (str(id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post with id {id} was not found"}
    return {"data": post}


@app.delete('/posts/{id}')
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE ID = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, data: Post):

    cursor.execute("""UPDATE POSTS SET TITLE = %s, CONTENT = %s, PUBLISHED = %s  WHERE ID = %s  RETURNING *""",
                   (data.title, data.body, data.published, str(id)),)
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with ID {id} does not exist ')
    return {"data": updated_post}
