from fastapi import FastAPI
from app.routes import files

app = FastAPI(title="Mini Cloud", version="1.0")
app.include_router(files.router)