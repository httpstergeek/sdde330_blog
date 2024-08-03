from fastapi import APIRouter, HTTPException
from ..models import Comment

router = APIRouter(
    prefix="/api/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Comment)
async def create_comment():
    return {}


@router.get("/{comment_id}", response_model=Comments)
async def get_comment():
    return {}


@router.delete("/{comment_id}", response_model=Comments)
async def get_comment():
    return {}


@router.post("/search", response_model=Comment)
async def create_comment():
    return {}
