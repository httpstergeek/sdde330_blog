from fastapi import APIRouter, HTTPException, Request
from models import User, UserReturn
from typing import Dict, Any

router = APIRouter(
    prefix="/api/user", tags=["user"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[UserReturn])
async def get_users(req: Request):
    users = await req.app.state.db.fetch_rows("SELECT * FROM USERS;")
    return [UserReturn(**dict(user)) for user in users]


@router.post("/", response_model=UserReturn)
async def create_user(user: User, req: Request):
    query = f"Select * from Users where username='{user.username}';"
    user = await req.app.state.db.fetch_rows(query)
    if user:
        raise HTTPException(status_code=404, detail="username already exists")
    query = (
        f"INSERT INTO users(username, bio, email)"
        f"VALUES ('{user.username}', '{user.bio}', '{user.email}')"
        "RETURNING username, bio, email, user_id, created_date, last_post_date;"
    )
    user = await req.app.state.db.fetch_rows(query)
    return UserReturn(**user[0])


@router.get("/{user_id}", response_model=UserReturn)
async def get_user(user_id: str, req: Request):
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    user = await req.app.state.db.fetch_rows(query)
    return UserReturn(**user[0])


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User, req: Request):
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    rsp = await req.app.state.db.fetch_rows(query)
    # Verify user exists
    if not rsp:
        raise HTTPException(status_code=404, detail="username does not exists")
    current_user = User(**rsp[0])
    # Verify user name is not taken
    if current_user.username != user.username:
        query = f"Select * from Users where username='{user.username}';"
        rsp = await req.app.state.db.fetch_rows(query)
        if rsp:
            raise HTTPException(status_code=404, detail="username already exists")
    update_values = ", ".join(
        ["%s = '%s'" % (k, v) for (k, v) in user.__dict__.items()]
    )
    query = (
        f"UPDATE users SET {update_values} WHERE user_id = '{user_id}'"
        "RETURNING username, bio, email, user_id, created_date, last_post_date;"
    )
    rsp = await req.app.state.db.fetch_rows(query)
    return User(**rsp[0])
