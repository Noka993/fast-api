from fastapi import FastAPI
import psycopg
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello wwdadod!"}
