from fastapi import APIRouter, HTTPException, Request
from models import Blog, BlogReturn

router = APIRouter(
    prefix="/api/blog", tags=["blog"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[BlogReturn])
async def get_blogs(req: Request):
    rsp = await req.app.state.db.fetch_rows("SELECT * FROM blogs;")
    return [BlogReturn(**dict(blog)) for blog in rsp]


@router.post("/", response_model=Blog)
async def create_blog():
    return Blog


@router.get("/{blog_id}", response_model=BlogReturn)
async def get_blog(blog_id: str, req: Request):
    query = f"SELECT * FROM blogs WHERE blog_id = '{blog_id}'"
    rsp = await req.app.state.db.fetch_rows(query)
    if not rsp:
        raise HTTPException(status_code=404, detail="Blog does not exist")
    return BlogReturn(**rsp[0])


@router.put("/{blog_id}", response_model=Blog)
async def update_blog():
    return Blog
