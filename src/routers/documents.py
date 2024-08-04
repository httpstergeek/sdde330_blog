from fastapi import APIRouter, Request
from models import BlogDocument, BlogDocumentReturn, Search, Comment, CommentReturn
from connector import query_handler, sql_search

router = APIRouter(
    prefix="/api/document",
    tags=["document"],
    responses={404: {"description": "Not found"}},
)

META = {}


@router.get("/", response_model=list[BlogDocumentReturn])
async def get_documents(req: Request):
    query = "SELECT * FROM blog_documents;"
    rsp = await query_handler(req.app.state.db, query, 404, "No resources")
    return [BlogDocumentReturn(**dict(document)) for document in rsp]


@router.post("/", response_model=BlogDocumentReturn)
async def create_document(doc: BlogDocument, req: Request):
    query = (
        f"INSERT INTO blog_documents (title, content, author_id, blog_id)"
        f"VALUES ('{doc.title}', '{doc.content}', '{doc.author_id}', '{doc.blog_id}')"
        "RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to create document")
    return BlogDocumentReturn(**rsp[0])


@router.post("/search", response_model=list[BlogDocumentReturn])
async def search_documents(search: Search, req: Request):
    fmt_search = sql_search(search.query)
    query = (
        "SELECT * FROM blog_documents "
        f"WHERE to_tsvector(title || ' ' || content) @@ to_tsquery('{fmt_search}');"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "No results")
    return BlogDocumentReturn(**rsp[0])


@router.get("/{document_id}", response_model=BlogDocument)
async def get_document(document_id: str, req: Request):
    query = f"SELECT * FROM blogs_documents WHERE document_id = '{document_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "Document does not exist")
    return BlogDcoumentReturn(**rsp[0])


@router.get("/{document_id}/comments", response_model=CommentReturn)
async def get_document_comments(document_id: str, req: Request):
    query = f"SELECT * FROM comments WHERE document_id = '{document_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "No comments found")
    return [CommentReturn(**comment) for comment in rsp]


@router.put("/{document_id}", response_model=BlogDocumentReturn)
async def update_document(doc: BlogDocument, req: Request):
    query = f"SELECT * FROM blogs_documents WHERE document_id = '{document_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "Blog does not exist")
    update_values = ", ".join(["%s = '%s'" % (k, v) for (k, v) in doc.__dict__.items()])
    query = (
        f"UPDATE users SET {update_values} WHERE document_id = '{document_id}'"
        "RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "unable to upate resource")
    return BlogDocumentReturn(**rsp[0])


@router.delete("/{document_id}", response_model=BlogDocumentReturn)
async def update_document(document_id: str, req: Request):
    query = f"DELETE FROM comments WHERE document_id = '{document_id}' RETURNING *;"
    await req.app.state.db.fetch_rows(query)
    query = (
        f"DELETE FROM blogs_documents WHERE document_id = '{document_id}' RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "Unable to delete document")
    return BlogDocumentReturn(**rsp[0])


@router.post("/{document_id}/search", response_model=list[CommentReturn])
async def search_blog_docs(blog_id: str, search: Search, req: Request):
    fmt_search = sql_search(search.query)
    query = (
        "SELECT * FROM blog_documents"
        f"WHERE blog_id = '{blog_id}' AND "
        f"WHERE to_tsvector(title || ' ' || content) @@ to_tsquery('{fmt_search}');"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "No results")
    return [BlogDocumentReturn(**doc) for doc in rsp]
