from fastapi import APIRouter, HTTPException, Request
from models import User, UserReturn, CommentReturn, BlogDocumentReturn, BlogReturn
from connector import query_handler

router = APIRouter(
    prefix="/api/user", tags=["users"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[UserReturn])
async def get_users(req: Request):
    query = "SELECT * FROM USERS;"
    rsp = await query_handler(req.app.state.db, query, 404, "No resources")
    return [UserReturn(**dict(user)) for user in rsp]


@router.post("/", response_model=UserReturn)
async def create_user(user: User, req: Request):
    query = f"Select * from Users where username='{user.username}';"
    rsp = await req.app.state.db.fetch_rows(query)
    if rsp:
        raise HTTPException(status_code=404, detail="username already exists")
    query = (
        f"INSERT INTO users(username, bio, email)"
        f"VALUES ('{user.username}', '{user.bio}', '{user.email}')"
        "RETURNING username, bio, email, user_id, created_date, last_post_date;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "Failed to create user")
    return UserReturn(**rsp[0])


@router.get("/{user_id}", response_model=UserReturn)
async def get_user_details(user_id: str, req: Request):
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "username does not exists")
    return UserReturn(**rsp[0])


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User, req: Request):
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "username does not exists")
    current_user = User(**rsp[0])
    if current_user.username != user.username:
        query = f"Select * from Users where username='{user.username}';"
        rsp = await req.app.state.db.fetch_rows(query)
        if rsp:
            raise HTTPException(status_code=404, detail="username taken")
    update_values = ", ".join(
        ["%s = '%s'" % (k, v) for (k, v) in user.__dict__.items()]
    )
    query = (
        f"UPDATE users SET {update_values} WHERE user_id = '{user_id}'"
        "RETURNING username, bio, email, user_id, created_date, last_post_date;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "Failed to update user")
    return User(**rsp[0])


@router.get("/{user_id}/comments", response_model=list[CommentReturn])
async def get_user_comments(user_id: str, req: Request):
    query = f"SELECT * FROM comments WHERE author_id = '{user_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "No comments found")
    return [CommentReturn(**comment) for comment in rsp]


@router.get("/{user_id}/documents", response_model=list[BlogDocumentReturn])
async def get_user_documents(user_id: str, req: Request):
    query = f"SELECT * FROM blog_documents WHERE author_id = '{user_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "No documents found")
    return [BlogDocumentReturn(**document) for document in rsp]


@router.get("/{user_id}/blogs", response_model=list[BlogReturn])
async def get_user_blog_spaces(user_id: str, req: Request):
    query = f"SELECT * FROM blogs WHERE creator_id = '{user_id}'"
    rsp = await req.app.state.db.fetch_rows(query)
    print(rsp)
    return [BlogReturn(**blog) for blog in rsp]
