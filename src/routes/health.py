from fastapi import APIRouter

router = APIRouter()


@router.post("/health")
@router.get("/health")
async def health():
    return {"status": "ok"}
