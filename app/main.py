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



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id_number": 1},
            {"title": "favorite foods", "content": "I like pizza", "id_number": 2}]

def find_post(id_number):
    for elem in my_posts:
        if elem["id_number"] == id_number: 
            return elem


# My variant
# def find_post_index(id_number):
#     i = 0
#     for elem in my_posts:
#         if elem["id_number"] == id_number:
#             return i
#         i +=1


def find_post_index(id_number):
    """Iterate through my_posts array and retrieve post based on input id"""   
    for i,p in enumerate(my_posts):
        if p["id_number"] == id_number:
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
    post_dict['id_number'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return  {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}
    

# fastapi will run the code of the first route match, meaning /posts/latest 
# should be declared before /posts/{id_number} otherwise /posts/{id_number} section will match a GET /posts/latest, where {id_number} == "latest"

@app.get("/posts/{id_number}")
def get_post(id_number: int, response: Response):
    post = find_post(id_number)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id_number: {id_number} was not found")
    return post


@app.delete("/posts/{id_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_number: int):
    post_index = find_post_index(id_number)

    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id_number} not found")
    
    my_posts.pop(post_index)
    print(my_posts)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id_number}")
def update_post(id_number:int, post: Post):

    post_index = find_post_index(id_number)

    if post_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id_number} not found")

    post_dict = post.model_dump()
    post_dict['id_number'] = id_number
    my_posts[post_index] = post_dict
    return {"data": post_dict}