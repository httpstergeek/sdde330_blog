from fastapi import APIRouter, Request
from models import BlogDocument, BlogDocumentReturn, Search, Comment, CommentReturn
from connector import query_handler, sql_search

router = APIRouter(
    prefix="/api/document",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[BlogDocumentReturn])
async def get_documents(req: Request):
    """
    Retrieves all documents
    """
    query = "SELECT * FROM blog_documents;"
    rsp = await query_handler(req.app.state.db, query, 404, "No resources")
    req.app.log.info(f"Retriving blog documents")
    return [BlogDocumentReturn(**dict(document)) for document in rsp]


@router.post("/", response_model=BlogDocumentReturn)
async def create_document(doc: BlogDocument, req: Request):
    """
    Create blog documents
    """
    print(doc)
    query = (
        f"INSERT INTO blog_documents (title, content, author_id, blog_id)"
        f"VALUES ('{doc.title}', '{doc.content}', '{doc.author_id}', '{doc.blog_id}')"
        "RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to create document")
    req.app.log.info(f"Creating blog document")
    return BlogDocumentReturn(**rsp[0])


@router.post("/search", response_model=list[BlogDocumentReturn])
async def search_documents(search: Search, req: Request):
    """
    Search All documents based on query.  String is split on spaces.
    Document must contain all keywords.
    """
    fmt_search = sql_search(search.query)
    query = (
        "SELECT * FROM blog_documents "
        f"WHERE to_tsvector(title || ' ' || content) @@ to_tsquery('{fmt_search}');"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "No results")
    req.app.log.info(f"searching blog documents {fmt_search}")
    return [BlogDocumentReturn(**doc) for doc in rsp]


@router.get("/{document_id}", response_model=BlogDocument)
async def get_document_details(document_id: str, req: Request):
    """
    Retrieve blog document details
    """
    query = f"SELECT * FROM blog_documents WHERE document_id = '{document_id}';"
    rsp = await query_handler(req.app.state.db, query, 404, "Document does not exist")
    req.app.log.info(f"retrieving blog document {document_id}")
    return BlogDocumentReturn(**rsp[0])


@router.get("/{document_id}/comments", response_model=list[CommentReturn])
async def get_document_comments(document_id: str, req: Request):
    """
    Retieve all comments assocaited with blog document.
    """
    query = f"SELECT * FROM comments WHERE document_id = '{document_id}';"
    rsp = await query_handler(req.app.state.db, query, 404, "No comments found")
    req.app.log.info(f"retrieving comments document {document_id}")
    return [CommentReturn(**comment) for comment in rsp]


@router.put("/{document_id}", response_model=BlogDocumentReturn)
async def update_document(document_id: str, doc: BlogDocument, req: Request):
    """
    Update blog documents
    """
    query = f"SELECT * FROM blogs_documents WHERE document_id = '{document_id}'"
    rsp = await query_handler(req.app.state.db, query, 404, "Blog does not exist")
    update_values = ", ".join(["%s = '%s'" % (k, v) for (k, v) in doc.__dict__.items()])
    query = (
        f"UPDATE blog_docouments SET {update_values} WHERE document_id = '{document_id}'"
        "RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "unable to upate resource")
    req.app.log.info(f"updating document {document_id}")
    return BlogDocumentReturn(**rsp[0])


@router.delete("/{document_id}", response_model=BlogDocumentReturn)
async def update_document(document_id: str, req: Request):
    """
    Deletes blog documment and all assocaited comments
    """
    query = f"DELETE FROM comments WHERE document_id = '{document_id}' RETURNING *;"
    await req.app.state.db.fetch_rows(query)
    query = (
        f"DELETE FROM blog_documents WHERE document_id = '{document_id}' RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 404, "Unable to delete document")
    req.app.log.info(f"deleting blog document {document_id}")
    return BlogDocumentReturn(**rsp[0])
