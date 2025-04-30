from fastapi import APIRouter, UploadFile, HTTPException, File, Query

from app.database import add_text_file_data
from app.tfidf.schemas import UploadFileSchema
from app.tfidf.services import process_text

router = APIRouter()


@router.post(
    "/upload-file",
    summary="Загрузить файл для анализа",
    response_model=UploadFileSchema)
async def upload_file(
        file: UploadFile = File(
            ...,
            description=f"Разрешены только файлы с расширением .txt")
) -> UploadFileSchema:
    if not file.filename.lower().endswith('.txt'):
        raise HTTPException(
            status_code=400,
            detail="Разрешены только файлы с расширением .txt"
        )

    file_data = await file.read()

    word_stats = process_text(file_data.decode("utf-8"))
    await add_text_file_data(file.filename, word_stats)
    response = UploadFileSchema(file_name=file.filename, word_stats=word_stats[:50])
    return response


@router.get(
    "/get-file-data",
    summary="Получить данные TF-IDF анализа")
async def get_file_data(
        file_id: int = Query(..., description="ID проанализированного файла"),
        offset: int = Query(0, description="offset")
):
    return {"result": "# TODO"}
