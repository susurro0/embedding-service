from fastapi import APIRouter
from app.models import Text
from app.services import add_text, search

router = APIRouter()

@router.post("/add_text")
async def add_text_endpoint(text: Text):
    add_text(text.text)
    return {"message": "Text added successfully"}

@router.post("/search")
async def search_endpoint(text: Text):
    D, I = search(text.text)
    return {"distances": D.tolist(), "indices": I.tolist()}