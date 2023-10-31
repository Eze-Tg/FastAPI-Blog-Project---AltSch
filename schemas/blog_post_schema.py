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
    id: Optional[UUID] = uuid4()


class EditBlogPost(BlogPostBase):
    pass


class Responce(BlogPostBase):
    pass

