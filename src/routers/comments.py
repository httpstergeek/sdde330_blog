from fastapi import APIRouter, HTTPException, Request
from models import Comment, CommentReturn
from connector import query_handler

router = APIRouter(
    prefix="/api/comment",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_comment(req: Request):
    query = "SELECT * FROM comments;"
    rsp = await query_handler(req.app.state.db, query, 404, "No comments")
    req.app.log.info(f"Retrieving all comments")
    return [dict(comment) for comment in rsp]


@router.post("/", response_model=CommentReturn)
async def creae_comment(comment: Comment, req: Request):
    query = (
        f"INSERT INTO comments (content, author_id, document_id)"
        f"VALUES ('{comment.content}', '{comment.author_id}', '{comment.document_id}')"
        "RETURNING *;"
    )
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to create document")
    req.app.log.info(f"Creating comment for document {comment.document_id}")
    return CommentReturn(**rsp[0])


@router.delete("/{comment_id}", response_model=CommentReturn)
async def delete_comment(comment_id: str, req: Request):
    query = f"DELETE FROM comments WHERE comment_id = '{comment_id}' RETURNING *;"
    rsp = await query_handler(req.app.state.db, query, 500, "Unable to delete document")
    req.app.log.info(f"Deleting comment {comment_id}")
    return CommentReturn(**rsp[0])
