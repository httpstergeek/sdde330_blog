from fastapi import APIRouter, HTTPException
from ..models import Blog

router = APIRouter(
    prefix="/api/blog", tags=["blog"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[Blog])
async def get_blogs():
    return []


@router.post("/", response_model=User)
async def create_blog():
    return {}


@router.get("/{blog_id}", response_model=Blog)
async def get_blog():
    return {}


@router.put("/{blog_id}", response_model=Blog)
async def update_blog():
    return {}
