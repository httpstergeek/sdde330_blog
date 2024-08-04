from dataclasses import field
from typing import List, Dict, Optional, Union
from uuid import UUID
from pydantic.dataclasses import dataclass
from datetime import datetime


"""
Two similar class for each resource. One for input and output of api.
Classes used to populate swagger api docs.
Need to learn more about about pydantic with optional fields
"""


@dataclass
class Search:
    query: str


@dataclass
class User:
    username: str
    bio: str
    email: str


@dataclass
class UserReturn(User):
    user_id: Optional[UUID]
    created_date: Optional[datetime]
    last_post_date: Optional[datetime]


@dataclass
class Blog:
    title: str
    creator_id: Optional[UUID]


@dataclass
class BlogReturn(Blog):
    blog_id: Optional[UUID]
    title: str
    created_date: Optional[datetime]
    last_post_date: Optional[datetime]


@dataclass
class Content:
    content: str
    author_id: UUID


@dataclass
class BlogDocument(Content):
    title: str
    blog_id: UUID


@dataclass
class BlogDocumentReturn(BlogDocument):
    document_id: UUID
    created_date: datetime
    author_id: UUID
    blog_id: UUID


@dataclass
class Comment(Content):
    document_id: UUID


@dataclass
class CommentReturn(Comment):
    comment_id: UUID
    create_date: datetime
    parent_comment_id: Union[None, UUID]
