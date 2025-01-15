# Embedding Service

## Overview
The Embedding Service is a RESTful API that allows users to convert chunks into embeddings. 

## Features
- convert chunks to embeddings 
- search by embedding id

## API Endpoints

### 1. create Embeddings 
- **Endpoint**: `POST /embeddings/{id}`
- **Request Body**:
- **Response**:
  ```json
  {"embeddings": [[floats]]}
  

### Requirements
- Python 3.9+
- FastAPI

### Installation
1. Create Virtual environment ```python -m venv venv```
2. Install requirements ``` pip install -r requirements.txt```

### Start
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port  9002
```
### Testing
pytest --cov=app tests/

pytest --cov=app --cov-report=term-missing

pytest --cov=app --cov-report=html tests/
### License
This project is licensed under the MIT License. See the LICENSE file for details.
