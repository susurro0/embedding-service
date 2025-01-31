from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints import EmbeddingRoutes
from app.core.dependencies import Dependency
from app.core.initializer import AppInitializer


from app.database.database import Database
from crud.embedding_crud import EmbeddingCRUD
from database.database import database_instance


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5174"],  # Adjust to your frontend URL
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
    initializer = AppInitializer(app, database_instance.database)
    initializer.initialize()

    dependency = Dependency(initializer.db)

    # Include routers
    embedding_routes = EmbeddingRoutes(dependency=dependency, embedding_crud=EmbeddingCRUD())
    app.include_router(embedding_routes.router)
    return app




if __name__ == "__main__": # pragma: no cover
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=9002)