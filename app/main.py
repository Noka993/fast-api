from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg


app = FastAPI()


class Post(BaseModel):
    title: str  # Type checking and validation
    content: str
    published: bool = True  # Default value
    rating: Optional[int] = None

try:
    conn = psycopg.connect("host=localhost port=5432 dbname=fastapi user=postgres password=admin123")
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as e:
    print("Database connection was failed!")
    print(e)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello wwdadod!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    # print(new_post)
    # print(new_post.model_dump()) # dict
    post_dict = new_post.model_dump()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"data": post}

@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    my_posts.pop(index)
    return {"message": "post was deleted"}

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    post_dict = updated_post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}