from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/health", status_code=200)
async def health() -> dict:
    """Return OK if program is running

    Raises:
        HTTPException: Raised if any error occurs while calling this endpoint

    Returns:
        dict: A dictionary with property "result" set to OK
    """
    try:
        return {'result': 'OK'}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))