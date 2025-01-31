import json
from typing import Optional, List

import numpy as np
from fastapi import HTTPException

from app.models.embedding_model import Embedding


class EmbeddingCRUD:
    def __init__(self):
        pass
    def save_embedding(self, chunks: List[str], embeddings: List[List[float]]) -> List[Embedding]:
        """
        Save the embedding as a list in the database.
        """
        embedding_instances = []
        for chunk, embedding in zip(chunks, embeddings):
            embedding_instance = Embedding.create(
                text=chunk,
                embedding=embedding  # Save as string representation of a list
            )
            embedding_instances.append(embedding_instance)
        return embedding_instances

    def get_embedding_by_id(self, embedding_id: int):
        embedding_instance = Embedding.get_or_none(Embedding.id == embedding_id)
        try:

            if embedding_instance:
                return embedding_instance, embedding_instance.embedding
        except Exception:
            raise HTTPException(status_code=404, detail="Embedding not found")
        return None

