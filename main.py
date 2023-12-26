from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

def find_post(id):
    for elem in my_posts:
        if elem["id"] == id: 
            return elem


# My variant
# def find_post_index(id):
#     i = 0
#     for elem in my_posts:
#         if elem["id"] == id:
#             return i
#         i +=1

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump() # dic() method is deprecated
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return  {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}
    

# fastapi will run the code of the first route match, meaning /posts/latest 
# should be declared before /posts/{id} otherwise /posts/{id} section will match a GET /posts/latest, where {id} == "latest"

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index = find_post_index(id)
    
    if post_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
    
    my_posts.pop(post_index)
    print(my_posts)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


