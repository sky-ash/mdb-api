from fastapi import APIRouter
router = APIRouter()

from app.utils import process_request
@router.get("/api/v1/getByName")
def getByName(name: str):
    result = process_request(name)
    return result

@router.get("/health")
def health_check():
    return {"status": "UP"}

from fastapi.responses import RedirectResponse
@router.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/redoc")