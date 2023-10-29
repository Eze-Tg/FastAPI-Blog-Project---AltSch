from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class BlogPostBase(BaseModel):
    title: str
    body: str
    author: str
    published : bool = True
    created_at: datetime


class CreateBlogPost(BlogPostBase):
    id: str


class EditBlogPost(BlogPostBase):
    pass
