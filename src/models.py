from dataclasses import field
from typing import List, Dict, Optional, Union
from uuid import UUID
from pydantic.dataclasses import dataclass
from datetime import datetime


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
class BlogDocument:
    document_id: UUID
    title: str
    content: str
    create_date: datetime
    author_id: UUID
    blog_id: UUID


@dataclass
class Comment:
    comment_id: UUID
    content: str
    create_date: datetime
    author_id: UUID
    document_id: UUID
    parrent_comment_id: Union[None, UUID]
