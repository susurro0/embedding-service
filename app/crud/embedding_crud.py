import json
from typing import Optional, List

from app.models.models import Embedding


class EmbeddingCRUD:
    def __init__(self):
        pass
    def save_embedding(self, chunks: List[str], embeddings: List[List[float]]) -> List[Embedding]:
        """
        Save the embedding as a list in the database.
        """
        embedding_instances = []
        for i in range(len(chunks)):
            embedding_instance = Embedding.create(
                text=chunks[i],
                embedding=str(embeddings[i])  # Save as string representation of a list
            )
            embedding_instances.append(embedding_instance)
        return embedding_instances

    def get_embedding_by_id(self, embedding_id: int):
        embedding_instance = Embedding.get_or_none(Embedding.id == embedding_id)

        if embedding_instance:
            try:
                embedding = None
                embedding_str = embedding_instance.embedding  # Assume this is a string
                try:
                    # If the embedding is a Python literal (like a list in string format)
                    embedding = list(map(float, embedding_str.split()))
                except (ValueError, SyntaxError) as e:
                    print(f"Warning converting string to list: {e}")
                    # Handle the error (maybe use default or log)            # json_str = json.dumps(embedding_instance.embedding.tolist())

                # Deserialize the embedding from JSON string back into a list
                embedding = json.loads(embedding_str)
                print("##5")
                return embedding_instance, embedding
            except json.JSONDecodeError:
                print("Error decoding JSON from embedding")
                return None  # You can raise an HTTPException if needed here
        return None

