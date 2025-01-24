from sentence_transformers import SentenceTransformer
from typing import List
import json

from torch import Tensor

model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

def compute_embedding_from_text(text: str) -> Tensor:
    """
    Compute the embedding for the input text and return as a numpy array.
    """
    return model.encode(text)

def compute_embeddings_from_texts(texts: List[str]) -> List[List[float]]:
    """
    Compute embeddings for a list of texts.
    """
    embeddings = model.encode(texts)
    return [embedding.tolist() for embedding in embeddings]

def convert_embedding_to_float_list(embedding_instance) -> List[float]:
    """
    Convert the embedding instance (stored as a string) to a list of floats.
    """
    try:
        embedding_str = embedding_instance.embedding
        try:
            return list(map(float, embedding_str.split()))
        except ValueError:
            return json.loads(embedding_str)
    except (ValueError, json.JSONDecodeError, AttributeError) as e:
        raise ValueError(f"Failed to parse embedding: {e}")
