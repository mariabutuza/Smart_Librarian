from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.images import router as images_router

app = FastAPI(
    title="Smart Librarian API",
    version="1.0.0",
)

app.include_router(chat_router)
app.include_router(images_router)


@app.get("/")
def root():
    return {
        "message": "Smart Librarian API is running."
    }

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
