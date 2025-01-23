import json
from typing import List

from sentence_transformers import SentenceTransformer
from fastapi import APIRouter, HTTPException, Depends

from app.api.schemas.embedding_schemas import TextRequest
from app.core.dependencies import Dependency
from app.crud.embedding_crud import EmbeddingCRUD
from app.utils.embedding_utils import compute_embeddings_from_texts, convert_embedding_to_float_list


class EmbeddingRoutes:
    def __init__(self, dependency: Dependency, embedding_crud=EmbeddingCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db  # Assuming `get_db` is the correct way to access the database session
        self.embedding_crud = embedding_crud

        @self.router.post("/embedding/text/")
        async def create_embedding_from_text(request: TextRequest):
            embeddings = compute_embeddings_from_texts(request.chunks)
            embedding_instances = embedding_crud.save_embedding(request.chunks, embeddings)
            return {"embeddings": [convert_embedding_to_float_list(instance) for instance in embedding_instances]}


        @self.router.get("/embeddings/{id}")
        async def get_embedding(id: int):
            # Retrieve embedding by ID
            result = embedding_crud.get_embedding_by_id(id)
            if result:
                embedding_instance, embedding = result
                return {"id": embedding_instance.id, "text": embedding_instance.text, "embedding": embedding}
            else:
                raise HTTPException(status_code=404, detail="Embedding not found")
