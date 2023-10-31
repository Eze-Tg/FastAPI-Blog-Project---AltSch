from fastapi import APIRouter, HTTPException
from schemas.blog_post_schema import BlogPostBase, CreateBlogPost, EditBlogPost
from datetime import datetime
from uuid import UUID, uuid4


blog_post_router = APIRouter()


articles = [
    # CreateBlogPost(title= "Ade goes to sch", 
    #                body= "We shall be discussing the adventures of ade as he goes", 
    #                author= "ohiri the man", 
    #                created_at = datetime.now()),
    # CreateBlogPost(title= "Ola goes to sch", 
    #                body= "We shall be discussing the adventures of ola as he goes", 
    #                author= "Paul the man", created_at=datetime.now())
    ]


def get_post_by_id(id: str):
    for post in articles:
        if post.id == id:
              return post
        return{"message": f"No post with id {id}"}


@blog_post_router.get("/",  status_code=200)
def get_all_blog_posts():
    return articles

@blog_post_router.get("/{id}", status_code=200)
def get_blog_post_by_id(id: str):
    post = get_post_by_id(id)
    if post:
        return post
    return{"error": "Post not found"}

#create a new blog post
@blog_post_router.post("/posts", status_code=201)
def create_blog_post(post: BlogPostBase):
    # post.title = title
    # post.body = body
    # post.author = author

    new_post = CreateBlogPost(id=str(UUID(int=len(articles) +1)), 
                              **post.dict())


    articles.append(new_post)
    return {"message": "Your Post has been sent!", "Title": new_post.title}


#Edit an existing blog post.
@blog_post_router.put("/posts/{id}", status_code=201)
def update_blog_post(id: str, update_post: EditBlogPost):
    post = get_blog_post_by_id(id)
    if not post:
        return{"error": "No article with that ID!!"}
    
    post.title = update_post.title
    post.body = update_post.body
    post.author = update_post.author
    

    return{"message": "Article Updated succesfully"}


#Delete a blog post
@blog_post_router.delete("/posts/{id}", status_code=200)
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