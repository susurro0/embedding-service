import json
from typing import List

from sentence_transformers import SentenceTransformer
from fastapi import APIRouter, HTTPException, Depends

from app.api.schemas.embedding_schemas import TextRequest
from app.core.dependencies import Dependency
from app.crud.embedding_crud import EmbeddingCRUD


class EmbeddingRoutes:
    def __init__(self, dependency: Dependency, embedding_crud=EmbeddingCRUD):
        self.router = APIRouter()
        self.db = dependency.get_db  # Assuming `get_db` is the correct way to access the database session
        self.embedding_crud = embedding_crud
        self.model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

        @self.router.post("/embedding/text/")
        @self.router.post("/embedding/text/")
        async def create_embedding_from_text(request: TextRequest):
            embeddings = _compute_embeddings_from_texts(request.chunks)
            embedding_instances = embedding_crud.save_embedding(self, request.chunks, embeddings)
            return {"embeddings": [_convert_embedding_to_float_list(instance) for instance in embedding_instances]}

        def _compute_embedding_from_text(text: str) -> List[float]:
            """
            Compute the embedding for the input text and return as numpy array.
            """
            embedding = self.model.encode(text)
            # Return as a numpy array (instead of JSON string)
            return embedding.tolist()

        def _compute_embeddings_from_texts(texts: List[str]) -> List[List[float]]:
            """
            Compute embeddings for a list of texts.
            """
            embeddings = self.model.encode(texts)
            return [embedding.tolist() for embedding in embeddings]

        @self.router.get("/embeddings/{id}")
        async def get_embedding(id: int):
            # Retrieve embedding by ID
            result = embedding_crud.get_embedding_by_id(self, id)
            if result:
                embedding_instance, embedding = result
                return {"id": embedding_instance.id, "text": embedding_instance.text, "embedding": embedding}
            else:
                raise HTTPException(status_code=404, detail="Embedding not found")

        def _convert_embedding_to_float_list(embedding_instance) -> List[float]:
            """
            Convert the embedding instance (stored as a string) to a list of floats.

            Args:
                embedding_instance: The instance containing the embedding (stored as a string).

            Returns:
                List[float]: A list of floats representing the embedding.
            """
            try:
                embedding_str = embedding_instance.embedding
                try:
                    return list(map(float, embedding_str.split()))
                except ValueError:
                    return json.loads(embedding_str)
            except (ValueError, json.JSONDecodeError, AttributeError) as e:
                raise ValueError(f"Failed to parse embedding: {e}")

