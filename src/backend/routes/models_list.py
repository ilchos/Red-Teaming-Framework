from fastapi import APIRouter
from schemas import ModelsListResponse

router = APIRouter()


@router.get("/models_list", response_model=ModelsListResponse)
async def get_models_list():
    list_models = [
        "openai/gpt-3.5-turbo-0125",
        "openai/gpt-4o-mini",
        "google/gemini-pro",
    ]
    return ModelsListResponse(result=list_models)
