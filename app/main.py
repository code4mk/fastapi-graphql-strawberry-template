from fastapi import FastAPI, BackgroundTasks, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.config.cors import CORS_CONFIG
from app.api import health, root_index
from app.database.database import get_db_session
from sqlalchemy.orm import Session


app = FastAPI()

# Add CORS middleware with configuration from cors.py
app.add_middleware(CORSMiddleware, **CORS_CONFIG)


async def get_context(
    request: Request,
    background_tasks: BackgroundTasks,
    db_session: Session = Depends(get_db_session),
) -> dict:
    """Get the context for the request."""
    return {"request": request, "background_tasks": background_tasks, "db": db_session}


# GraphQL Router
graphql_app = GraphQLRouter(schema, graphql_ide="apollo-sandbox", context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

# Include the root index and health router
app.include_router(root_index.router)
app.include_router(health.router, prefix="/health")
