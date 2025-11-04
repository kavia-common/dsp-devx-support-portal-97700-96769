from fastapi import APIRouter

router = APIRouter(tags=["health"])


# PUBLIC_INTERFACE
@router.get("/", summary="Health Check", description="Health check endpoint.\nReturns a simple payload to indicate the service is running.")
def health_check():
    """Health check endpoint that returns a simple payload to indicate service is up."""
    return {"message": "Healthy"}
