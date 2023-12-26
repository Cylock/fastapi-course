from random import randrange
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id: int):
    for elem in my_posts:
        if elem["id"] == id: 
            return elem


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump() # dic() method is deprecated
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return  {"data": post_dict}

@app.get("/posts/{id}")
def get_post_by_id(id):
    post = find_post(int(id))
    return post