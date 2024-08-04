from fastapi import APIRouter, HTTPException, Request
from models import Blog, BlogReturn, Search, BlogDocumentReturn
from connector import query_handler, sql_search

router = APIRouter(
    prefix="/api/blog", tags=["blog"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[BlogReturn])
async def get_blogs(req: Request):
    query = "SELECT * FROM blogs;"
    rsp = await query_handler(req.app.state.db, query, 404, "No resources")
    return [BlogReturn(**dict(blog)) for blog in rsp]


@router.post("/", response_model=BlogReturn)
async def create_blog(blog: Blog):
    query = (
        f"INSERT INTO blogs(title, creator_id)"
        f"VALUES ('{blog.title}', '{blog.creator_id}', '{user.email}')"
        "RETURNING blog_id, title, created_date, last_post_date;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to create blog")
    return BlogReturn(**rsp[0])


@router.post("/search", response_model=list[BlogReturn])
async def search_blogs(search: Search, req: Request):
    fmt_search = sql_search(search.query)
    query = (
        "SELECT * FROM blogs"
        f"WHERE to_tsvector('english', title) @@ to_tsquery('english', '{fmt_search}' );"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "No results")
    return [BlogReturn(**blog) for blog in rsp]


@router.get("/{blog_id}", response_model=BlogReturn)
async def get_blog(blog_id: str, req: Request):
    query = f"SELECT * FROM blogs WHERE blog_id = '{blog_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "Blog does not exist")
    return BlogReturn(**rsp[0])


@router.put("/{blog_id}", response_model=BlogReturn)
async def update_blog(blog_id: str, blog: Blog, req: Request):
    query = f"SELECT * FROM blogs WHERE blog_id = '{blog_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "Blog does not exist")
    update_values = ", ".join(
        ["%s = '%s'" % (k, v) for (k, v) in blog.__dict__.items()]
    )
    query = (
        f"UPDATE users SET {update_values} WHERE blog_id = '{blog_id}'"
        "RETURNING blog_id, title, created_date, last_post_date;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "unable to upate resource")
    return BlogReturn(**rsp[0])


@router.get("/{blog_id}/documents", response_model=BlogDocumentReturn)
async def get_blog_documents(blog_id: str, req: Request):
    query = f"SELECT * FROM get_blog_documents WHERE blog_id = '{blog_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "No comments found")
    return [BlogDocumentReturn(**doc) for doc in rsp]


@router.post("/{blog_id}/search", response_model=list[BlogDocumentReturn])
async def search_blog_documents(blog_id: str, search: Search, req: Request):
    fmt_search = sql_search(search.query)
    query = (
        "SELECT * FROM blog_documents"
        f"WHERE blog_id = '{blog_id}' AND "
        f"WHERE to_tsvector(title || ' ' || content) @@ to_tsquery('{fmt_search}');"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "No results")
    return [BlogDocumentReturn(**doc) for doc in rsp]
