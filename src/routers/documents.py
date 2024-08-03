from fastapi import APIRouter, HTTPException
from ..models import BlogDocument

router = APIRouter(
    prefix="/api/docuement",
    tags=["document"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[BlogDocument])
async def get_documents():
    return []


@router.post("/", response_model=BlogDocument)
async def create_document():
    return {}


@router.get("/{document_id}", response_model=BlogDocument)
async def get_document():
    return {}


@router.put("/{document_id}", response_model=BlogDocument)
async def update_document():
    return {}


@router.delete("/{document_id}", response_model=BlogDocument)
async def update_document():
    return {}


@router.post("/{document_id}/comment", response_model=BlogDocument)
async def create_comment():
    return {}


@router.get("/{document_id}/comment", response_model=BlogDocument)
async def get_comments():
    return {}


@router.get("/{document_id}/comment/{comment_id}", response_model=BlogDocument)
async def get_comment():
    return {}


@router.delete("/{document_id}/comment/{comment_id}", response_model=BlogDocument)
async def delete_comment():
    return {}
