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
    text: str


@app.post("/embedding/")
async def create_embedding(request: EmbeddingRequest):
    # Convert the list to a numpy array
    embedding_array = np.array(request.embedding)

    # Save the embedding in the database
    embedding_instance = save_embedding(request.text, embedding_array)
    return {"id": embedding_instance.id, "text": embedding_instance.text}

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
    embedding_array = compute_embedding_from_text(request.text)

    # Save the embedding in the database
    embedding_instance = save_embedding(request.text, embedding_array)
    return {"id": embedding_instance.id, "text": embedding_instance.text}


@app.get("/embeddings/{id}")
async def get_embedding(id: int):
    # Retrieve embedding by ID
    result = get_embedding_by_id(id)
    if result:
        embedding_instance, embedding = result
        return {"id": embedding_instance.id, "text": embedding_instance.text, "embedding": embedding}
    else:
        raise HTTPException(status_code=404, detail="Embedding not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9002)