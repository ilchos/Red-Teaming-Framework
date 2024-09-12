from fastapi import APIRouter, Depends, HTTPException
from pg_client import PostgresClient, get_postgres_client
from pydantic import ValidationError
from schemas import UploadFileRequest

router = APIRouter()


# Эндпоинт для загрузки JSON файла
@router.post("/upload")
async def upload_jsonlist(
    data_list: list[UploadFileRequest],
    postgres_client: PostgresClient = Depends(get_postgres_client),
):
    validated_data_list = []
    errors = []

    for index, data in enumerate(data_list):
        try:
            # Валидация данных по схеме
            validated_data = UploadFileRequest(**data.dict())

            # Если валидация прошла успешно, добавляем данные в список
            validated_data_list.append(validated_data)

        except ValidationError as e:
            # Если данные не соответствуют схеме, добавляем ошибки в список
            file_errors = e.errors()
            error_messages = [
                f"{error['loc'][0]}: {error['msg']}" for error in file_errors
            ]
            errors.append(f"Ошибки в объекте {index}: {', '.join(error_messages)}")

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    try:
        postgres_client.insert_competitors(validated_data_list)
    except Exception:
        raise HTTPException(status_code=400, detail=errors)

    return {
        "message": "Данные успешно загружены и проверены",
        "data": validated_data_list,
    }
