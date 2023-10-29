from fastapi import FastAPI
from typing import List
from schemas.user_schema import User
from routers.user_routes import users_routers
from routers.blog_routes import blog_post_router, articles

app = FastAPI()

app.include_router(users_routers, prefix="/users", tags=["Users"])
app.include_router(blog_post_router, prefix="/blog_post", tags=["Blog Posts"])



@app.get("/")
def home():
    return{"message": "Welcome to my Blog App. We'll add more features shortly..", "blog_posts" :articles}

