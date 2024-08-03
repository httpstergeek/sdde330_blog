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
    blog_id: UUID
    title: str
    creator_id: UUID
    create_date: datetime
    last_post_date: Union[None, datetime]


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
