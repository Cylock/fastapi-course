from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # using pythons oob syntax `=` for default
    # If I want to add pydantic strict type checking on
    # a field and combine it with a default
    # https://docs.pydantic.dev/2.2/usage/strict_mode/#strict-mode-with-field
    # rating: Optional[int] = Field(default=None,strict=True)


while True:
    try:
        conn = psycopg2.connect(host="db",
                                database="fastapi",
                                user="postgres",
                                password='postgres-admin',
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Database connection was succesful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(5)


# Global variable declaration
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2},
            {"title": "drinks", "content": "I like cola", "id": "sadas"}]


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# Automatically convert to string the comparison element without using pydantics data conversion on id
# def find_post(id):
#     for elem in my_posts:
#         if str(elem["id"]) == id:
#             return elem


@app.get("/")
def read_root():
    return {"message": "This is live reload"}

# def read_root():
#     app.get("/")
#     return {"message:" "This is behaviour without decorator"}


@app.get("/posts")
def get_posts():
    cur.execute("SELECT * FROM posts;")
    all_posts = cur.fetchall()
    print(all_posts)
    return {"data": all_posts}

# Matching routes are evaluated in order, so if there are 2 definitions of the same route (ex. /posts ),
# first match is executed as code

# @app.get("/posts")
# def get_posts():
#     return {"data": "This route is not evaluated"}

# ... = Elipsis - a constant in python which acts as a placeholder


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    # Debug
    # print(post)
    # Convert pydantic model to python dictionary
    # This was my attempt with string interpolation and deciding the post id in the frontend
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0, 1000000)

    # cur.execute(f"""INSERT
    #                 INTO posts (title, content, published)
    #                 VALUES ('{post_dict["title"]}','{post_dict["content"]}',{post_dict["published"]})
    #                 RETURNING *;""")

    # This variant is using query variables instead of a formatted/interpolated string
    # which looks better and less error prone/security (SQL injection)
    cur.execute(""" INSERT
                    INTO posts (title, content, published)
                    VALUES (%s,%s,%s)
                    RETURNING *;""", (post.title, post.content, post.published))
    inserted_row = cur.fetchone()
    conn.commit()
    return {"data": inserted_row}


@app.get("/posts/{post_id}")
# post_id: int <- force pydantic data conversion from str to int of {post_id}
def get_post(post_id: int):
    # Path parameters are returned as string. Cast type to int()

    cur.execute("""SELECT * FROM posts WHERE id = %s ;""", (post_id,))
    post = cur.fetchone()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found, maybe non-existing id")

    # The value of %s must be a string since we have triple quotes otherwise
    # we get "TypeError: 'int' object does not support indexing"
    # So that's why we either retrieve the value from the object with the help
    # of indexes (post_id,) - tuple or [post_id] - array OR by type casting str(post_id)

    return {"data": post}


# @app.get("/posts/latest") <-- error prone because of {post_id} above.
# Position of routes matter in code structure. Parsing is done top-down

# FastApi behaviour with routes
# @app.get("/posts/{post_id}") will also match a GET on "/posts/latest" since
# in this case the variable {post_id} = latest


# @app.get("/posts/{post_id}")
# def get_post(post_id):
#     posts_by_id = {}
#     for elem in my_posts:
#         posts_by_id[elem["id"]] = elem
#     return {"data": posts_by_id[int(post_id)]}


# @app.delete("/posts/{post_id}")
# def delete_post(post_id: int):
#     print(my_posts)
#     # deleting a post
#     for elem in my_posts:
#         if elem["id"] == post_id:
#             my_posts.pop(my_posts.index(elem))
#             return {"Information": f"{elem} was deleted"}
# Receive input id
# Determine index of element which contains this id
# Delete that element from the array based of index and result should be a new array


# A variation with a counter variable

# @app.delete("/posts/{post_id}")
# def delete_post(post_id: int):
#     # print(my_posts)
#     count = 0
#     # deleting a post
#     for elem in my_posts:
#         if elem["id"] == post_id:
#             my_posts.pop(count)
#             count += 1
#             return {"Information": f"{elem} was deleted"}

# Another variation

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):

    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (post_id,))
    post = cur.fetchone()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {post_id} doesn't exist")
    conn.commit()

# My variation for changing each key 1 by 1 if I find the post in my_posts
# @app.put("/posts/{post_id}",status_code=status.HTTP_200_OK)
# def update_post(updated_post: Post, post_id: int):
#     post = find_post(post_id)
#     if post is None:
#         raise HTTPException(status_code=404, detail="Post not found, maybe non-existing id")

#     updated_post = updated_post.model_dump()

#     for key in updated_post:
#         if (key in post) and (updated_post[key] != post[key]):
#             post[key] = updated_post[key]
#         else:
#             continue
#     return post


@app.put("/posts/{post_id}")
def update_post(updated_post: Post, post_id: int):

    cur.execute(""" UPDATE
                posts
                SET title = %s, content = %s, published = %s
                WHERE id = %s
                RETURNING *;""", (updated_post.title, updated_post.content, updated_post.published, post_id))
    updated_row = cur.fetchone()

    if updated_row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {post_id} doesn't exist")

    conn.commit()
    return {"data": updated_row}
