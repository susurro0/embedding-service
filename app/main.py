import json
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from starlette.middleware.cors import CORSMiddleware

from app.crud import save_embedding, get_embedding_by_id
from app.database import initialize_db
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5174", "http://localhost:9001"],  # Adjust to your frontend URL
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
# Initialize DB
initialize_db()

class EmbeddingIdRequest(BaseModel):
    id: int

# Pydantic schema for input
class EmbeddingRequest(BaseModel):
    text: str
    embedding: list


class TextRequest(BaseModel):
    chunks: List[str]


# Placeholder function to simulate embedding generation from text
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

def compute_embedding_from_text(text: str) -> List[float]:
    """
    Compute the embedding for the input text and return as numpy array.
    """
    embedding = model.encode(text)
    # Return as a numpy array (instead of JSON string)
    return embedding.tolist()


@app.post("/embedding/text/")
async def create_embedding_from_text(request: TextRequest):
    # Compute the embedding from the text (e.g., using a pre-trained model)
    embedding_array = []
    for chunk in request.chunks:
        embedding = compute_embedding_from_text(chunk)  # Use your embedding function here
        embedding_array.append(embedding)

    # Save the embedding in the database
    embedding_instances = save_embedding(request.chunks, embedding_array)
    embeddings = []
    for embedding in embedding_instances:
        embeddings.append(__convert_embedding_to_float_list(embedding))
    return {"embeddings": embeddings}


@app.get("/embeddings/{id}")
async def get_embedding(id: int):
    # Retrieve embedding by ID
    result = get_embedding_by_id(id)
    if result:
        embedding_instance, embedding = result
        return {"id": embedding_instance.id, "text": embedding_instance.text, "embedding": embedding}
    else:
        raise HTTPException(status_code=404, detail="Embedding not found")

import json

def __convert_embedding_to_float_list(embedding_instance) -> list:
    """
    Convert the embedding instance (stored as string) to a list of floats.

    Args:
        embedding_instance: The instance containing the embedding (stored as string).

    Returns:
        list: A list of floats representing the embedding.
    """
    try:
        embedding_str = embedding_instance.embedding  # Assume this is a string

        # Try to split the string into floats (space-separated)
        try:
            embedding_floats = list(map(float, embedding_str.split()))
            print("Successfully converted string to list of floats:", embedding_floats)
        except ValueError as e:
            print(f"Error converting string to list using split: {e}")
            # Handle if the string is not space-separated, maybe log or use defaults

            # Try to deserialize from JSON format (if it's a JSON string of the list)
            try:
                embedding_floats = json.loads(embedding_str)
                print("Successfully deserialized embedding from JSON:", embedding_floats)
            except json.JSONDecodeError as e:
                print(f"Error deserializing string from JSON: {e}")
                # Handle the error (maybe return an empty list or raise exception)

        return embedding_floats

    except Exception as e:
        print(f"An error occurred while converting embedding: {e}")
        # Return an empty list or raise exception if needed
        return []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9002)