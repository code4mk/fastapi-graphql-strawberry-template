from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

# Create a api router
router = APIRouter()


# root index
@router.get("/")
async def root_index(request: Request) -> JSONResponse:
    """Root index route."""
    data = {
        "message": "fastapi (strawberry) is running....",
        "graphql_url": str(request.base_url) + "graphql",
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)


@router.get("/the-index")
async def the_index(request: Request) -> JSONResponse:
    """Index route."""
    data = {
        "message": "fastapi (strawberry) is running....",
        "graphql_url": str(request.base_url) + "graphql",
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)
