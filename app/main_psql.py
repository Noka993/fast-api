from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
import psycopg
import time


app = FastAPI()


class Post(BaseModel):
    title: str  # Type checking and validation
    content: str
    published: bool = True  # Default value
    rating: Optional[int] = None


while True:
    try:
        conn = psycopg.connect(
            """host=localhost port=5432 
            dbname=fastapi user=postgres password=admin123""",
            row_factory=psycopg.rows.dict_row,
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as e:
        print("Database connection was failed!")
        print(e)
        time.sleep(2)

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
    posts = cursor.execute("""SELECT * FROM posts""").fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    # print(new_post)
    # print(new_post.model_dump()) # dict
    # post_dict = new_post.model_dump()
    # post_dict["id"] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    cursor.execute(
        """
        INSERT INTO posts (title, content, published) 
        VALUES (%s, %s, %s) RETURNING *""",
        (new_post.title, new_post.content, new_post.published),
    )
    conn.commit()
    return {"data": "created post"}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        """
        SELECT * FROM posts WHERE id = %s
        """,
        (str(id),),
    )
    post = cursor.fetchone()
    # print(test_post)
    # post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    #   response.status_code = status.HTTP_404_NOT_FOUND
    #   return {"message": f"post with id: {id} was not found"}
    return {"data": post}


@app.delete("/posts/{id}")
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT):
    cursor.execute(
        """
        DELETE FROM posts WHERE id = %s RETURNING id
        """,
        (str(id),),
    )
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """
        UPDATE posts SET title = %s, content = %s, published = %s
        WHERE id = %s RETURNING *
        """,
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"data": updated_post}
