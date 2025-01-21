from datetime import datetime
from typing import Optional, List

from fastapi import File, UploadFile
from pydantic import BaseModel, ConfigDict



class EmbeddingIdRequest(BaseModel):
    id: int

# Pydantic schema for input
class EmbeddingRequest(BaseModel):
    text: str
    embedding: list


class TextRequest(BaseModel):
    chunks: List[str]

