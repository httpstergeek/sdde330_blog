from fastapi import APIRouter, HTTPException, Request
from models import Blog, BlogReturn, Search, BlogDocumentReturn
from connector import query_handler, sql_search

tag = {
    "name": "blog",
    "description": (
        "This resource repersents Blog Spaces. Use it to get, crate,  find.",
        "Blog Spaces are not indented to be deleted.",
    ),
}

router = APIRouter(
    prefix="/api/blog", tags=["blog"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[BlogReturn])
async def get_blogs(req: Request):
    """
    Retrieves all blog spaces
    """
    query = "SELECT * FROM blogs;"
    try:
        rsp = await query_handler(req.app.state.db, query, 404, "No resources")
    except HTTPException as e:
        req.app.log.warning(e)
    req.app.log.info("Geting all blog spaces")
    return [BlogReturn(**dict(blog)) for blog in rsp]


@router.post("/", response_model=BlogReturn)
async def create_blog(blog: Blog, req: Request):
    """
    Create blog space
    """
    query = (
        f"INSERT INTO blogs(title, creator_id) "
        f"VALUES ('{blog.title}', '{blog.creator_id}') "
        "RETURNING *;"
    )
    req.app.log.info(f"Creating blog  {blog.title}")
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to create blog")
    return BlogReturn(**rsp[0])


@router.post("/search", response_model=list[BlogReturn])
async def search_blogs(search: Search, req: Request):
    """
    Search all blogs by title using key words
    """
    fmt_search = sql_search(search.query)
    query = (
        "SELECT * FROM blogs "
        f"WHERE to_tsvector(title) @@ to_tsquery('english', '{fmt_search}');"
    )
    req.app.log.info(f"searching blog using {fmt_search}")
    rsp = await query_handler(req.app.state.db, query, 404, "No results")
    return [BlogReturn(**blog) for blog in rsp]


@router.get("/{blog_id}", response_model=BlogReturn)
async def get_blog(blog_id: str, req: Request):
    """
    Retrives blog space by id
    """
    query = f"SELECT * FROM blogs WHERE blog_id = '{blog_id}'"
    rsp = await query_handler(
        req.app.state.db, query, 404, f"Blog: {blog_id} does not exist"
    )
    req.app.log.info(f"retrieving blog {blog_id}")
    return BlogReturn(**rsp[0])


@router.put("/{blog_id}", response_model=BlogReturn)
async def update_blog(blog_id: str, blog: Blog, req: Request):
    """
    updates blog information title and Creator
    """
    query = f"SELECT * FROM blogs WHERE blog_id = '{blog_id}'"
    rsp = await query_handler(
        req.app.state.db, query, 404, f"Blog: {blog_id} does not exist"
    )
    update_values = ", ".join(
        ["%s = '%s'" % (k, v) for (k, v) in blog.__dict__.items()]
    )
    query = (
        f"UPDATE blogs SET {update_values} WHERE blog_id = '{blog_id}' " "RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "unable to upate resource")
    req.app.log.info(f"updating blog {blog_id}")
    return BlogReturn(**rsp[0])


@router.get("/{blog_id}/documents", response_model=list[BlogDocumentReturn])
async def get_blog_documents(blog_id: str, req: Request):
    """
    retreives all documents associated with blog spaces.
    """
    query = f"SELECT * FROM blog_documents WHERE blog_id = '{blog_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "No comments found")
    req.app.log.info(f"retieving blog documents for blog {blog_id}")
    return [BlogDocumentReturn(**doc) for doc in rsp]


@router.post("/{blog_id}/search", response_model=list[BlogDocumentReturn])
async def search_blog_documents(blog_id: str, search: Search, req: Request):
    """
    retrieves all documents assocated with blog based on query.
    Query search for all keywords in query using 'AND' logic.
    """
    fmt_search = sql_search(search.query)
    query = (
        "SELECT * FROM blog_documents "
        f"WHERE blog_id = '{blog_id}' AND "
        f"to_tsvector(title || ' ' || content) @@ to_tsquery('english', '{fmt_search}');"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "No results")
    req.app.log.info(f"searching blog documents for blog {blog_id}")
    return [BlogDocumentReturn(**doc) for doc in rsp]
