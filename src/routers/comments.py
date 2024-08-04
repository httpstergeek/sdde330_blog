from fastapi import APIRouter, HTTPException, Request
from models import Comment, CommentReturn

router = APIRouter(
    prefix="/api/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Comment)
async def create_comment(req: Request):
    query = "SELECT * FROM comments;"
    rsp = await query_handler(req.app.state.db, query, 404, "No resources")
    return [CommentReturn(**dict(document)) for document in rsp]


@router.post("/", response_model=CommentReturn)
async def get_comment(comment: Comment, req: Request):
    query = (
        f"INSERT INTO comments (content, author_id, document_id)"
        f"VALUES ('{comment.title}', '{comment.content}', '{comment.document_id}')"
        "RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to create document")
    return CommentReturn(**rsp[0])


@router.delete("/{comment_id}", response_model=CommentReturn)
async def delete_comment(comment_id: str, req: Request):
    query = f"DELETE FROM commments WHERE comment_id = '{comment_id}' RETURNING *;"
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to delete document")
    return CommentReturn(**rsp[0])
