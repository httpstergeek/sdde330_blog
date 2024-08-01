from fastapi import APIRouter, HTTPException
from ..models import User as User

router = APIRouter(
    prefix="/api/user", tags=["user"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[User])
async def get_users():
    return []


@router.post("/{user_id}", response_model=User)
async def get_user():
    return {}


@router.post("/", response_model=User)
async def create_user():
    return {"users": []}
