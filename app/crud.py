import ast
from typing import List

from app.models import Embedding
import numpy as np

import json

def save_embedding(text: str, embedding: List[float]) -> Embedding:
    """
    Save the embedding as a list in the database.
    """
    embedding_instance = Embedding.create(
        text=text,
        embedding=str(embedding)  # Save as string representation of a list
    )
    return embedding_instance

def get_embedding_by_id(embedding_id: int):
    embedding_instance = Embedding.get_or_none(Embedding.id == embedding_id)

    if embedding_instance:
        try:
            embedding =None
            embedding_str = embedding_instance.embedding  # Assume this is a string
            try:
                # If the embedding is a Python literal (like a list in string format)
                embedding = list(map(float, embedding_str.split()))
                print(embedding)
            except (ValueError, SyntaxError) as e:
                print(f"Error converting string to list: {e}")
                # Handle the error (maybe use default or log)            # json_str = json.dumps(embedding_instance.embedding.tolist())

            # Deserialize the embedding from JSON string back into a list
            embedding = json.loads(embedding_str)
            print("##5")
            return embedding_instance, embedding
        except json.JSONDecodeError:
            print("Error decoding JSON from embedding")
            return None  # You can raise an HTTPException if needed here
    return None
