from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.database import recreate_tables
from app.tfidf.routers import router
from app.tfidf.services import process_text


@asynccontextmanager
async def lifespan(_application: FastAPI):
    await recreate_tables()
    yield
    print("Goodbye, World!")


app = FastAPI(lifespan=lifespan)

app.include_router(router=router, prefix="/tfidf", tags=["TF-IDF анализ документа"])

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Главная страница с формой загрузки файла"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_text(request: Request, file: UploadFile = File(...)):
    """Обрабатывает загруженный файл и возвращает результаты"""
    if not file.filename.endswith('.txt'):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Пожалуйста, загрузите текстовый файл (.txt)"
        })

    contents = await file.read()
    text = contents.decode('utf-8')

    word_stats = process_text(text)[:50]

    return templates.TemplateResponse("results.html", {
        "request": request,
        "word_stats": word_stats
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
