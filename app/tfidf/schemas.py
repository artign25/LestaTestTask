from typing import List

from pydantic import BaseModel, Field


class WordSchema(BaseModel):
    word: str = Field(..., description="Word"),
    tf: int = Field(..., description="TF"),
    idf: float = Field(..., description="IDF")


class GetFileData(BaseModel):
    word_stats: List[WordSchema]


class UploadFileSchema(BaseModel):
    file_name: str = Field(..., description="File name")
    word_stats: List[WordSchema]
