from fastapi import APIRouter, Form, HTTPException, status
from schemas.blog_post_schema import BlogPostBase, BlogRequestBody, CreateBlogPost, EditBlogPost
from datetime import datetime
from uuid import UUID, uuid4
from routers.user_routes import get_username_from_token


blog_post_router = APIRouter()


articles = [
    CreateBlogPost(
        title= "Ade goes to sch", 
        body= "We shall be discussing the adventures of ade as he goes", 
        author= "ohiri the man", 
        created_at = datetime.now(),
        id=uuid4()),
    CreateBlogPost(
        title= "Ola goes to sch", 
        body= "We shall be discussing the adventures of ola as he goes", 
        author= "Paul the man", 
        created_at=datetime.now(),
        id=uuid4())
    ]


def get_post_by_id(id: str):
    for post in articles:
        print(post)
        if str(post.id) == id:
            return post
    return False


@blog_post_router.get("/",  status_code=200)
def get_all_blog_posts():
    return articles

@blog_post_router.get("/{id}", status_code=200)
def get_blog_post_by_id(id: str):
    post = get_post_by_id(id)
    if post != False:
        return post
    return{"error": "Post not found"}

#create a new blog post
@blog_post_router.post("/posts", status_code=201)
def create_blog_post(post: BlogRequestBody, token: str):
    #get user id
    #check if user exist, if not throw error
    #if user exist, create blog
    author = get_username_from_token(token)
    if author == False :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized. Please login")
    
    new_post = CreateBlogPost(id=str(UUID(int=len(articles) +1)), created_at=datetime.now(), published=True, author=author, **post.model_dump()) #Next task is to assigned author to user.id gotten from user route


    articles.append(new_post)
    return {"message": "Your Post has been sent!", "Title": new_post.title}


#Edit an existing blog post.
@blog_post_router.put("/posts/{id}", status_code=201)
def update_blog_post(id: str, update_post: BlogRequestBody, token: str):
    author = get_username_from_token(token)
    if author == False :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized. Please login")

    post = get_post_by_id(id)
    if post == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found!")

    print(post)
    if author != post.author:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your post bro"
        )
    post.title = update_post.title
    post.body = update_post.body
    

    return{"message": "Article Updated succesfully"}


#Delete a blog post
@blog_post_router.delete("/posts/{id}", status_code=200)
        #get user id
    #check if user exist, if not throw error
    #if user exist, create blog
def delete_post(id: str):
    blog_post = get_blog_post_by_id(id)
    if not blog_post:
        raise HTTPException(
            status_code=404, detail="Book not found"
        )
    
    post_index = None

    for i, post in enumerate(articles):
        if post.id == id:
            post_index = i
            break
    
    articles.pop(post_index)
    return {"message": "Post deleted succesfully!"}